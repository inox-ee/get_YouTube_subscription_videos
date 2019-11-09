# YouTube Data API v3 を使って Python(CLI)から登録チャンネルの一覧を取得する

## YouTube Data API v3 を使うための前準備

1. Google アカウントを作成する
2. Google Cloud Platform で新しいプロジェクトを作成する
3. API の利用登録を行う。(ここで躓いた)
   1. 頑張って「API とサービス > 認証情報」にたどり着く。
   2. 「認証情報を作成」から「**ウィザードで選択**」を押す(その他からは正しい JSON が得られない or 設定が不明瞭)。
   3. 使用する API を「YouTube Data API v3」に、API を呼び出す場所を「その他の UI(Windows、CLI ツールなど)」に、アクセスする場所を「ユーザデータ」に。
   4. 出力される JSON を保存

今回はとりあえず CLI から API を叩くだけなので、_client-secret.json_ は以下のようになるはず。

```json
{
  "installed": {
    "client_id": "YOUR-CLIENT-ID.apps.googleusercontent.com",
    "project_id": "YOUR-PROJECT-ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "CLIENT-SECRET",
    "redirect_uris": "REDIRECT-URIS"
  }
}
```
