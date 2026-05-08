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
- **Search** — two modes: session name (incremental) and content (full-text across all sessions). Hits are highlighted in-context with jump navigation
- Session rename support
- Token count per session
- **Playback mode** — replay a session with smooth bubble animations (▶ play/pause, ⏹ stop, speed slider). Controls tucked into a collapsible panel
- **Quote mode** — select messages and copy as labeled text. User/Agent display names are customizable (e.g. "少佐" / "バトー")
- **Auto-linking** — URLs in messages are automatically converted to clickable links (`target="_blank"`)
- Dark / Light / AUTO theme
- EN / JA UI language toggle
- Reload button to pick up new sessions
- **Mobile-friendly** — responsive 3-row header layout that avoids overlap on small screens

### Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

> **Apple Silicon (M1/M2/M3) users:** Make sure you are using an **arm64-native** Python.
> System Python from Xcode Command Line Tools may be too old (3.9), and Intel-version (`x86_64`) Python installed via Rosetta Homebrew (`/usr/local/bin/brew`) can cause architecture mismatch errors.
> We recommend installing via **arm64 Homebrew** (`/opt/homebrew/bin/brew`):
> ```bash
> brew install python@3.12
> ```

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
pip install -e .
python3 -m claude_log_viewer.main
```

Then open http://127.0.0.1:4512 in your browser.

**Quick alias (optional)**

For one-command startup, install the package and add a shell alias:

```bash
cd claude-log-viewer
source .venv/bin/activate
pip install -e .
```

Add to your `~/.zshrc` (or `~/.bashrc`):

```bash
alias clv='source ~/claude-log-viewer/.venv/bin/activate && claude-log-viewer'
```

Then just run `clv` from anywhere.

### Playback mode

Open the playback panel with the ▼ toggle in the header, then press ▶ to replay the conversation with a smooth bubble animation.

- **▶ / ⏸** — play or pause. Pausing keeps your position; pressing ▶ again resumes from where you stopped
- **⏹** — stop and show all messages instantly
- **Speed slider** — drag to adjust playback speed (0.05x slow to 4x fast)

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
- **検索** — セッション名検索（インクリメンタル）と本文検索（全セッション横断）の2モード。ヒット箇所をハイライト表示＆ジャンプナビ付き
- セッション名の手動変更
- セッションごとのトークン数表示
- **再生モード** — セッションを吹き出しアニメーションで追体験（▶ 再生/一時停止、⏹ 停止、速度スライダー）。折りたたみパネルに格納
- **引用モード** — メッセージを選択してラベル付きテキストとしてコピー。User/Agent の表示名をカスタマイズ可能（例:「少佐」/「バトー」）
- **URLの自動リンク化** — メッセージ内のURLをクリック可能なリンクに自動変換（`target="_blank"`）
- ダーク / ライト / AUTO テーマ切り替え
- EN / JA 言語切り替え
- リロードボタン（新しいセッションを再読み込み）
- **モバイル対応** — スマホでも見やすい3段構成のレスポンシブヘッダー

### 必要なもの

- Python 3.11 以上
- [uv](https://docs.astral.sh/uv/)（推奨）または pip

> **Apple Silicon（M1/M2/M3）の場合:** **arm64ネイティブ** の Python を使ってください。
> Xcode Command Line Tools 付属の Python は 3.9 と古く、Rosetta 経由の Intel版 Homebrew（`/usr/local/bin/brew`）で入れた Python はアーキテクチャ不一致エラーの原因になります。
> **arm64 Homebrew**（`/opt/homebrew/bin/brew`）経由でのインストールを推奨します：
> ```bash
> brew install python@3.12
> ```

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
pip install -e .
python3 -m claude_log_viewer.main
```

起動したら http://127.0.0.1:4512 をブラウザで開いてください。

**ワンコマンド起動（オプション）**

パッケージをインストールしてシェルエイリアスを設定すると、`clv` 一発で起動できます：

```bash
cd claude-log-viewer
source .venv/bin/activate
pip install -e .
```

`~/.zshrc`（または `~/.bashrc`）に追加：

```bash
alias clv='source ~/claude-log-viewer/.venv/bin/activate && claude-log-viewer'
```

以降は `clv` だけで起動できます。

### 再生モード

ヘッダーの ▼ トグルで再生パネルを開き、▶ を押すと会話を吹き出しアニメーションで追体験できます。

- **▶ / ⏸** — 再生または一時停止。一時停止した位置から再開できます
- **⏹** — 停止して全メッセージを即時表示
- **速度スライダー** — ドラッグして再生速度を調整（0.05x〜4x）

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

## Troubleshooting / トラブルシューティング

### `ImportError: incompatible architecture (have 'x86_64', need 'arm64')`

This happens when Python or its packages were installed for the wrong CPU architecture (typically Intel Homebrew on Apple Silicon).

Apple Silicon で Intel 版の Python やパッケージがインストールされている場合に発生します。

**Fix / 対処法:**

```bash
# 1. Remove the existing venv / 既存の venv を削除
rm -rf .venv

# 2. Confirm you are using arm64 Python / arm64版 Python を確認
file $(which python3)
# Expected: "Mach-O 64-bit executable arm64"

# 3. If it shows x86_64, install arm64 Python via Homebrew
#    x86_64 と表示された場合、arm64 Homebrew で Python を入れ直す
/opt/homebrew/bin/brew install python@3.12

# 4. Recreate the venv with the correct Python / 正しい Python で venv を再作成
/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### System Python is too old (`python3 --version` shows 3.9 or older)

macOS ships with Python from Xcode Command Line Tools, which may be 3.9. This project requires 3.11+.

macOS 付属の Python（Xcode Command Line Tools 経由）は 3.9 の場合があります。本プロジェクトは 3.11 以上が必要です。

**Fix / 対処法:**

```bash
brew install python@3.12
# Then create the venv with the new version / 新しいバージョンで venv を作成
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## License

MIT
