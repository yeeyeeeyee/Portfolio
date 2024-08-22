from selenium import webdriver
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
# 添加參數到 ChromeOptions
options.add_argument("--enable-chrome-browser-cloud-management") # 讓程序不會卡住
options.add_argument("--headless") # 背景運行
options.add_argument('--log-level=1') # "Error with Permissions-Policy header: Unrecognized feature: 'ch-ua-form-factor'.",

# 使用已設定的 options
browser = webdriver.Chrome(options=options)
browser.get("https://tw.stock.yahoo.com/quote/0050.TW")
find = browser.find_element(By.XPATH, "//*[@id='qsp-overview-realtime-info']/div[2]/div[2]/div/ul/li[4]/span[2]")
print(find.text)