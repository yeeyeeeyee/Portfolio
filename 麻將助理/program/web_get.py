from selenium import webdriver
from selenium.webdriver.common.by import By
import re
TRANSDICT = {
    "1z": "東",
    "2z": "南",
    "3z": "西",
    "4z": "北",
    "5z": "白",
    "6z": "發",
    "7z": "中",
    "m": "萬",
    "p": "筒",
    "s": "索"
}

def get_solution(url:str):
   # 建立 ChromeOptions 物件
    options = webdriver.ChromeOptions()
    # 添加參數到 ChromeOptions
    options.add_argument("--enable-chrome-browser-cloud-management") # 讓程序不會卡住
    options.add_argument("--no-sandbox")
    options.add_argument("--headless") # 背景運行
    options.add_argument('--log-level=1') # "Error with Permissions-Policy header: Unrecognized feature: 'ch-ua-form-factor'.",

    # 使用已設定的 options
    browser = webdriver.Chrome(options=options)
    try:
        browser.get(f'https://tenhou.net/2/?q={url}')
        solution = browser.find_element(By.XPATH, "//*[@id='m2']/textarea")
        win = browser.find_element(By.XPATH, "//*[@id='tehai']").text
        Convert = parse_sample(solution.text)
        Convert = "".join([f"打:{discard_translated}  ,摸:{tiles_translated}  ,進張數共:{count}枚\n" for discard_translated,tiles_translated,count in Convert])
        #print(f'solution.text:{solution.text}')
        #print(Convert)
        #print(win)
        return Convert, win
    
    except Exception as e:
        print("error")
        print(e)
        if browser:
            browser.quit()

 
def translate_tile(tile):
    if len(tile) == 2:
        num, char = tile[0], tile[1]
        if char == 'z':
            return TRANSDICT.get(tile, tile)
        return f"{num}{TRANSDICT.get(char, char)}"
    return tile

def translate_tiles(tiles_str):
    tiles = re.findall(r'\d[a-z]', tiles_str)
    translated_tiles = ''.join([f"{translate_tile(tile)} " for tile in tiles])
    return translated_tiles

def parse_sample1(sample):
    lines = sample.strip().split('\n')
    if not lines:
        return []
    actions = []

    for line in lines[1:]:
        if not line.strip():
            continue
        discard_match = re.search(r'打([0-9a-z]+)', line)
        draw_match = re.search(r'摸\[(.*?) (\d+)枚\]', line)
        if discard_match and draw_match:
            discard = discard_match.group(1)
            tiles, count = draw_match.groups()
            discard_translated = translate_tile(discard)
            tiles_translated = translate_tiles(tiles)
            actions.append([discard_translated, tiles_translated, count])

    return actions

def parse_sample2(sample):
    lines = sample.strip().split('\n')
    if not lines:
        return []
    actions = []

    for line in lines[1:]:
        if not line.strip():
            continue
        discard_match = re.search(r'打([0-9a-z]+)', line)
        wait_match = re.search(r'待ち\[(.*?) (\d+)枚\]', line)
        if discard_match and wait_match:
            discard = discard_match.group(1)
            wait, count = wait_match.groups()
            discard_translated = translate_tile(discard)
            wait_translated = translate_tiles(wait)
            actions.append([discard_translated, wait_translated, count])

    return actions

def parse_sample(sample):
    if "摸" in sample:
        return parse_sample1(sample)
    elif "待ち" in sample:
        return parse_sample2(sample)
    else:
        return []


   


if __name__ == '__main__':
    #get_solution("0m6z6z1z2z2z2m9s2m9s5m6m6m8s1m")
    output = get_solution("7m8m1p6p4s9s2z6m")
    print(output)
