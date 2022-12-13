import time
import serial
import threading
from collections import Counter
import numpy as np
from scipy import signal
from tensorflow import keras
import pygame as pg
import random
from math import *
from pygame import event
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame.math import *
from os import getcwd

pg.font.init()
WINDOW_SIZE = (720, 480)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BOOK1 = [getcwd().replace('\\', '/') + '/books/book_test-000{}.jpg'.format(i) for i in range(10)] + [getcwd().replace('\\', '/') + '/books/book_test-0010.jpg']
BOOK2 = [getcwd().replace('\\', '/') + '/books/book_test2-000{}.jpg'.format(i) for i in range(10)] + [getcwd().replace('\\', '/') + '/books/book_test2-0010.jpg']
HAND = [getcwd().replace('\\', '/') + '/paper.png', getcwd().replace('\\', '/') + '/rock.png', getcwd().replace('\\', '/') + '/scissor.png']
BOOK = getcwd().replace('\\', '/') + '/book1.png'

score_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", 20)
title_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", 40)
pivot = (360 , 450)                                                                     
btn_preview = 1
preview_color = (124, 252, 0)
mode = 0

class Hand(pg.sprite.Sprite):
    def __init__(self, img, center):
        super().__init__()
        self.center = center
        self.image = pg.image.load(img).convert_alpha()
        self.image = pg.transform.scale(self.image, (200, 200))
        self.org_image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def change(self, i):
        self.image = pg.image.load(HAND[i]).convert_alpha()
        self.image = pg.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = self.center

class Book(pg.sprite.Sprite):    
    def __init__(self, img, center):
        super().__init__()
        self.center = center
        self.image = pg.image.load(img).convert_alpha()
        self.image = pg.transform.scale(self.image, screen.get_size())
        self.org_image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def next_page(self, i):
        self.image = pg.image.load(BOOK1[i]).convert_alpha()
        self.image = pg.transform.scale(self.image, screen.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def prev_page(self, i):
        self.image = pg.image.load(BOOK2[i]).convert_alpha()
        self.image = pg.transform.scale(self.image, screen.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = self.center

def start(LIST):
    # 建立畫布bg
    global screen, WINDOW_SIZE, run, btn_preview, mode
    bg1 = pg.Surface(screen.get_size())
    bg1 = bg1.convert()
    bg1.fill(WHITE)

    screen.blit(bg1, (0,0))
    pg.display.update()
    count_d = 0
    count_u = 0
    counter = 0
    # state = 0
    while run:
        counter += 1
        time.sleep(0.001)
        out = Counter(LIST).most_common(1)
        # print("show: ",gestures[out[0][0]])
        gesture = out[0][0]
        print(gesture)

        bg1 = pg.Surface(screen.get_size())
        bg1 = bg1.convert()
        bg1.fill(WHITE)
        BTN_mode1 = pg.Rect(WINDOW_SIZE[0]/5, WINDOW_SIZE[1]/4, WINDOW_SIZE[0]*3/5, WINDOW_SIZE[1]/8)                 
        BTN_mode2 = pg.Rect(WINDOW_SIZE[0]/5, WINDOW_SIZE[1]/2.5, WINDOW_SIZE[0]*3/5, WINDOW_SIZE[1]/8)
        BTN_mode3 = pg.Rect(WINDOW_SIZE[0]/5, WINDOW_SIZE[1]/1.8, WINDOW_SIZE[0]*3/5, WINDOW_SIZE[1]/8)                               
        pg.draw.rect(bg1, BLUE, BTN_mode1, 4)
        pg.draw.rect(bg1, BLUE, BTN_mode2, 4)
        pg.draw.rect(bg1, BLUE, BTN_mode3, 4)
        screen.blit(bg1, (0,0))
        game_name = title_font.render('Bio Exp', True, (0, 0, 0))  # 大小需要調整

        book_mode = title_font.render('Book', True, (0, 0, 0))
        picture_mode = title_font.render('Picture', True, (0, 0, 0))
        game_mode = title_font.render('Game', True, (0, 0, 0))

        # screen.blit(game_name, (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/8))
        screen.blit(book_mode, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/4))
        screen.blit(picture_mode, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/2.5))
        screen.blit(game_mode, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/1.8))

        if btn_preview == 1:
            pg.draw.rect(screen, preview_color, BTN_mode1, 10)
        elif btn_preview == 2:
            pg.draw.rect(screen, preview_color, BTN_mode2, 10)
        elif btn_preview == 3:
            pg.draw.rect(screen, preview_color, BTN_mode3, 10)
        
        if gesture == 5:            # Down
            count_d += 1
            # btn_preview = 3 if btn_preview == 3 else btn_preview + 1
        elif gesture == 4:          # Up
            count_u += 1
            # btn_preview = 1 if btn_preview == 1 else btn_preview - 1
        elif gesture == 8:          # Thumbsup
            mode = btn_preview
            return

        if count_d > 100:
            btn_preview = 3 if btn_preview == 3 else btn_preview + 1
            count_d = 0
            count_u = 0
            counter = 0
        if count_u > 100:
            btn_preview = 1 if btn_preview == 1 else btn_preview - 1
            count_d = 0
            count_u = 0
            counter = 0
        if counter > 500:
            count_d = 0
            count_u = 0
            counter = 0

        pg.display.update()
        for event in pg.event.get():
            if event.type == KEYDOWN:           # 觸發關閉視窗
                if event.key == K_ESCAPE:
                    run = False
                elif event.key == pg.K_DOWN:
                    btn_preview = 3 if btn_preview == 3 else btn_preview + 1
                elif event.key == pg.K_UP:
                    btn_preview = 1 if btn_preview == 1 else btn_preview - 1
                elif event.key == pg.K_RIGHT:
                    mode = btn_preview
                    return
                
            elif event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:  
                if event.button == 1 and BTN_mode1.collidepoint(event.pos):
                    mode = 1
                    return
                elif event.button == 1 and BTN_mode2.collidepoint(event.pos):
                    mode = 2
                    return
                elif event.button == 1 and BTN_mode3.collidepoint(event.pos):
                    mode = 3
                    return
            elif event.type == pg.VIDEORESIZE:
                WINDOW_SIZE = event.size
                screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)

def mode1(LIST):  
    global run, screen, WINDOW_SIZE, pivot, Start_loc, all_sprites, mode
    bg2 = pg.Surface(screen.get_size())
    bg2 = bg2.convert()
    bg2.fill(WHITE)

    clock = pg.time.Clock()
    # 書
    book1 = Book(BOOK1[0], (int(WINDOW_SIZE[0] /2) , int(WINDOW_SIZE[1]/2)))
    screen.blit(bg2, (0,0))
    pg.display.update()
    # 清空物件
    all_sprites.empty()
    all_sprites.add(book1)
    state = 0
    i = 0

    while run:
        time.sleep(0.001)
        out = Counter(LIST).most_common(1)
        gesture = out[0][0]
        #print(gesture)
        # print(state)
        if state == 0:
            if gesture == 7:            
                print("next page")
                state = 1
            elif gesture == 6:          
                print("previous page")
                state = 2
            elif gesture == 9:       # Double tap
                mode = 0
                print("Quit!")
                return

        for event in pg.event.get():
            if event.type == KEYDOWN:           # 觸發關閉視窗
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False
            elif event.type == pg.VIDEORESIZE:
                WINDOW_SIZE = event.size
                screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    print("next page")
                    state = 1
                if event.key == pg.K_LEFT:
                    print("prev page")
                    state = 2
                    # Back
                if event.key == pg.K_DOWN:
                    mode = 0
                    return

        if state == 1:
            if i < len(BOOK1):
                book1.next_page(i)
                i += 1
            else:
                i = 0
                state = 0
        elif state == 2:
            if i < len(BOOK2):
                book1.prev_page(i)
                i += 1
            else:
                i = 0
                state = 0
        
        screen.fill(WHITE)
        all_sprites.draw(screen)                             # 全部畫出來
        # 正式渲染
        pg.display.update()
        clock.tick(10)

def mode2(LIST):
    from PIL import Image
    # from pykeyboard import PyKeyboard
    import keyboard
    # import sys
    # import subprocess
    global run, screen, WINDOW_SIZE, pivot, Start_loc, all_sprites, mode
    # k = PyKeyboard()

    image = Image.open('002.jpg')
    image.show()
    # imageViewerFromCommandLine = {'linux':'xdg-open',
    #                               'win32':'explorer',
    #                               'darwin':'open'}[sys.platform]
    # print(imageViewerFromCommandLine)
    # pro = subprocess.run([imageViewerFromCommandLine, "002.jpg"])
    # subprocess.run([imageViewerFromCommandLine, 'book1.png'])
    mode = 0
    zoom = 0
    count = 0
    while run:
        count += 1
        # Reset
        if count > 1000:
            count = 0
            zoom = 0
            
        time.sleep(0.001)
        out = Counter(LIST).most_common(1)
        gesture = out[0][0]

        if zoom == 1:
            if gesture == 3:          # stone + paper   
                print("Zoom in")
                keyboard.press_and_release("ctrl+add")
                keyboard.press_and_release("ctrl+add")
                keyboard.press_and_release("ctrl+add")
                # k.press_keys([k.control_key, k.keypad_keys["Add"]])
                # k.press_keys([k.control_key, k.keypad_keys["Add"]]) 
                zoom = 0
        elif zoom == 2:               # paper + stone
            if gesture == 2:            
                print("Zoom out")
                keyboard.press_and_release("ctrl+subtract")
                keyboard.press_and_release("ctrl+subtract")
                keyboard.press_and_release("ctrl+subtract")
                # k.press_keys([k.control_key, k.keypad_keys["Subtract"]])
                # k.press_keys([k.control_key, k.keypad_keys["Subtract"]])
                zoom = 0
        else:
            if gesture == 2:          # stone
                zoom = 1
            if gesture == 3:          # paper
                zoom = 2

        if gesture == 9:              # Double tap
            mode = 0
            print("Quit!")
            return
        # if keyboard.read_key() == "p":
        #     print("You pressed p")
        #     keyboard.press_and_release("ctrl+add")
        #     keyboard.press_and_release("ctrl+add")
        #     keyboard.press_and_release("ctrl+add")
        #     # k.press_keys([k.control_key, k.keypad_keys["Add"]])
        #     # k.press_keys([k.control_key, k.keypad_keys["Add"]])     
        #     # image.close()
        #     # break
        # if keyboard.read_key() == "o":
        #     print("You pressed o")
        #     keyboard.press_and_release("ctrl+subtract")
        #     keyboard.press_and_release("ctrl+subtract")
        #     keyboard.press_and_release("ctrl+subtract")
        #     # k.press_keys([k.control_key, k.keypad_keys["Subtract"]])
        #     # k.press_keys([k.control_key, k.keypad_keys["Subtract"]])  
        # if keyboard.read_key() == "q":
        #     print("You pressed q")
        #     # pro.kill()
        #     mode = 0
        #     break
        #     # for proc in psutil.process_iter():
        #     #     print(proc.name())
        #     #     if proc.name() == "explorer.exe":
        #     #         proc.kill()
    mode = 0
    # return

def mode3(LIST):
    # 遊戲bg
    global run, screen, WINDOW_SIZE, pivot, Start_loc, all_sprites, mode
    bg2 = pg.Surface(screen.get_size())
    bg2 = bg2.convert()
    bg2.fill(WHITE)

    clock = pg.time.Clock()
    player = Hand(HAND[1], (int(WINDOW_SIZE[0] /2) , int(WINDOW_SIZE[1]*3/4)))  # (x, y)
    opponent = Hand(HAND[1], (int(WINDOW_SIZE[0] /2) , int(WINDOW_SIZE[1]/4)))
    screen.blit(bg2, (0,0))
    pg.display.update()
    # 清空物件
    all_sprites.empty()
    all_sprites.add(player)
    all_sprites.add(opponent)
    state = 0
    throw = False
    i = 1
    win = 0
    lose = 0
    count_p = 0
    count_st = 0
    count_sc = 0
    #all_sprites.add()

    while run:
        time.sleep(0.001)
        out = Counter(LIST).most_common(1)
        gesture = out[0][0]
        print(gesture)

        if gesture == 3:  
            count_p += 1          
            # print("paper!")
            # i = 0
            # throw = True
        elif gesture == 2:  
            count_st += 1        
            # print("stone!")
            # i = 1
            # throw = True
        elif gesture == 1:
            count_sc += 1
            # print("scissor!")
            # i = 2
            # throw = True
        elif gesture == 9:       # Double tap
            mode = 0
            print("Quit!")
            return

        if count_p > 3:            
            print("paper!")
            i = 0
            throw = True
        elif count_st > 3:          
            print("stone!")
            i = 1
            throw = True
        elif count_sc > 3:
            print("scissor!")
            i = 2
            throw = True

        for event in pg.event.get():
            if event.type == KEYDOWN:           # 觸發關閉視窗
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False
            elif event.type == pg.VIDEORESIZE:
                WINDOW_SIZE = event.size
                screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    print("paper!")
                    i = 0
                    throw = True
                elif event.key == pg.K_DOWN:
                    print("stone!")
                    i = 1
                    throw = True
                elif event.key == pg.K_RIGHT:
                    print("scissor!")
                    i = 2
                    throw = True
                # Back
                elif event.key == pg.K_UP:
                    mode = 0
                    return
        
        if throw:
            num = random.randint(0, 2)
            # print(num)
            opponent.change(num)
            player.change(i)
            # throw = False

            if (i==num):
                print("Tie")
                state = 1
            elif (i == 0 and num ==1) or (i == 1 and num == 2) or (i == 2 and num == 0):
                print("You win!")
                win += 1
                state = 2
            else:
                print("You lose.")
                lose += 1
                state = 3

            
        screen.fill(WHITE)
        all_sprites.draw(screen)                             # 全部畫出
        # 正式渲染
        msg = title_font.render("", True, (0, 0, 0))
        if state == 1:
            msg = title_font.render("It's a tie!", True, (0, 0, 0))
            screen.blit(msg, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/2.3))
        elif state == 2:
            msg = title_font.render('You win!', True, GREEN)
            screen.blit(msg, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/2.3))
        elif state == 3:
            msg = title_font.render('You Lose QQ', True, RED)
            screen.blit(msg, (WINDOW_SIZE[0]/2.8, WINDOW_SIZE[1]/2.3))
        else:
            screen.blit(msg, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/2.3))

        if throw: 
            throw = False
            count_p = 0
            count_sc = 0
            count_st = 0
            time.sleep(1)

        win_counter = score_font.render('Win : '+ str(win), True, (0, 0, 0))
        lose_counter = score_font.render('Lose : '+ str(lose), True, (0, 0, 0))
        screen.blit(win_counter, (WINDOW_SIZE[0]*0.05, WINDOW_SIZE[1]*0.8)) 
        screen.blit(lose_counter, (WINDOW_SIZE[0]*0.05, WINDOW_SIZE[1]*0.9)) 
        pg.display.update()
        clock.tick(6)

def emg_filter(data):
    emg = data[:,2:6]
    fsr = data[:,0:2]
    
    m = np.mean(emg,  axis = 0)
    pemg = emg - m
    l=1000
    
    high = 2*55/l
    low = 2*65/l
    b, a = signal.butter(4, [high,low], btype='bandstop')
    
    pemg = signal.filtfilt(b, a, pemg, axis=0)
    
    high = 2*10/l
    low = 2*450/l
    b, a = signal.butter(4, [high,low], btype='bandpass')
    
    pemg = signal.filtfilt(b, a, pemg, axis=0)
    
    pdata = np.concatenate([fsr, pemg], axis=1)
    
    return pdata


def main(RF, COM_PORT = 'COM7' , BAUD_RATES = 500000, LIST = [0] * 10):

    ser = serial.Serial(COM_PORT, BAUD_RATES)
    
    s = 0
    temp = []
    update = False
    window = 200
    
    
    mode = 0 #0 for emg + fsr ,1 for emg 

    if mode == 1:
        size = 4
    else :
        size = 6
        
    data = np.zeros((3,500,size))
    step = np.zeros((500,size))
    
    model = keras.models.load_model('my_model.h5')
    
    second = time.time()
    

    while RF.is_set():
        
        while ser.in_waiting >= 1 and s < window :
            if ser.read() == b'\r' :
                if ser.read() == b'\n' :                    
                    temp_raw = ser.read(6)
                    temp.append(list(temp_raw))
                    s += 1
                    if s == window :
                        update = True
                        
            #print(s)
                        
        if update == True :    
            temp = np.array(temp)
            step = np.delete(step, slice(window), axis=0)
            step = np.append(step, temp[:,6-size:6], axis=0)
            
            pstep = emg_filter(step) #(500,6)
            
            pstep = np.reshape(pstep, (1,500,size)) 
            
            
            data = np.delete(data, 0 , axis=0)  

            data = np.append(data, pstep, axis=0) #(3,500,6)
             
            
# =============================================================================
#             fig, (plt1, plt2) = plt.subplots(2, 1, figsize=(12,7))
#             plt1.plot(data)
#             plt2.plot(pdata)
#             plt.show()
# =============================================================================
            
            pdata = np.reshape(data, (1,3,500,size)) 

            prediction = model(pdata).numpy()
            gesture = np.argmax(prediction,axis=1)
            
            
            LIST[:-1] = LIST[1:]
            LIST[-1] = gesture[0]
            
            
            print(gestures[gesture[0]])
            
            update = False
            s = 0
            temp = []
            
# =============================================================================
#             print(time.time()-second)
#             second = time.time()
# =============================================================================
            
        
    ser.close()
    print('Model End')

if __name__ == "__main__":
    
    gestures = {0:"rest",
                1:"剪刀",
                2:"石頭",
                3:"布",
                4:"手腕:上",
                5:"手腕:下",
                6:"手腕:內",
                7:"手腕:外",
                8:"大拇指",
                9:"雙點"}

    COM_PORT = 'COM7'    # 指定通訊埠名稱
    BAUD_RATES = 500000    # 設定傳輸速率
    LIST = [0] * 6
    RF = threading.Event()
    
    model_thread = threading.Thread(target = main, args=(RF, COM_PORT, BAUD_RATES, LIST,))
    
    RF.set()
    model_thread.setDaemon(True)
    model_thread.start()

    pg.init()
    pg.display.set_caption('Bioexp')                 # 視窗標題
    screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)
    all_sprites = pg.sprite.Group()                
    run = True

    try:
        while run :
            #print(mode)
            if mode == 0:
                start(LIST)
            elif mode == 1:
                mode1(LIST)
            elif mode == 2:
                mode2(LIST)
            elif mode == 3:
                mode3(LIST)
                
            time.sleep(0.01)

            # show = input("show?")
            # time.sleep(2)
            # out = Counter(LIST).most_common(1)
            # print("show: ",gestures[out[0][0]])
            
    except (KeyboardInterrupt, SystemExit):
        RF.clear()
        model_thread.join()
        print ('KeyboardInterrupt')
        
    finally :
        RF.clear()
        model_thread.join()
        print ('END')
        #quit() 