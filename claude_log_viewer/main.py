import json
import os
import re
from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

app = FastAPI(title="Claude Log Viewer")

# Config file for custom paths and session names
CONFIG_PATH = Path.home() / ".config" / "claude-log-viewer" / "config.json"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    return {"extra_paths": [], "session_names": {}}


def save_config(config: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False))


def get_log_dirs() -> list[Path]:
    """Return all log source directories to scan."""
    # Default: CLAUDE_CONFIG_DIR env or ~/.claude/projects
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
    if config_dir:
        default = Path(config_dir) / "projects"
    else:
        default = Path.home() / ".claude" / "projects"

    dirs = [default]
    config = load_config()
    for p in config.get("extra_paths", []):
        extra = Path(p)
        if extra not in dirs:
            dirs.append(extra)
    return dirs


def get_session_meta(path: Path) -> dict:
    """Extract first user text, first timestamp, and last timestamp from a .jsonl file."""
    first_text = ""
    first_ts = ""
    last_ts = ""
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") not in ("user", "assistant"):
                    continue
                ts = entry.get("timestamp", "")
                if ts:
                    if not first_ts:
                        first_ts = ts
                    last_ts = ts
                if not first_text and entry.get("type") == "user":
                    message = entry.get("message", {})
                    if not isinstance(message, dict):
                        continue
                    content = message.get("content")
                    if isinstance(content, str) and content.strip():
                        first_text = content.strip()
                    elif isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict) and c.get("type") == "text":
                                text = c.get("text", "").strip()
                                if text:
                                    first_text = text
                                    break
    except Exception:
        pass
    return {"first_text": first_text, "first_ts": first_ts, "last_ts": last_ts}


def parse_session(path: Path) -> dict:
    messages = []
    total_tokens = 0

    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_type = entry.get("type")
                if msg_type not in ("user", "assistant"):
                    continue

                message = entry.get("message", {})
                if not isinstance(message, dict):
                    continue

                if msg_type == "assistant":
                    usage = message.get("usage", {})
                    total_tokens += usage.get("input_tokens", 0) + usage.get("output_tokens", 0)

                content = message.get("content")
                if not content:
                    continue

                if isinstance(content, str):
                    content = [{"type": "text", "text": content}]
                if not isinstance(content, list):
                    continue

                items = []
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    t = c.get("type")
                    if t == "text" and c.get("text"):
                        items.append({"type": "text", "text": c["text"]})
                    elif t == "tool_use":
                        tool_input = c.get("input", {})
                        cmd = (
                            tool_input.get("command")
                            or tool_input.get("path")
                            or tool_input.get("file_path")
                            or tool_input.get("prompt")
                            or str(tool_input)[:80]
                        )
                        items.append({
                            "type": "tool_use",
                            "name": c.get("name", "Tool"),
                            "cmd": cmd,
                            "input": tool_input,
                        })
                    elif t == "tool_result":
                        result_content = c.get("content", "")
                        if isinstance(result_content, list):
                            result_content = " ".join(
                                x.get("text", "") for x in result_content if isinstance(x, dict)
                            )
                        items.append({
                            "type": "tool_result",
                            "text": str(result_content)[:500],
                        })

                if items:
                    messages.append({
                        "role": msg_type,
                        "timestamp": entry.get("timestamp", ""),
                        "items": items,
                        "is_sidechain": entry.get("isSidechain", False),
                    })

    except Exception:
        pass

    return {"messages": messages, "total_tokens": total_tokens}


def get_sessions() -> list[dict]:
    config = load_config()
    custom_names = config.get("session_names", {})
    sessions = []

    for log_dir in get_log_dirs():
        if not log_dir.exists():
            continue
        for project_dir in sorted(log_dir.iterdir()):
            if not project_dir.is_dir():
                continue
            project_name = project_dir.name.replace("-", "/").lstrip("/")
            # source_dir identifies which root this project belongs to
            source_dir = str(log_dir)

            for jsonl_file in sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True):
                stat = jsonl_file.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
                session_id = jsonl_file.stem
                meta = get_session_meta(jsonl_file)
                display_name = custom_names.get(session_id) or meta["first_text"] or session_id[:20]

                sessions.append({
                    "id": session_id,
                    "display_name": display_name,
                    "first_text": meta["first_text"],
                    "first_ts": meta["first_ts"],
                    "last_ts": meta["last_ts"],
                    "project": project_name,
                    "project_dir": project_dir.name,
                    "source_dir": source_dir,
                    "mtime": mtime.isoformat(),
                    "size": stat.st_size,
                })

    return sessions


# --- API routes ---

@app.get("/", response_class=HTMLResponse)
def index():
    html_path = Path(__file__).parent / "templates" / "index.html"
    return html_path.read_text()


@app.get("/api/sessions")
def list_sessions():
    return JSONResponse(get_sessions())


@app.get("/api/sessions/{project_dir}/{session_id}")
def get_session(project_dir: str, session_id: str):
    for log_dir in get_log_dirs():
        path = (log_dir / project_dir / f"{session_id}.jsonl").resolve()
        if not str(path).startswith(str(log_dir.resolve())):
            raise HTTPException(status_code=400, detail="Invalid path")
        if path.exists():
            return JSONResponse(parse_session(path))
    raise HTTPException(status_code=404, detail="Session not found")


@app.get("/api/search")
def search_content(q: str = ""):
    """Search message content across all sessions."""
    query = q.strip().lower()
    if not query or len(query) < 2:
        return JSONResponse([])

    results = []
    for log_dir in get_log_dirs():
        if not log_dir.exists():
            continue
        for project_dir in sorted(log_dir.iterdir()):
            if not project_dir.is_dir():
                continue
            for jsonl_file in sorted(project_dir.glob("*.jsonl"),
                                     key=lambda p: p.stat().st_mtime, reverse=True):
                hits = _search_session(jsonl_file, query)
                if hits:
                    session_id = jsonl_file.stem
                    results.append({
                        "session_id": session_id,
                        "project_dir": project_dir.name,
                        "hit_count": len(hits),
                        "hits": hits[:20],
                    })
    return JSONResponse(results)


def _search_session(path: Path, query: str) -> list[dict]:
    """Search a single session file for query matches in text content.

    msg_index must match the index in parse_session()'s messages array,
    so we replicate the exact same filtering logic here.
    """
    hits = []
    msg_index = -1
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg_type = entry.get("type")
                if msg_type not in ("user", "assistant"):
                    continue
                message = entry.get("message", {})
                if not isinstance(message, dict):
                    continue
                content = message.get("content")
                if not content:
                    continue
                if isinstance(content, str):
                    content = [{"type": "text", "text": content}]
                if not isinstance(content, list):
                    continue

                # Check if this entry would produce items in parse_session
                has_items = any(
                    isinstance(c, dict) and (
                        (c.get("type") == "text" and c.get("text"))
                        or c.get("type") in ("tool_use", "tool_result")
                    )
                    for c in content
                )
                if not has_items:
                    continue

                # Only count messages that parse_session would include
                msg_index += 1

                # Search text content
                for c in content:
                    if not isinstance(c, dict) or c.get("type") != "text":
                        continue
                    text = c.get("text", "")
                    if query in text.lower():
                        idx = text.lower().index(query)
                        start = max(0, idx - 40)
                        end = min(len(text), idx + len(query) + 40)
                        snippet = ("…" if start > 0 else "") + text[start:end] + ("…" if end < len(text) else "")
                        hits.append({
                            "msg_index": msg_index,
                            "role": msg_type,
                            "snippet": snippet,
                        })
                        break
    except Exception:
        pass
    return hits


@app.post("/api/sessions/{session_id}/rename")
async def rename_session(session_id: str, body: dict):
    config = load_config()
    name = body.get("name", "").strip()
    if name:
        config.setdefault("session_names", {})[session_id] = name
    else:
        config.setdefault("session_names", {}).pop(session_id, None)
    save_config(config)
    return {"ok": True}



def run():
    uvicorn.run("claude_log_viewer.main:app", host="0.0.0.0", port=4512, reload=False)


if __name__ == "__main__":
    run()
