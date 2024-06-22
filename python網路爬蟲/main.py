from flask import Flask, request, abort
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, CarouselContainer, BubbleContainer, ImageComponent, BoxComponent, TextComponent, ButtonComponent, URIAction
import requests
import re
import logging

app = Flask(__name__)
app.config['DEBUG'] = True  # 啟用 Debug 模式

# Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('Channel Access Token')
handler = WebhookHandler('Channel Secret')

# 保存用戶輸入
user_data = {}

# 日誌設定
logging.basicConfig(level=logging.INFO)

def shorten_url(url: str) -> str:
    """
    縮短連接飯店資訊的網址
    """
    try:
        api_url = f'http://tinyurl.com/api-create.php?url={url}'
        response = requests.get(api_url)
        response.raise_for_status()  # 檢查 HTTP 狀態碼
        return response.text
    except requests.RequestException as e:
        app.logger.error(f"Shorten URL failed: {e}")
        return url

def get_url(position, start_date, end_date):
    """
    依據 User 的資料調取URL
    """
    from selenium.webdriver.common.keys import Keys
    import time
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-chrome-browser-cloud-management")
    # 背景運行
    # options.add_argument("--headless")
    url = "https://www.trivago.com.tw/zh-Hant-TW"
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(10)
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    input_element = browser.find_element(By.CSS_SELECTOR, '[data-testid="search-form-destination"]')
    input_element.clear()
    input_element.send_keys(position)
    input_element.send_keys(Keys.RETURN)
    time.sleep(1)

    submit = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/section[1]/div[2]/div[4]/div/button/span/span')
    submit.click()
    time.sleep(1)
    submit.click()
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="accommodation-list-element"]')))
        now_url = browser.current_url
        return f"{now_url};dr-{start_date}-{end_date};"
    except Exception as e:
        app.logger.error(f"URL generation failed: {e}")
        return "輸入錯誤"
    finally:
        browser.quit()

def get_browser(url: str) -> list:
    """
    使用 get_url() 提供 URL 去爬飯店資訊
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-chrome-browser-cloud-management")
    # 背景運行
    # options.add_argument("--headless")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(10)
    browser.get(url)
    detail = []
    max_items = 12  # 輪播訊息最多12筆資料
    item_count = 0

    wait = WebDriverWait(browser, 10)
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="accommodation-list-element"]')))
        hotels = browser.find_elements(By.CSS_SELECTOR, '[data-testid="accommodation-list-element"]')
        if browser.find_element(By.CSS_SELECTOR, '[data-testid="calendar-button-close"]'):
            browser.find_element(By.CSS_SELECTOR, '[data-testid="calendar-button-close"]').click()

        for hotel in hotels:
            if item_count >= max_items:
                break
            hotel_name = hotel.find_element(By.TAG_NAME, 'h2').text
            try:
                check = hotel.find_element(By.CSS_SELECTOR, '[data-testid="cheapest-price-label"]').text
                if check == "其他價格":
                    hotel_price = hotel.find_element(By.CSS_SELECTOR, '[data-testid="recommended-price"]').text
                else:
                    hotel_price = hotel.find_element(By.CSS_SELECTOR, '[data-testid="more-deals"]').text
                    hotel_price = re.search(r"\$\d+(?:,\d{3})*", hotel_price).group()
            except Exception as e:
                app.logger.error(f"Price extraction failed: {e}")
                hotel_price = "無價格資訊"

            hotel_score = hotel.find_element(By.CSS_SELECTOR, "span[itemprop='ratingValue']").text
            hotel_img = hotel.find_element(By.CSS_SELECTOR, '[data-testid="accommodation-main-image"]').get_attribute('src')
            button = hotel.find_element(By.CSS_SELECTOR, '[data-testid="champion-deal"]')
            browser.execute_script("arguments[0].click();", button)
            window_handles = browser.window_handles
            browser.switch_to.window(window_handles[-1])
            new_url = browser.current_url
            browser.close()
            browser.switch_to.window(window_handles[0])
            short_url = shorten_url(new_url)
            detail.append([hotel_name, hotel_price, hotel_score, hotel_img, short_url])
            item_count += 1

    except Exception as e:
        app.logger.error(f"Error occurred while fetching hotel details: {e}")

    finally:
        browser.quit()
    return detail

def format_for_linebot(details: list[list[str, str, str, str]]) -> list[FlexSendMessage]:
    """
    飯店資料格式化
    """
    bubbles = []
    for detail in details:
        hotel_name, hotel_price, hotel_score, hotel_img, short_url = detail
        
        bubble = BubbleContainer(
            header=BoxComponent( # 設置文字的粗細、大小
                layout='vertical',
                contents=[
                    TextComponent(text=hotel_name, weight='bold', size='xl')
                ]
            ),
            hero=ImageComponent( # 設置圖片大小、寬高和顯示模式
                url=hotel_img,
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover'
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text=f"最低價錢: {hotel_price}", size='md'),
                    TextComponent(text=f"評分: {hotel_score}", size='md')
                ]
            ),
            footer=BoxComponent( # 設置按鈕樣式、高度和行為
                layout='vertical',
                contents=[
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='查看詳細資訊', uri=short_url)
                    )
                ]
            )
        )
        
        bubbles.append(bubble)

    if len(bubbles) > 12:
        bubbles = bubbles[:12]

    carousel = CarouselContainer(contents=bubbles)
    return [FlexSendMessage(alt_text="飯店資訊", contents=carousel)]


@app.route("/callback", methods=['POST'])
def callback():
    """
    處理來自 Line 的回調請求
    """
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    if user_message.lower() == "開始搜尋":
        user_data[user_id] = {}
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請提供目的地：")
        )
    elif "destination" not in user_data[user_id]:
        user_data[user_id]['destination'] = user_message.strip()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請提供入住日期： \n(格式：YYYYMMDD)")
        )
    elif "check_in_date" not in user_data[user_id]:
        user_data[user_id]['check_in_date'] = user_message.strip()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請提供退房日期： \n(格式：YYYYMMDD)")
        )
    else:
        user_data[user_id]['check_out_date'] = user_message.strip()
        destination = user_data[user_id]['destination']
        check_in_date = user_data[user_id]['check_in_date']
        check_out_date = user_data[user_id]['check_out_date']

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="資料讀取中，請稍後")
        )

        search_url = get_url(destination, check_in_date, check_out_date)
        if "輸入錯誤" in search_url:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無法生成搜索網址，請檢查輸入資訊。")
            )
            return

        details = get_browser(search_url)
        if not details:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無法獲取酒店資訊，請稍後再試。")
            )
            return

        messages = format_for_linebot(details)
        try:
            for message in messages:
                line_bot_api.push_message(user_id, message)
        except LineBotApiError as e:
            app.logger.error(f"Error sending message: {e}")
            line_bot_api.push_message(user_id, TextSendMessage(text="無法發送酒店資訊，請稍後再試。"))

if __name__ == "__main__":
    app.run(port=8000, debug = False)
