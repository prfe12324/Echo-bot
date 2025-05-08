from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    StickerMessage,
    LocationMessage,
    AudioMessage,
    QuickReply,
    QuickReplyItem
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    LocationMessageContent,
    StickerMessageContent,
    AudioMessageContent
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, AudioMessage,
    StickerMessage, LocationMessage, QuickReply, QuickReplyButton,
    LocationAction
)
from linebot.v3.messaging import ReplyMessageRequest

import os

app = Flask(__name__)
configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature.")
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # Confirm Template
        if text == 'Confirm':
            confirm_template = ConfirmTemplate(
                text='今天學程式了嗎?',
                actions=[
                    MessageAction(label='是', text='是!'),
                    MessageAction(label='否', text='否!')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Confirm alt text',
                template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

        # Buttons Template
        elif text == 'Buttons':
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http", "https")
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title='示範',
                text='詳細說明',
                actions=[
                    CameraAction(label='拍照'),
                    CameraRollAction(label='選擇相片'),
                    LocationAction(label='選擇位置')
                ]
            )
            template_message = TemplateMessage(
                alt_text="This is a buttons template",
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[template_message])
            )

        # Carousel Template
        elif text == 'Carousel':
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http", "https")
            carousel_template = CarouselTemplate(columns=[
                CarouselColumn(
                    thumbnail_image_url=url,
                    title='第一項',
                    text='這是第一項的描述',
                    actions=[URIAction(label='按我前往 Google', uri='https://www.google.com')]
                ),
                CarouselColumn(
                    thumbnail_image_url=url,
                    title='第二項',
                    text='這是第二項的描述',
                    actions=[URIAction(label='按我前往 Yahoo', uri='https://www.yahoo.com')]
                )
            ])
            carousel_message = TemplateMessage(alt_text='這是 Carousel Template', template=carousel_template)
            line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[carousel_message]))

        # ImageCarousel Template
        elif text == 'ImageCarousel':
            url = request.url_root + 'static/'
            url = url.replace("http", "https")
            image_carousel_template = ImageCarouselTemplate(columns=[
                ImageCarouselColumn(image_url=url+'facebook.png', action=URIAction(label='造訪FB', uri='https://www.facebook.com/NTUEBIGDATAEDU')),
                ImageCarouselColumn(image_url=url+'instagram.png', action=URIAction(label='造訪IG', uri='https://instagram.com/ntue.bigdata')),
                ImageCarouselColumn(image_url=url+'youtube.png', action=URIAction(label='造訪YT', uri='https://www.youtube.com/@bigdatantue'))
            ])
            image_carousel_message = TemplateMessage(alt_text='圖片輪播範本', template=image_carousel_template)
            line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[image_carousel_message]))

        # Quick Reply
        elif text == 'Quick':
            reply = TextMessage(
                text='請選擇：',
                quick_reply=QuickReply(items=[
                    QuickReplyItem(action=MessageAction(label="打招呼", text="您好")),
                    QuickReplyItem(action=LocationAction(label="傳送位置")),
                    QuickReplyItem(action=CameraAction(label="開啟相機"))
                ])
            )
            line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[reply]))

        # 音訊、貼圖、位置 (測試回傳)
        elif text == '音訊':
            audio = AudioMessage(
                original_content_url='https://ffe0-114-33-34-103.ngrok-free.app/static/music.mp3',
                duration=10000
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[audio])
            )

        elif text == '貼圖':
            sticker = StickerMessage(package_id='446', sticker_id='1988')
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[sticker])
            )

        elif text == '位置':
            message = TextSendMessage(
                text='請傳送你目前的位置給我 😊',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=LocationAction(label="傳送位置"))
                    ]
                )
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[message])
            )

        # 處理使用者傳送的位置訊息
        elif isinstance(event.message, LocationMessage):
            address = event.message.address
            latitude = event.message.latitude
            longitude = event.message.longitude

            reply_text = (
                f"你傳送的位置資訊如下：\n"
                f"📍 地址：{address}\n"
                f"🌐 緯度：{latitude}\n"
                f"🌐 經度：{longitude}"
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[TextSendMessage(text=reply_text)])
            )

if __name__ == "__main__":
    app.run()