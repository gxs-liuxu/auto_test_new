from ctypes import windll
import win32con
import win32api
import time

key_map = {
    "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90
}


def key_down(key):
    """121
    函数功能：按下按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), 0, 0)


def key_up(key):
    """
    函数功能：抬起按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)


def key_press(key, wait_time = 0.01):
    """
    函数功能：点击按键（按下并抬起）
    参    数：key:按键值
    """
    key_down(key)
    time.sleep(0.02)
    key_up(key)
    time.sleep(wait_time)


def mouse_click(abscissa, ordinate):
    '''
    函数功能：指定横坐标和纵坐标，单击鼠标左键
    '''
    windll.user32.SetCursorPos(abscissa, ordinate)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, abscissa, ordinate)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, abscissa, ordinate)


def main():
    position_list = [
        (20, 1024)
    ]

    key_set = ['1','2']

    time.sleep(3)
    while(1):
        # for i in key_set:
        #     for j in position_list:
        #         time.sleep(0.2)
        #         mouse_click(j[0], j[1])
        #         key_press(i)
        for i in key_set:
            time.sleep(0.5)
            key_press(i)
# width = windll.user32.GetSystemMetrics(0)
# height = windll.user32.GetSystemMetrics(1)
# print(width, height)



if __name__ == "__main__":
    main()


