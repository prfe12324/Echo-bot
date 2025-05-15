from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
import json
from linebot.v3.messaging import (
    FlexBox,
    FlexMessage,
    FlexBubble,
    FlexImage,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
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
    user_id = event.source.user_id
    user_text = event.message.text
    with open("user_messages_log.txt", "a", encoding="utf-8") as f:
        f.write(f"User ID: {user_id} - Message: {user_text}\n")

    # === [2] 回覆功能（原本的邏輯） ===
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
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
        
        elif text == '課程':
            line_flex_json = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://i.imgur.com/8KotKuq.jpeg",
    "size": "full",
    "aspectRatio": "4:3",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "阿嬤的春捲課程",
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "icon",
            "size": "sm",
            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
          },
          {
            "type": "text",
            "text": "5.0",
            "size": "sm",
            "color": "#999999",
            "margin": "md",
            "flex": 0
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "地址",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "高雄市湖內區活動中心",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "時間",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "10:00 - 13:30",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "spacing": "sm",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "uri": "https://www.google.com/",
              "label": "GOOGLE"
            },
            "style": "primary"
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "FB",
              "uri": "https://www.facebook.com/"
            },
            "style": "secondary"
          }
        ],
        "margin": "sm"
      }
    ],
    "flex": 0
  }
}
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='詳細說明', contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        # Buttons Template
        elif text == 'Buttons':
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http:", "https:")
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
            url = url.replace("http:", "https:")
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
            url = url.replace("http:", "https:")
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
                    QuickReplyItem(action=MessageAction(label="打招呼", text="嗨")),
                    QuickReplyItem(action=LocationAction(label="傳送位置")),
                    QuickReplyItem(action=CameraAction(label="開啟相機"))
                ])
            )
            line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[reply]))



        # 音訊、貼圖、位置 (測試回傳)
        elif text == '音訊':
            url = request.url_root + 'static/music.mp3'
            url = url.replace("http:", "https:")
            audio = AudioMessage(original_content_url=url, duration=10000)
            line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[audio]))

        elif text == '貼圖':
            sticker = StickerMessage(package_id='446', sticker_id='1988')
            line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[sticker]))
        elif text == '位置':
            location = LocationMessage(title='台北車站', address='台北市中正區忠孝西路一段49號', latitude=25.0478, longitude=121.5170)
            line_bot_api.reply_message(ReplyMessageRequest(reply_token=event.reply_token, messages=[location]))

if __name__ == "__main__":
    app.run()