# claude-log-viewer

A local web viewer for [Claude Code](https://claude.ai/code) session logs (`.jsonl` files).

ローカルで動く Claude Code セッションログビューアーです。

---

## English

### What is this?

Claude Code automatically saves all session logs to `~/.claude/projects/`. This tool lets you browse and read those logs in a clean chat-style web UI.

**Features**
- Chat-style timeline (user messages on the right, assistant on the left)
- Tool calls (Bash, Read, Edit, etc.) shown as collapsible rows
- Session list grouped by project and date, with time range display
- Session rename support
- Token count per session
- Dark / Light / AUTO theme
- EN / JA UI language toggle
- Reload button to pick up new sessions

### Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

**With uv (recommended)**

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and run
git clone https://github.com/law5/claude-log-viewer.git
cd claude-log-viewer
uv run python -m claude_log_viewer.main
```

**With pip**

```bash
git clone https://github.com/law5/claude-log-viewer.git
cd claude-log-viewer
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
python3 -m claude_log_viewer.main
```

Then open http://127.0.0.1:4512 in your browser.

### Adding custom session files

Place any `.jsonl` files under a subdirectory of `~/.claude/projects/`, then click the reload button in the UI.

```
~/.claude/projects/
  my-custom-sessions/
    mysession.jsonl   ← will appear in the sidebar
```

### Browser permission dialog

When using the folder picker, your browser may show a dialog:

> **"Allow this site to view and copy files?"**
> `http://127.0.0.1:4512` can view files in "..." and make copies

This is normal. The tool runs entirely on your local machine and never sends data externally. Click **Allow**.

### Environment variable

If you use a custom Claude config directory, set `CLAUDE_CONFIG_DIR`:

```bash
CLAUDE_CONFIG_DIR=/path/to/config uv run python -m claude_log_viewer.main
```

---

## 日本語

### これは何？

Claude Code はセッションのログを自動的に `~/.claude/projects/` に保存します。このツールはそれをチャット形式のWebUIで読めるようにするローカルビューアーです。

**機能**
- チャット形式のタイムライン表示（ユーザー右・AIアシスタント左）
- ツール呼び出し（Bash, Read, Edit 等）を折りたたみ行で表示
- プロジェクト別・日付別セッション一覧（時間帯表示付き）
- セッション名の手動変更
- セッションごとのトークン数表示
- ダーク / ライト / AUTO テーマ切り替え
- EN / JA 言語切り替え
- リロードボタン（新しいセッションを再読み込み）

### 必要なもの

- Python 3.11 以上
- [uv](https://docs.astral.sh/uv/)（推奨）または pip

### インストール

**uv を使う場合（推奨）**

```bash
# uv がなければインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# クローンして起動
git clone https://github.com/law5/claude-log-viewer.git
cd claude-log-viewer
uv run python -m claude_log_viewer.main
```

**pip を使う場合**

```bash
git clone https://github.com/law5/claude-log-viewer.git
cd claude-log-viewer
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
python3 -m claude_log_viewer.main
```

起動したら http://127.0.0.1:4512 をブラウザで開いてください。

### カスタムファイルの追加

`~/.claude/projects/` 以下の任意のサブフォルダに `.jsonl` ファイルを置いて、UIのリロードボタンを押すと左サイドバーに表示されます。

```
~/.claude/projects/
  my-sessions/
    mysession.jsonl   ← サイドバーに表示される
```

### ブラウザの許可ダイアログについて

フォルダ選択時にブラウザから以下のようなダイアログが表示される場合があります：

> **「このサイトにファイルの表示とコピーを許可しますか？」**
> `http://127.0.0.1:4512` は「...」内のファイルを表示し、独自のコピーを作成できます

これは正常な動作です。データは完全にローカルで処理され、外部には送信されません。**「許可する」** をクリックしてください。

### 環境変数

Claude のコンフィグディレクトリをカスタマイズしている場合は `CLAUDE_CONFIG_DIR` を設定してください：

```bash
CLAUDE_CONFIG_DIR=/path/to/config uv run python -m claude_log_viewer.main
```

---

## License

MIT
