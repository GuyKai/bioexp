# 開始介面 + 連線
# 一般 健身環 mode
import pygame as pg
import random, socket, time
from math import *
from pygame import event
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame.math import *
from os import getcwd


# Todo
# 猜拳
# 撥歌

pg.font.init()
WINDOW_SIZE = (720, 480)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BOOK1 = [getcwd().replace('\\', '/') + '/books/book_test-000{}.jpg'.format(i) for i in range(10)] + [getcwd().replace('\\', '/') + '/books/book_test-0010.jpg']
HAND = [getcwd().replace('\\', '/') + '/paper.png', getcwd().replace('\\', '/') + '/rock.png', getcwd().replace('\\', '/') + '/scissor.png']
BOOK = getcwd().replace('\\', '/') + '/book1.png'

score_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", 20)
title_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", 40)
Start_loc = [[WINDOW_SIZE[0]*i/9 , 10] for i in range(9) ]
pivot = (360 , 450)                                      # 軸心
offset = Vector2((0, 75))                                # 偏移 (武器長度的一半)
btn_preview = 1
preview_color = (124, 252, 0)

# Host = '192.168.137.1'
# Port = 5438
# s = socket.socket()
# s.bind((Host, Port))
# s.listen(5)

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
        # self.image = self.org_image
        #print(self.rect)
        #return rotated_weapon, self.rect

class Interface(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mode = 0
        # self.score = 0
        # self.hp = 3
        # self.image = pg.image.load(img).convert_alpha()
        # self.rect = self.image.get_rect()
    
    def show(self):
        for i in range(self.hp):
            self.rect.x = WINDOW_SIZE[0]*(0.8 + 0.05*i)
            self.rect.y = WINDOW_SIZE[1]*0.9
            screen.blit(self.image, self.rect)
        # text_surface = score_font.render('Score : '+ str(self.score), True, (0, 0, 0))
        # screen.blit(text_surface, (WINDOW_SIZE[0]*0.05, WINDOW_SIZE[1]*0.9))    

    def pause(self):
        pass 

def start(interface):
    # 建立畫布bg
    global screen, WINDOW_SIZE, run, btn_preview
    bg1 = pg.Surface(screen.get_size())
    bg1 = bg1.convert()
    bg1.fill(WHITE)

    screen.blit(bg1, (0,0))
    pg.display.update()
    while run:
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
                    interface.mode = btn_preview
                    return
                
            elif event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:  
                if event.button == 1 and BTN_mode1.collidepoint(event.pos):
                    interface.mode = 1
                    return
                elif event.button == 1 and BTN_mode2.collidepoint(event.pos):
                    interface.mode = 2
                    return
                elif event.button == 1 and BTN_mode3.collidepoint(event.pos):
                    interface.mode = 3
                    return
            elif event.type == pg.VIDEORESIZE:
                WINDOW_SIZE = event.size
                screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)

def mode1(interface):  
    global run, screen, WINDOW_SIZE, pivot, offset, Start_loc, all_sprites, block_list
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
    block_list.empty()
    all_sprites.add(book1)
    state = 0
    i = 0

    while run:

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
                    print("next page")
                    state = 1
                    # Back
                if event.key == pg.K_DOWN:
                    interface.mode = 0
                    return

        if state == 1:
            if i < len(BOOK1):
                book1.next_page(i)
                i += 1
            else:
                i = 0
                state = 0
        book1.org_image = pg.transform.scale(book1.org_image, (int(WINDOW_SIZE[0]/36), int(WINDOW_SIZE[1]/2.5)))
        screen.fill(WHITE)

        all_sprites.draw(screen)                             # 全部畫出來
        # interface.show()
        # 正式渲染
        pg.display.update()
        clock.tick(6)

        # if event.type == pg.KEYUP:                            # Back
        #     if event.key == pg.K_DOWN:
        #         interface.mode = 0
        #         return

def mode2(interface):
    from PIL import Image
    from pykeyboard import PyKeyboard
    from os import getcwd
    import keyboard
    import sys
    import subprocess
    import psutil
    global run, screen, WINDOW_SIZE, pivot, offset, Start_loc, all_sprites, block_list
    k = PyKeyboard()

    # image = Image.open('002.jpg')
    # image.show()
    imageViewerFromCommandLine = {'linux':'xdg-open',
                                  'win32':'explorer',
                                  'darwin':'open'}[sys.platform]
    # print(imageViewerFromCommandLine)
    pro = subprocess.Popen([imageViewerFromCommandLine, "002.jpg"])
    # subprocess.run([imageViewerFromCommandLine, 'book1.png'])
    interface.mode = 0
    while run:
        if keyboard.read_key() == "p":
            print("You pressed p")
            k.press_keys([k.control_key, k.keypad_keys["Add"]])
            k.press_keys([k.control_key, k.keypad_keys["Add"]])     
            # image.close()
            # break
        if keyboard.read_key() == "o":
            print("You pressed o")
            k.press_keys([k.control_key, k.keypad_keys["Subtract"]])
            k.press_keys([k.control_key, k.keypad_keys["Subtract"]])  
        if keyboard.read_key() == "q":
            print("You pressed q")
            pro.kill()
            interface.mode = 0
            break
            # for proc in psutil.process_iter():
            #     print(proc.name())
            #     if proc.name() == "explorer.exe":
            #         proc.kill()

    interface.mode = 0
    # return

def mode3(interface):
    # 遊戲bg
    global run, screen, WINDOW_SIZE, pivot, offset, Start_loc, all_sprites, block_list
    bg2 = pg.Surface(screen.get_size())
    bg2 = bg2.convert()
    bg2.fill(WHITE)

    clock = pg.time.Clock()
    player = Hand(HAND[1], (int(WINDOW_SIZE[0] /2) , int(WINDOW_SIZE[1]*3/4)))  # (x, y)
    opponent = Hand(HAND[1], (int(WINDOW_SIZE[0] /2) , int(WINDOW_SIZE[1]/4)))
    interface.hp = 3
    interface.score = 0
    screen.blit(bg2, (0,0))
    pg.display.update()
    # 清空物件
    all_sprites.empty()
    block_list.empty()
    all_sprites.add(player)
    all_sprites.add(opponent)
    state = 0
    throw = False
    i = 1
    win = 0
    lose = 0
    #all_sprites.add(interface)

    while run:
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
                    interface.mode = 0
                    return
        
        if throw:
            num = random.randint(0, 2)
            print(num)
            opponent.change(num)
            player.change(i)
            throw = False

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

            

        player.org_image = pg.transform.scale(player.org_image, (int(WINDOW_SIZE[0]/36), int(WINDOW_SIZE[1]/2.5)))
        screen.fill(WHITE)

        all_sprites.draw(screen)                             # 全部畫出來
        # interface.show()

        # 正式渲染
        msg = title_font.render("", True, (0, 0, 0))
        if state == 1:
            msg = title_font.render("It's a tie!", True, (0, 0, 0))
            screen.blit(msg, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/2.3))
        elif state == 2:
            msg = title_font.render('You win!', True, (0, 0, 0))
            screen.blit(msg, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/2.3))
        elif state == 3:
            msg = title_font.render('You Lose QQ', True, (0, 0, 0))
            screen.blit(msg, (WINDOW_SIZE[0]/2.8, WINDOW_SIZE[1]/2.3))

        win_counter = score_font.render('Win : '+ str(win), True, (0, 0, 0))
        lose_counter = score_font.render('Lose : '+ str(lose), True, (0, 0, 0))
        screen.blit(win_counter, (WINDOW_SIZE[0]*0.05, WINDOW_SIZE[1]*0.8)) 
        screen.blit(lose_counter, (WINDOW_SIZE[0]*0.05, WINDOW_SIZE[1]*0.9)) 

        pg.display.update()
        clock.tick(6)

        if interface.hp == 0:
            interface.mode = 0
            return
        

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('test')                 # 視窗標題
    screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)

    block_list = pg.sprite.Group()                 # 碰撞檢測
    all_sprites = pg.sprite.Group()                # 所有角色

    interface = Interface()
    """
    pg.font.init()
    pg.joystick.init()
    pg.mixer.init()    
    """
    run = True
    while run:
        if interface.mode == 0:
            start(interface)
        if interface.mode == 1:
            mode1(interface)
        if interface.mode == 2:
            mode2(interface)
        if interface.mode == 3:
            mode3(interface)

    quit()   
