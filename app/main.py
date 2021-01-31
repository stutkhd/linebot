from flask import Flask, request, abort

from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage,
)

import os

app = Flask(__name__)

CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# インスタンス作成
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
   # リクエストヘッダーから署名検証のための値を取得
   signature = request.headers['X-Line-Signature']
   # リクエストボディを取得?
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)
   # handle webhook body
   try:
       # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
       # @handler.add or defaultによって追加されたハンドラでWebhookを処理する -> 署名が一致しない場合はInvalid...errorが発生
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'

# イベントごとに関数を設定
# イベントがMessageEnventのインスタンスであり、event.messageがTextMessageのインスタンスである場合、このハンドラーメソッドが呼び出される
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=event.message.text)
    )
if __name__ == "__main__":
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)