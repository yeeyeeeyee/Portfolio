import cv2
import numpy as np
import pyautogui

# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()

# 捕获桌面屏幕截图
screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))

# 将 PIL 图像转换为 OpenCV 格式
screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# 显示截图
cv2.imshow("Screenshot", screenshot_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()
