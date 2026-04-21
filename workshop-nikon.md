author: Theo Monfort
summary: Nikon GitHub Copilot ワークショップ
id: github-copilot-workshop
categories: AI, Development
environments: Web
status: Published
feedback link: https://example.com/feedback

# Nikon GitHub Copilot ワークショップ

## ワークショップについて
Duration: 5

GitHub Copilotワークショップへようこそ！

![GitHub Copilot Logo](github-copilot-workshop/img/octocat_copilot.png)

このワークショップでは、**レガシーPHPで作られた「AI駆動開発ガイド」ページ** を題材に、GitHub Copilot の全機能を活用してモダンなウェブアプリケーションに変革する体験をしていただきます。

### 本日のゴール
- GitHub Copilot のセットアップとカスタマイズ方法を理解する
- Copilot Agent Mode でレガシーサイトを Next.js + TypeScript + Tailwind CSS に移行する
- 自動テスト、コード品質チェック、セキュリティスキャンを設定する
- Cloud Agent による自律的な機能実装を体験する
- Agentic Workflow で CI/CD パイプラインに AI を組み込む
- Copilot CLI で新規アプリケーションを構築する

### 本日のアジェンダ

| パート | 内容 | 概要 |
|---|---|---|
| Setup | プロジェクトセットアップ | テンプレートリポジトリから Codespaces を起動 |
| 1 | セットアップ＆カスタマイズ | /init、カスタム指示、Skill 作成、MCP 設定 |
| 2 | 実装：レガシーサイトの移行 | Plan Mode → Next.js + TypeScript + Tailwind への移行 |
| 3 | 自動テストと Actions | Vitest + Playwright テスト、CI ワークフロー |
| 4 | コード品質 | Copilot Code Review、GHAS 設定 |
| 5 | Cloud Agent | Issue からの自律的な機能実装 |
| 6 | Agentic Workflow | PAT 作成、テストカバレッジ自動更新 |
| 7 | CLI | AI 利用状況ダッシュボードの構築 |

### 前提条件

以下の**いずれか**の環境をご用意ください：

**オプション A: 個人環境**
- Visual Studio Code がインストールされていること
- GitHub Copilot のライセンスがあること（**Pro / Pro+ / Business / Enterprise** プラン推奨）
- GitHub アカウントを持っていること

> aside negative
> **⚠️ プランについて**: Free プランでも Agent Mode（Part 1〜2）は利用可能ですが、Cloud Agent（Part 5）、Agentic Workflow（Part 6）、自動 Code Review（Part 4）は **Pro プラン以上** が必要です。ワークショップの全パートを体験するには **Pro / Pro+ / Business / Enterprise** プランをご利用ください。

**オプション B: 企業環境（お客様向け）**
- 以下の機能が有効化されたプライベート Organization を持っていること：
  - GitHub Actions
  - GitHub Copilot（Pro+ / Business / Enterprise）
  - GitHub Advanced Security (GHAS)
- Organization 内でリポジトリを作成できる権限があること

## プロジェクトのセットアップ
Duration: 15

このワークショップでは、以下の GitHub リポジトリを使用します：

**プロジェクトURL**: https://github.com/theomonfort/2026-Github-Copilot-Workshop-Nodejs

### ステップ1: テンプレートからリポジトリを作成する

1. プロジェクト URL をブラウザで開く
2. 右上の **Use this template** ボタンをクリックし、**Create a new repository** を選択
3. リポジトリ作成画面で以下を設定：

#### Owner（オーナー）の選択

**個人で参加の場合：**
- Owner は **自分のアカウント** を選択
- Visibility は **Public** を選択（Free プランの場合、Public でないと一部機能が制限されます）

**企業の Organization で参加の場合：**
- Owner は **Copilot / Actions / GHAS / Codespaces などが有効化された Organization** を選択
- Visibility は **Private** を選択

#### Repository name（リポジトリ名）
- 任意の名前を入力してください（例: `hands-on-yourname`）

4. **Create repository** をクリック

### ステップ2: Codespaces で開発環境を起動する

1. 作成したリポジトリのページで、緑色の **Code** ボタンをクリック
2. **Codespaces** タブを選択
3. **Create codespace on main** をクリック

![Codespaces Setup](github-copilot-workshop/img/github-codespaces.png)

> aside positive
> **⏳ 注意**: Codespace の起動には数分かかる場合があります。DevContainer のビルドが完了するまでお待ちください。

DevContainer が自動的に Node.js 20 環境をセットアップし、以下が事前にインストールされます：
- GitHub Copilot & Copilot Chat 拡張機能
- Live Server 拡張機能（プレビュー用）
- GitHub CLI
- GitHub MCP Server（自動検出有効化済み）

### ステップ3: レガシーサイトを確認する

VS Code のターミナルを開き、以下のコマンドを実行してレガシーサイトを起動します：

```bash
cd github-legacy
php -S localhost:8080
```

Codespace がポート **8080** を自動検出し、**「Open in Browser」** のポップアップが表示されます。クリックしてブラウザでサイトを確認してください。

**これが今日のリファクタリング対象です。**

## セットアップ＆カスタマイズ
Duration: 20

### 1.1 — Copilot でリポジトリを理解する

まず、Copilot にこのリポジトリの全体像を把握させましょう。

> aside positive
> **💡 ヒント**: Codespaces で作業している場合、Copilot Chat の左下にある承認モードを **「Bypass Approvals」** に変更すると、ツール実行の承認をスキップでき、ワークショップをスムーズに進められます。

Copilot Chat で以下を実行します：

```
/init
```

`/init` コマンドにより、Copilot がリポジトリをスキャンし、`copilot-instructions.md` を自動生成します。（⏱ 約2分30秒）

生成された内容を確認し、レガシー PHP サイトの構造が正しく認識されていることを確認してください。

> aside negative
> **気づきましたか？** Copilot の応答が**英語**で返ってきます。`copilot-instructions.md` に言語設定がないため、Copilot はデフォルトの英語で応答しています。次のステップでこれを修正しましょう。

> aside positive
> **ポイント**: プロジェクトの文脈を一度設定すれば、以降の作業で一貫した理解に基づくアシストが可能になります。

### 1.2 — カスタム指示を追加する

`/init` で生成された `copilot-instructions.md` を日本語化し、移行ガイドラインを追加しましょう。Copilot Chat で以下のプロンプトを入力してください：

```
copilot-instructions.md を日本語にして、以下の内容を追記してください。既存の内容は残してください。

- 言語設定: すべての会話は日本語で行う
- 移行先の技術スタック: Next.js (App Router) + TypeScript + Tailwind CSS
- テスト: Vitest + Playwright
- デザイン要件: モダンで洗練されたUI、レスポンシブデザイン（モバイルファースト）
- コーディング規約: ESLint + Prettier 準拠、関数コンポーネント + Hooks、型定義は厳格に（any 禁止）
```

⏱ 約1分

> aside positive
> **ポイント**: `/init` で生成されたレガシーコードの説明を残しておくことで、Copilot は「現在の状態」と「移行先の目標」の両方を理解した上でアシストしてくれます。

### 1.3 — フロントエンド Skill を作成する

Copilot に以下のプロンプトを入力して、フロントエンド開発用の Skill を作成してもらいましょう。`[自社の会社名]` の部分を**実際の会社名に置き換えて**ください：

```
[自社の会社名] のブランディングに基づいたフロントエンド Skill を作成してください。
ウェブ上でリサーチを行い、ブランドカラー、タイポグラフィ、デザイン原則、コンポーネントパターンを定義してください。
Skill ファイルは .github/skills/ 配下に追加してください。
```

> aside negative
> **⚠️ 重要**: `[自社の会社名]` をそのまま入力しないでください。必ず実際の会社名（例: `Nikon`、`Sony`、`Toyota` など）に置き換えてください。

Copilot がウェブ上で会社のブランド情報をリサーチし、ブランドガイドラインに基づいた Skill ファイルを自動生成します。（⏱ 約2分30秒）

### 1.4 — MCP Server を確認する

MCP（Model Context Protocol）Server が正しく接続されていることを確認しましょう。

#### GitHub MCP Server の確認

`.vscode/mcp.json` に GitHub MCP Server が設定されていることを確認します：

```json
{
  "servers": {
    "github-mcp-server": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

Copilot Chat で以下を入力して、GitHub MCP Server の接続確認と Issue の作成を行います：

```
GitHub MCP Server を使って、このリポジトリに以下の Issue を作成してください：

1. このレガシー PHP サイトをモダンなフレームワークに移行する
2. 適切なテストを追加する
3. ダークモードをサポートする
4. 英語対応を追加する
```

⏱ 約30秒

> aside positive
> **ポイント**: GitHub MCP Server が正しく接続されていれば、Copilot がリポジトリに直接 Issue を作成します。作成された Issue は後のステップで活用します。

#### Playwright MCP Server の追加

テスト用に Playwright MCP Server を追加します。

1. Copilot Chat の入力欄にある **🔧 ツールボタン**（モデル選択の右側）をクリック
2. **「Add MCP Server」** を選択
3. **「Browse MCP Servers」** をクリック
4. 初回の場合は **「Enable MCP Servers Marketplace」** をクリックして有効化
5. **「Playwright」** で検索し、**Microsoft** の Playwright MCP Server を選択
6. **「Install in Workspace」** をクリックしてインストール

インストール後、`.vscode/mcp.json` に Playwright が追加されていることを確認してください：

```json
{
  "servers": {
    "github-mcp-server": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "playwright": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-server-playwright"]
    }
  }
}
```

> aside positive
> **ヒント**: 🔧 ツールボタンをクリックすると、現在 Copilot が利用可能な MCP Server とツールの一覧を確認できます。GitHub MCP Server と Playwright が表示されていれば正しく設定されています。

Playwright MCP Server が正しく動作することを確認するために、以下のプロンプトを試してみましょう：

```
Playwright を使って https://www.nikon.com を開き、スクリーンショットを撮ってください
```

スクリーンショットはプロジェクトのルートフォルダに保存されます。エクスプローラーで確認してみましょう。

> aside positive
> **ポイント**: Playwright MCP Server を使うと、Copilot がブラウザを操作してウェブページの確認やスクリーンショットの取得ができます。後のテスト工程で E2E テストにも活用します。

## 実装 — レガシーサイトの移行
Duration: 45

### 2.1 — Plan Mode で移行計画を立てる

いきなり実装に入るのではなく、まず **Plan Mode** で詳細な移行計画を立てましょう。

1. Copilot Chat のモデル選択の横にあるモード切り替えから **「Plan」** を選択
2. 以下のプロンプトを入力：

```
このレガシー PHP サイトを Next.js + Tailwind CSS に移行する計画を立ててください。
テストはまだ作成しないでください。

デザインの参考：
- 機能紹介 → モダンなタイルカード（グリッドレイアウト）
- 統計データ → テーブルではなくスタットカード形式
- FAQ → https://www.designjoy.co/ のようなクリーンなアコーディオン
- おすすめリソース → https://awesome-copilot.github.com/instructions/ のようなカード＋インストールボタン形式
```

3. Copilot が計画を立てる前に、いくつか質問をしてくることがあります。適切に回答してください。

![Plan Mode での質問例](github-copilot-workshop/img/plan-mode-questions.png)

4. Copilot が `copilot-instructions.md` の内容を踏まえて、詳細な移行計画を作成します（⏱ 約2分30秒）
5. 計画の内容を確認・調整

> aside positive
> **ポイント**: 実装前に計画を立て、レビューしてから着手できます。Plan Mode は大規模なリファクタリングやマイグレーションに最適です。

### 2.2 — 移行を実行する

計画が確定したら、**「Start with Autopilot」** ボタンをクリックして実装を開始します。

![Start with Autopilot](github-copilot-workshop/img/start-with-autopilot.png)

⏱ 約15分

Copilot エージェントが以下を自動的に実行します：
- Next.js プロジェクトの初期化
- TypeScript 設定
- Tailwind CSS の設定
- レガシー HTML からのコンテンツ移行
- コンポーネントの分割・作成
- レスポンシブレイアウトの実装

### 2.3 — 結果を確認する

移行が完了したら、サーバーを起動してブラウザでモダナイズされたサイトを確認しましょう。

ターミナルで以下のコマンドを実行します：

```bash
npm run dev
```

ポートフォワーディングの通知が表示されたら **「ブラウザで開く」** をクリックしてサイトを確認してください。

**Before → After** の違いを確認してみてください！

## 自動テストと Actions
Duration: 25

### 3.1 — 自動テストを作成する

移行したサイトに対して、自動テストを作成しましょう。

```
移行した Next.js サイトに対して、以下のテストを作成してください：

1. Vitest によるユニットテスト：
   - 各コンポーネントのレンダリングテスト
   - ProductCard コンポーネントの props テスト
   - Navigation コンポーネントのリンクテスト

2. Playwright による E2E テスト：
   - トップページの表示確認
   - ナビゲーションの動作確認
   - レスポンシブデザインの確認（モバイル・タブレット・デスクトップ）
   - 各製品カテゴリセクションへのスクロール

テストは tests/ ディレクトリに配置してください。
```

⏱ 約3〜5分

### 3.2 — GitHub Actions ワークフローを作成する

テストを PR 作成時に自動実行する GitHub Actions ワークフローを設定します。

```
以下の GitHub Actions ワークフローを作成してください：

1. PR 作成・更新時にトリガー
2. Node.js 20 環境でテストを実行
3. Vitest ユニットテストを実行
4. Playwright E2E テストを実行
5. テスト結果を PR にコメントとして投稿

ワークフローファイルは .github/workflows/test.yml に配置してください。
```

⏱ 約2分

### 3.3 — Dependency Review を追加する（ボーナス）

依存関係の脆弱性を PR 時に自動チェックする Dependency Review を追加します。

```
GitHub Actions に Dependency Review のワークフローを追加してください。
PR 作成時に依存関係の脆弱性を自動チェックし、問題があればコメントで通知するようにしてください。
```

⏱ 約1分

## コード品質
Duration: 15

### 4.1 — Copilot Auto Code Review を設定する

PR 作成時に Copilot が自動的にコードレビューを行う設定をします。

1. リポジトリの **Settings** → **Rules** → **Rulesets** → **New ruleset** → **New branch ruleset**
2. Ruleset 名を入力（例: `Require PR and CCR`）
3. **Enforcement status** を **Active** に変更
4. **Target branches** → **Add target** → **Include default branch** を選択
5. **Require a pull request before merging** を有効化
   - **Required approvals** を **1** に設定
6. **Automatically request Copilot code review** にチェック
7. **Create** をクリック

![Ruleset ターゲットブランチの設定](github-copilot-workshop/img/ruleset-target-branch.png)

> aside negative
> **注意**: Enforcement status が「Disabled」のままだとルールが適用されません。必ず **Active** に変更してください。

### 4.2 — GitHub Advanced Security (GHAS) を設定する

1. リポジトリの **Settings** → **Security** → **Advanced Security**
2. **Dependabot** セクション：
   - **Dependabot security updates** を有効化
   - **Dependabot version updates** を有効化
3. （オプション）**Tools** → **CodeQL analysis** → **Set up** → **Default** → **Enable CodeQL**

> aside negative
> **注意**: CodeQL はデフォルトブランチに存在する言語のみスキャンします。移行前のレガシー PHP しかない状態では JavaScript/TypeScript が検出されません。PR をマージした後に CodeQL を有効化すると、以降の Push/PR で自動スキャンが実行されます。

![GHAS Code Scanning Setup](github-copilot-workshop/img/code-scanning-setup.png)

### 4.3 — VS Code でコードレビューを実行する

PR を作成する前に、VS Code 上でコードレビューを実行できます。

1. **Source Control** タブを開く
2. **CHANGES** の横にある **Review uncommitted changes**（🔍アイコン）をクリック

![VS Code Review Uncommitted Changes](github-copilot-workshop/img/vscode-review-uncommitted.png)

Copilot がコードの問題点や改善提案をコメントしてくれます。

### 4.4 — コミット・Push・PR 作成

コード品質の設定が完了したら、コードをコミットして Pull Request を作成しましょう。

```
すべての変更をコミットして feature/modernize ブランチにプッシュし、main ブランチへの Pull Request を作成してください。
PR の説明に「Closes #（移行Issueの番号）」を含めてください。
```

> aside positive
> **ポイント**: PR に `Closes #N` を含めることで、PR がマージされた時に対応する Issue が自動的にクローズされます。Issue 番号は Step 1.4 で作成した移行 Issue の番号を確認してください。

### 4.5 — PR の結果を確認する

作成した PR を確認しましょう。Copilot Code Review が自動的に実行され、以下が表示されます（⏱ 約5分）：

- ✅ **Pull Request Overview** — PR 全体のサマリーコメント
- ✅ **コード提案** — 各ファイルに対する具体的な改善提案

### 4.6 — レビュー提案を修正する

Copilot のレビュー提案を修正する方法は2つあります：

1. **Commit suggestion** — 個別の提案を1つずつコミット
2. **Fix batch with Copilot** — すべての提案を一括で修正（おすすめ）

**Fix batch with Copilot** をクリックすると、修正内容を含む **新しい PR** が自動的に作成されます（⏱ 約15分）。

1. まず **修正用の新しい PR** をマージ
2. 次に **元の PR（feature/modernize）** をマージ

> aside negative
> **注意**: 場合によっては新しい PR が作成されず、修正が直接元の PR にコミットされることもあります。その場合はそのまま元の PR をマージしてください。

> aside positive
> **ポイント**:
> - Copilot Code Review のセッションは **Actions** タブで確認でき、レビュープロセスは完全に透明です。
> - レビューコメントが日本語で表示されているのは、`copilot-instructions.md` で設定した言語指定が反映されているためです！
> - `copilot-instructions.md` にレビュー観点（例: セキュリティ重視、パフォーマンス重視）を追記することで、レビュー内容をカスタマイズできます。

## Cloud Agent
Duration: 20

### 5.1 — Copilot の設定を確認する

Cloud Agent を使用するために、以下の設定を確認します：

1. GitHubの右上のプロフィールアイコン → **Copilot settings**
2. **Copilot Cloud Agent** が有効になっていることを確認

### 5.2 — 既存の Issue に Cloud Agent をアサインする

Step 1.4 で作成した Issue の中から、Cloud Agent に実装させたい Issue を開きます。

1. Issue を開く
2. 右サイドバーの **Assignees** をクリック
3. **Copilot**（GitHub）、**Claude**（Anthropic）、**Codex**（OpenAI）から選択してアサイン

![Cloud Agent アサイン画面](github-copilot-workshop/img/cloud-agent-assignees.png)

アサイン時に以下をカスタマイズできます：

- **追加プロンプト** — Issue の説明に補足指示を追加
- **モデル選択** — Copilot / Claude / Codex から選択
- **ベースブランチ** — 作業の起点となるブランチを指定

> aside positive
> **ポイント**: Cloud Agent が自律的にコードを実装し、PR を作成します（⏱ 各 Issue につき約15分）。Step 4.1 で設定した Validation Tools（CodeQL、Code Review、Secret Scanning）が有効な場合、Agent は自分の実装を検証してから PR を提出します。複数の Issue を同時にアサインすると並行して処理されます。

### 5.3 — PR を確認してマージする

Cloud Agent が作成した PR は **Draft（下書き）** 状態で作成されます。

1. PR を開き、内容を確認
2. **Ready for review** をクリックして Draft を解除
3. Copilot Code Review が自動的に開始されます
4. レビュー完了後、PR をマージ

> aside negative
> **コンフリクトが発生した場合**: 複数の Cloud Agent が並行して作業すると、同じファイルを変更してコンフリクトが発生することがあります。**Resolve conflicts** → **Fix with Copilot** をクリックすると、Copilot が自動的にコンフリクトを解決してくれます。

![Fix with Copilot でコンフリクト解決](github-copilot-workshop/img/fix-conflicts-copilot.png)

### 5.4 — 最新コードを取得して確認する

Cloud Agent の PR がマージされたら、Codespace で最新のコードを取得してサイトを確認しましょう。

```bash
git checkout main
git pull
npm install
npm run dev
```

ポートフォワーディングの通知が表示されたら **「ブラウザで開く」** をクリックして、Cloud Agent が実装した新機能を確認してください。

## Agentic Workflow
Duration: 15

### 6.1 — Personal Access Token (PAT) を作成する

Agentic Workflow で Copilot を活用するために PAT を作成します。

1. [https://github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new) にアクセス
2. 設定内容：
   - **Token name**: `copilot-workshop-agent`
   - **Resource owner**: リポジトリを作成した Organization（または個人アカウント）
   - **Repository access**: Only select repositories → 作成したリポジトリを選択
   - **Permissions**:
     - **Actions**: Read and write
     - **Contents**: Read-only
     - **Issues**: Read and write
     - **Metadata**: Read-only（自動付与）
     - **Pull requests**: Read and write

![PAT Permissions](github-copilot-workshop/img/pat-permissions.png)
3. 作成した PAT をコピー

> aside negative
> **注意**: PAT は作成時に一度だけ表示されます。必ずコピーして安全な場所に保存してください。再表示はできません。

#### リポジトリシークレットに設定

1. リポジトリの **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** をクリック
3. Name: `COPILOT_GITHUB_TOKEN`、Value: 作成した PAT

#### Workflow permissions の確認

1. **Settings** → **Actions** → **General**
2. **Allow GitHub Actions to create and approve pull requests** にチェック

### 6.2 — Daily Repo Status ワークフローを追加する

今日の活動を自動レポートするワークフローを追加しましょう。

ターミナルで以下のコマンドを実行します：

```bash
# gh aw 拡張機能をインストール
gh extension install github/gh-aw

# Daily Repo Status ワークフローを追加
gh aw add-wizard githubnext/agentics/daily-repo-status
```

ウィザードの指示に従って設定を完了してください。

追加が完了したら、手動で実行して今日の活動レポートを確認します：

```bash
gh aw run daily-repo-status
```

リポジトリの **Issues** タブに `[repo-status]` というプレフィックスの Issue が自動作成され、今日の PR、Issue、コード変更の活動サマリーが表示されます。

### 6.3 —（ボーナス）テストカバレッジ自動更新ワークフローを作成する

余裕がある方は、テストカバレッジレポートを自動更新するワークフローも作成してみましょう。

エージェントモードで以下を実行：

```
以下の Agentic Workflow を作成してください。
参照: https://github.com/github/gh-aw/blob/main/create.md

ワークフローの目的：
- main ブランチへの push 時にトリガー
- テストを実行してカバレッジレポートを生成
- カバレッジ結果を README.md のバッジとして自動更新
- 変更がある場合は PR を自動作成

ワークフローファイルは .github/workflows/coverage-update.md に配置してください。
```

## Copilot CLI
Duration: 45

### 7.1 — Copilot CLI を起動する

VS Code のターミナルで Copilot CLI を起動します：

```bash
copilot
```

### 7.2 — AI 利用状況ダッシュボードを構築する

Copilot CLI を使って、組織内の AI 利用状況を可視化するウェブサイトを構築します。

#### 準備

```
/allow-all
```

```
/model
```

最も高性能なモデル（例: Claude Opus 4.6）を選択してください。

#### 実装

**Shift+Tab** で Autopilot モードに切り替えた後、以下のプロンプトを実行：

```
/fleet 組織内の GitHub Copilot 利用状況を可視化するダッシュボード Web アプリケーションを ai-usage-dashboard/ ディレクトリに構築してください。

要件:
- フレームワーク: Next.js + TypeScript + Tailwind CSS
- GitHub Copilot Metrics API を使用してデータを取得
  - エンドポイント: GET /orgs/{org}/copilot/metrics
  - 認証: Bearer Token（環境変数 GITHUB_TOKEN から取得）
- ダッシュボード機能:
  - アクティブユーザー数の推移グラフ
  - 言語別のコード提案受入率
  - 日別・週別の利用統計
  - チャット vs コード補完の利用比率
- チャート: Recharts を使用
- レスポンシブデザイン
- ダークモード対応
- 動作確認まで行ってください
```

### 7.3 — 複数モデルでコードレビュー

作成したダッシュボードのコードを複数モデルでレビューします：

```
/review Claude Opus 4.6 と GPT-5.4 の各モデルで ai-usage-dashboard/ のコードをレビューし、結果を比較して表示してください
```

### 7.4 — Chronicle で利用状況を分析する

最後に、Copilot CLI の experimental モードを使って、自分の AI 利用状況を分析してみましょう。

```
/experimental
```

Chronicle コマンドを使用して、ワークショップ中の Copilot 利用状況のアドバイスを取得します：

```
chronicle
```

> aside positive
> **Chronicle のポイント**: Chronicle は Copilot の利用パターンを分析し、より効果的な使い方のアドバイスを提供します。個人の利用傾向に合わせた改善提案を受けることができます。

## おめでとうございます 🎉
Duration: 5

### 今日学んだこと

このワークショップでは、GitHub Copilot の全機能を横断的に体験しました：

1. **セットアップ＆カスタマイズ** — `/init`、カスタム指示、Skill 作成、MCP 設定
2. **Plan Mode による設計** — レガシーサイトの移行計画策定
3. **Agent Mode による実装** — Next.js + TypeScript + Tailwind CSS への移行
4. **自動テスト** — Vitest + Playwright + GitHub Actions
5. **コード品質** — Copilot Code Review + GHAS
6. **Cloud Agent** — Issue からの自律的な機能実装
7. **Agentic Workflow** — CI/CD パイプラインへの AI 統合
8. **Copilot CLI** — `/fleet` による並列実装、`/review` による複数モデルレビュー

### 次のステップ

- 実際のプロジェクトで Copilot を活用してみる
- Copilot Extensions や MCP Server を活用して開発ワークフローを拡張する
- Cloud Agent で日常的なタスクを自動化する
- Copilot CLI を日常の開発に組み込む

### リソース

- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [GitHub Copilot ベストプラクティス](https://docs.github.com/copilot/using-github-copilot/best-practices-for-using-github-copilot)
- [Copilot SDK](https://github.com/github/copilot-sdk)
- [Copilot CLI](https://githubnext.com/projects/copilot-cli)
