# Google APIとの通信に使用するモジュールをインポート
from googleapiclient.discovery import build
# ファイルのアップロードをサポートするクラスをインポート
from googleapiclient.http import MediaFileUpload
# OAuth2認証のフローを管理するクラスをインポート
from google_auth_oauthlib.flow import InstalledAppFlow

# YouTube APIのサービス名とバージョンを定義
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
# 認証時に要求する権限のスコープを定義
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
# クライアントの秘密情報が含まれるJSONファイルへのパスを定義
CLIENT_SECRETS_FILE = r"client_secrets.json"

# 認証関数を定義
def authenticate():
    # OAuth2認証のフローを管理
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # ローカルサーバーを使用して認証情報を取得
    credentials = flow.run_local_server(port=0)
    # 認証情報を使用してAPIサービスを構築
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)


# ビデオアップロード関数を定義
def upload_video(youtube, file_path, title, description, category, privacyStatus):
    # アップロードリクエストを作成
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category
            },
            "status": {
                "privacyStatus": privacyStatus
            }
        },
        # メディアファイルとしてアップロード
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if 'id' in response:
            print(f"Video id '{response['id']}' was successfully uploaded.")
        else:
            print("The upload failed with an unexpected response:", response)


# メイン部分
if __name__ == "__main__":
    # 以下は変数の例であり、実際には適切な値を設定する必要があります
    file_path = "path/to/video.mp4"
    title = "Test Title"
    description = "Test Description"
    category = "1"  # YouTubeの公式カテゴリリストから選択
    privacyStatus = "private"  # または "private" または "unlisted"

    # YouTube APIサービスを認証
    youtube = authenticate()
    # ビデオをアップロード
    upload_video(youtube, file_path, title, description, category, privacyStatus)
