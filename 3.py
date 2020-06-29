# from tkinter import *
# def call_back(event):
#     # 按哪个键，在console中打印
#     print("现在的位置是", event.x_root, event.y_root)
#
#
# def main():
#     root = Tk()
#
#     # 创建一个框架，在这个框架中响应事件
#     frame = Frame(root,
#                   width=200, height=200,
#                   background='green')
#
#     frame.bind("<Motion>", call_back)
#     frame.pack()
#
#     # 当前框架被选中，意思是键盘触发，只对这个框架有效
#     frame.focus_set()
#
#     mainloop()
#
# if __name__ == '__main__':
#     main()


import  os
import  time
import pyautogui as pag
try:
    while True:
        print("Press Ctrl-C to end")
        screenWidth, screenHeight = pag.size()  #获取屏幕的尺寸
        print(screenWidth,screenHeight)
        ptx,pty = pag.position()   #获取当前鼠标的位置
        showStr = "Position:" + str(ptx).rjust(4)+','+str(pty).rjust(4)
        print(showStr) ###
        time.sleep(0.5)
        os.system('cls')   #清除屏幕
except KeyboardInterrupt:
    print('end....')


