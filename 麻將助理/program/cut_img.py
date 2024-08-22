import cv2
import numpy as np
import pyautogui

# 從get_screen 改變
def get_screen():
    """
    return cv2 image
    """
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()

    # 计算截图区域的大小
    region_width = screen_width 
    region_height = screen_height // 4

    # 计算截图区域在屏幕中的位置
    start_x = 0
    start_y = (screen_height - region_height) 

    # 捕获桌面屏幕截图
    screenshot = pyautogui.screenshot(region=(start_x, start_y, region_width, region_height))

    # 将 PIL 图像转换为 OpenCV 格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 显示截图
    #cv2.imshow("Screenshot", screenshot_cv)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    return screenshot_cv