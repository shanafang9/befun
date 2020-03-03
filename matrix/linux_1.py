# linux 终端运行
import os
import random
import time
import threading


arr = [0,1,' ']
alpha = 'abcdefghijklmnopqrstuvwxyz'
column = 80                             # 列数
lines = 24                              # 行数
picture = []                            # 画面

def init():
    pass
    # os.system('\033[1;31m<!')
    # os.system('clear')

def play(arr):
    init()
    while True:
        draw(arr)
        time.sleep(0.08)
        # os.system('clear')

def draw(arr):
    produceline(arr)
    for i in picture:
        print("\033[1;31m<!",i)

def produceline(arr):
    newline = ''
    global picture
    for i in range(column//4):
        newline = newline + str(random.choice(arr)) + '    '
    picture.insert(0, newline)
    picture = picture[:lines]


if __name__ == '__main__':
    t = threading.Thread(target=play, args=(arr,))
    t.start()
    t.join()