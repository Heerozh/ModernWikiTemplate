# ModernWiki

Gitリポジトリをデータベースとして使用し、Markdownをフォーマット言語とするミニマリストWikiシステム。

Wikiの本質はバージョン管理とオープンソースコラボレーションであり、成熟したGitを使用することで悪意のある破壊行為の問題をより適切に管理でき、Markdownも編集が容易です。

## クイックスタート

## 1. コンテンツリポジトリの作成

コンテンツリポジトリはWikiのページリポジトリであり、ユーザーが自由に編集できるように提供されます。[ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git) リポジトリをテンプレートとして使用してください。このリポジトリはHugoプロジェクト形式であり、ウェブサイトのスタイルを自由に変更できます。

### **GitHub:**

[ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git) を直接Forkします。
Gitee、GitLabもサポートしています。

### **（推奨）プライベートGitリポジトリ:**

まずはスキップし、システム起動後に戻って設定します：

<http://localhost/git> にアクセスし、直接「Install Gitea（今すぐインストール）」をクリックし、Adminアカウントを登録します。右上の ➕ をクリックし、「migrate（外部リポジトリを移行）」を選択し、
<https://github.com/Heerozh/ModernWikiTemplate.git> をクローンし、
名前をWikiに変更します。

> リポジトリの権限は全員がPushできるように開く必要があります。そうでない場合はRP審査が必要です。ContentディレクトリのみPush可能にし、サイト設定やスタイルファイルはPRが必要にしたい場合は、Gitサブモジュールを使用し、2つの異なるリポジトリで実現できます。

## 2. 環境変数の設定

環境変数テンプレートをコピー：

```bash
cp .env.example .env
```

`.env` ファイルを編集し、Gitリポジトリを設定：

```bash
GIT_REPO=https:/domain.com/your-username/your-wiki-content.git
GIT_BRANCH=master
DOMAIN=:80 # ローカルテストでは:80のみ使用可能、そうでないとアクセスできません
```

> [!NOTE]
> `.env` を変更するたびに、イメージを再構築する必要があります：`docker compose build`

## 3. システムの起動

まずDocker Engineとdocker-compose-pluginをインストールし、次に：

```bash
# サービスを起動（サードパーティGitホスティング）
docker compose up -d

# サービスを起動（ローカル自建Giteaホスティング）
docker compose --profile with-gitea up -d
```

## 4. Wikiへのアクセス

- メインサイト：<http://localhost>
- Webhookエンドポイント：<http://localhost/webhook>
- Giteaローカルリポジトリ（有効化した場合）：<http://localhost/git/>

## 5. 自動更新の設定

GitHubを例に、Push時にWebhookをトリガーする設定：

1. GitHubリポジトリの設定に移動
2. "Webhooks" オプションをクリック
3. "Add Webhook" をクリック
4. 設定を入力：
   - **Payload URL**: `http://your-domain.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: ランダムなパスワードを入力
   - **Which events**: "Just the push event" を選択

Gitリポジトリの内容が更新されると、このWebhookがHugoのウェブサイト再構築をトリガーします。

Gitea、Gitee（WebHookパスワードモードのみ）、GitLabも同様にサポートしています。

## システムアーキテクチャ解析

ModernWikiは複数のDockerコンテナで構成され、軽量システムを採用し、メモリ使用量はわずか130Mです：

### 1. サイト更新コンテナ (hugo-builder)

- 公開Gitリポジトリをプルし、Hugoを使用して静的ウェブページを生成
- 共有の `site` ディレクトリに出力
- ワンショットコンテナ、実行後終了。

### 2. 静的サイトコンテナ (static-site)

- `site` ディレクトリ内の静的ファイルを継続的にサービス提供

### 3. Webhookコントローラーコンテナ (webhook)

- git push時のwebhookリクエストを継続的に受信
- 受信後、Docker APIを通じてhugo-builderを再起動

### 4. コメントサーバー

- artalk

### 5. オプション：Giteaコンテナ (gitea)

- オプションコンテナ、自建Gitウェブホスティング用
- Giteaのデータは `data/gitea` ディレクトリに保存され、バックアップが必要

### 6. エントリーリバースプロキシコンテナ (proxy)

- 80ポートをリスニングし、エントリーポイントとして機能
- ルーティングルール：
  - `/` → 静的サイトコンテナ
  - `/webhook` → Webhookコンテナ
  - 追加のCaddyfileサイト設定のインポートをサポート

## 開発とデバッグ

### アップグレード

まず本リポジトリを更新し、次にdocker再構築を実行すると、すべてのイメージとソフトウェアが最新版にアップグレードされます。

```bash
git pull
docker compose build --pull
```

### ログの確認

```bash
# すべてのサービスのログを確認
docker compose logs -f

# 特定サービスのログを確認
docker compose logs -f hugo-builder
docker compose logs -f static-site
docker compose logs -f webhook
docker compose logs -f proxy
```

### 手動でのサイト再構築

```bash
docker compose restart hugo-builder
```

## 本番環境デプロイ

このWikiシステムはリポジトリ更新時のみ構築を行い、通常は静的ファイルサービスを提供するため、パフォーマンスオーバーヘッドは非常に低いです。そのため、バーストパフォーマンスインスタンスで十分です（**価格-50%**）。

### 1. ドメイン名の使用

`.evn` を編集し、`DOMAIN=` をあなたのドメイン名に設定します。

### 2. HTTPSサポート

設定不要、システムは自動的かつ定期的にあなたのドメイン名に対してLet's EncryptまたはZeroSSLの無料証明書を申請します。以下を確認してください：

- ドメイン名のDNSがあなたのサーバーを指していること
- ファイアウォールのポート80と443が外部に開放されていること

## Serverlessデプロイ方法 （TODO）

これは最も低コストなデプロイ方法ですが、デプロイが煩雑で機能が少ないため、参考までに紹介します。

- サードパーティホスティングリポジトリを使用
- 関数計算FCを利用し、HttpトリガーでWebhookを受信、hugo-builderコンテナを起動し、OSSストレージに出力
- OSSで静的ウェブサイトホスティングを有効化し、ドメイン名を設定
- 別の関数計算FCを設定し、毎月定期的にトリガーされ、SSL証明書を更新してOSSにアップロード

## ライセンス

MIT License
