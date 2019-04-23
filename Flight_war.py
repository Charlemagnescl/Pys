import pygame
import sys
import traceback
from pygame.locals import *
from random import *
import playerlpane
import enemy
import bullet
import supply

#初始化
pygame.init()
pygame.mixer.init()

#背景图片
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Flight_war Demo")

#背景音乐
background  = pygame.image.load("source/background.png")
#颜色设置
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

#载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/button.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

#添加敌人函数定义
def add_Small_enmemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_Mid_enmemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.MidEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_Big_enmemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
#给敌人加速
def inc_speed(target,inc):
    for each in target:
        each.speed +=inc


#主循环
def main():
    restart = False
    while True:
        pygame.mixer.music.play(-1)

        #生成飞机
        player = playerlpane.Playerplane(bg_size)

        enemies = pygame.sprite.Group()

        #生成子弹
        bullet1 = []
        bullet1_index = 0
        BULLET1_NUM = 4
        for i in range(BULLET1_NUM):
            bullet1.append(bullet.Bullet1(player.rect.midtop))

        bullet2 = []
        bullet2_index = 0
        BULLET2_NUM = 8
        for i in range(BULLET2_NUM):
            bullet2.append(bullet.Bullet2((player.rect.centerx-33,player.rect.centery)))
            bullet2.append(bullet.Bullet2((player.rect.centerx+30,player.rect.centery)))

        #生成敌方小型飞机
        Small_enemies = pygame.sprite.Group()
        add_Small_enmemies(Small_enemies,enemies,30)

        #生成敌方中型型飞机
        Mid_enemies = pygame.sprite.Group()
        add_Mid_enmemies(Mid_enemies,enemies,10)

        #生成敌方大型飞机
        Big_enemies = pygame.sprite.Group()
        add_Big_enmemies(Big_enemies,enemies,5)

        #中弹图片索引
        e1_destroy_index = 0
        e2_destroy_index = 0
        e3_destroy_index = 0
        player_destroy_index = 0
        #统计得分
        score = 0
        score_font = pygame.font.Font("font/font.ttf",36)

            

        #设置难度
        level = 1

        #全屏炸弹
        bomb_image = pygame.image.load("source/bomb.png")
        bomb_rect = bomb_image.get_rect()
        bomb_font = pygame.font.Font("font/font.ttf",48)
        bomb_num = 3

        #补给包
        bullet_supply = supply.Bullet_Supply(bg_size)
        bomb_supply = supply.Bomb_Supply(bg_size)
        SUPPLY_TIME = USEREVENT
        pygame.time.set_timer(SUPPLY_TIME,30 * 1000)

        #子弹定时器
        DOUBLE_BULLET_TIME = USEREVENT + 1

        #解除无敌
        INVINCIBLE_TIME = USEREVENT + 2


        #是否使用超级子弹
        is_double_bullet = False

        #用户生命
        life_image = pygame.image.load("source/life.png").convert_alpha()
        life_image_rect =life_image.get_rect()
        life_num = 3

        #限制打开记录文件
        with open("target.txt","r") as f:
            target_score = int(f.read())
        recorded = False

        #绘制结束页面
        gameover_font = pygame.font.Font("font/font.ttf",48)
        again_image = pygame.image.load("source/restart_nor.png").convert_alpha()
        again_image_rect = again_image.get_rect()
        gameover_image = pygame.image.load("source/gameover.png").convert_alpha()
        gameover_image_rect = gameover_image.get_rect()



        #暂停
        pause = False
        pause_nor_image = pygame.image.load("source/game_pause_nor.png").convert_alpha()
        pause_pressed_image = pygame.image.load("source/game_pause_pressed.png").convert_alpha()
        resume_nor_image = pygame.image.load("source/game_resume_nor.png").convert_alpha()
        resume_pressed_image = pygame.image.load("source/game_resume_pressed.png").convert_alpha()
        pause_rect = pause_nor_image.get_rect()
        pause_rect.left,pause_rect.top = width - pause_rect.width - 10,10
        pause_image = pause_nor_image
        pause_pressed = False

        #重新开始与推出游戏与继续与开始游戏
        quit_image_nor = pygame.image.load("source/quit_nor.png")
        quit_image_pressed = pygame.image.load("source/quit_sel.png")
        restart_image_nor = pygame.image.load("source/restart_nor.png")
        restart_image_pressed = pygame.image.load("source/restart_sel.png")
        quit_image = quit_image_nor
        quit_rect = quit_image_nor.get_rect()
        quit_rect.left,quit_rect.top = 265,525
        restart_image = restart_image_nor
        restart_rect = restart_image_nor.get_rect()
        restart_rect.left,restart_rect.top = 80,525
        score_final_font = pygame.font.Font("font/font.ttf",38)
        begin_image = pygame.image.load("source/begin.png")
        begin_image_rect = begin_image.get_rect()
        begin_image_rect.left,begin_image_rect.top = 120,565
        """continue_nor_image = pygame.image.load("source/resume_nor.png")
        continue_press_image = pygame.image.load("source/restart_sel.png")
        continue_image = continue_nor_image
        continue_image_rect = continue_nor_image.get_rect()
        continue_image_rect.left,continue_image_rect.top = """

        #切换飞机
        switch_playerplane = True

        #延时
        delay = 100

        #帧率
        clock = pygame.time.Clock()

        running = True
        begining = True
        bullets = []


        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if begining:
                            if begin_image_rect.collidepoint(event.pos):
                                begining = False
                        elif life_num and pause_rect.collidepoint(event.pos):
                            pause = not pause
                            if pause:
                                pause_image = resume_pressed_image
                                pygame.time.set_timer(SUPPLY_TIME,0)
                                pygame.mixer.music.unpause()
                            else :
                                pause_image = pause_pressed_image
                                pygame.time.set_timer(SUPPLY_TIME,30*1000)
                                pygame.mixer.music.unpause() 
                        elif not life_num or pause:
                            if restart_rect.collidepoint(event.pos):
                                if pause:
                                    pause = False
                                restart = True
                                break
                                
                            elif quit_rect.collidepoint(event.pos):
                                if pause:
                                    pause = False
                                pygame.quit()
                                sys.exit()
                            
                elif event.type == MOUSEMOTION :
                    if life_num:
                        if pause_rect.collidepoint(event.pos):
                            if pause:
                                pause_image = resume_pressed_image
                            else:
                                pause_image = pause_pressed_image
                        else :
                            if pause:
                                pause_image = resume_nor_image
                            else:
                                pause_image = pause_nor_image
                    elif not life_num or pause:
                        if restart_rect.collidepoint(event.pos):
                            restart_image = restart_image_pressed
                        else :
                            restart_image = restart_image_nor
                        if quit_rect.collidepoint(event.pos):
                            quit_image = quit_image_pressed
                        else :
                            quit_image = quit_image_nor
                
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if bomb_num>0:
                            bomb_num-=1
                            bomb_sound.play()
                            for each in enemies:
                                if each.rect.bottom>0:
                                    each.live = False
                
                elif event.type == SUPPLY_TIME:
                    supply_sound.play()
                    if choice([True,False]):
                        bomb_supply.Reset()
                    else :
                        bullet_supply.Reset()

                elif event.type == DOUBLE_BULLET_TIME:
                    is_double_bullet = False
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,0)
                
                elif event.type == INVINCIBLE_TIME:
                    player.invincible = False
                    pygame.time.set_timer(INVINCIBLE_TIME,0)
            if restart:
                restart = False
                break

            #根据用户得分提高难度
            if (score//level) > 100000:
                upgrade_sound.play()
                level+=1
                add_Big_enmemies(Big_enemies,enemies,1)
                add_Mid_enmemies(Mid_enemies,enemies,3)
                add_Small_enmemies(Small_enemies,enemies,5)
                if (level%4==0):
                    inc_speed(Small_enemies,1)
                if (level%8==0):
                    inc_speed(Mid_enemies,1)
                if (level%16==0):
                    inc_speed(Big_enemies,1)
            screen.blit(background,(0, 0))
            if begining:
                screen.blit(begin_image,(180,545))
                help_text6 = score_font.render("How to play:",True,WHITE)
                screen.blit(help_text6,(50,195))
                help_text1 = score_font.render("Press up/right/left/down ",True,WHITE)
                screen.blit(help_text1,(50,235))
                help_text3 = score_font.render("to fly the plane",True,WHITE)
                screen.blit(help_text3,(50,265))
                help_text2 = score_font.render("Press space ",True,WHITE)
                screen.blit(help_text2,(50,335))
                help_text4 = score_font.render("to use the big bomb",True,WHITE)
                screen.blit(help_text4,(50,375))

            elif not pause and life_num:

                #获得用户键盘操作
                key_pressed = pygame.key.get_pressed()

                if key_pressed[K_w] or key_pressed[K_UP]:
                    player.MoveUp()
                if key_pressed[K_d] or key_pressed[K_DOWN]:
                    player.MoveDown()
                if key_pressed[K_l] or key_pressed[K_LEFT]:
                    player.MoveLeft()
                if key_pressed[K_r] or key_pressed[K_RIGHT]:
                    player.MoveRight()

                #绘制补给并检测
                if bomb_supply.active:
                    bomb_supply.Move()
                    screen.blit(bomb_supply.image,bomb_supply.rect)
                    if pygame.sprite.collide_mask(bomb_supply,player):
                        get_bomb_sound.play()
                        if bomb_num<3:
                            bomb_num+=1
                        bomb_supply.active = False
                    
                if bullet_supply.active:
                    bullet_supply.Move()
                    screen.blit(bullet_supply.image,bullet_supply.rect)
                    if pygame.sprite.collide_mask(bullet_supply,player):
                        get_bullet_sound.play()
                        #发射子弹2
                        is_double_bullet = True
                        pygame.time.set_timer(DOUBLE_BULLET_TIME,18 * 1000)
                        bullet_supply.active = False

                #发射子弹
                if not (delay%10):
                    bullet_sound.play()
                    if is_double_bullet:
                        bullets = bullet2
                        bullets[bullet2_index].Reset((player.rect.centerx-33,player.rect.centery))
                        bullets[bullet2_index+1].Reset((player.rect.centerx+30,player.rect.centery))
                        bullet2_index = (bullet2_index+2)% BULLET2_NUM 
                    else :
                        bullets = bullet1
                        bullets[bullet1_index].Reset(player.rect.midtop)
                        bullet1_index = (bullet1_index+1)%BULLET1_NUM

                for b in bullets:
                    if b.live:
                        b.Move()
                        screen.blit(b.image,b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                        if enemy_hit:
                            b.live = False
                            for e in enemy_hit:
                                if e in Mid_enemies or e in Big_enemies:
                                    e.Hp -= 1
                                    e.hit = True
                                    e.hitted = True
                                    if e.Hp == 0: 
                                        e.live = False                           
                                else :
                                    e.live = False
                #绘制敌机
                for each in Big_enemies:
                    if each.live:
                        each.Move()
                        if each.hit:
                            screen.blit(each.image_hit,each.rect)
                            each.hit = False
                        else :
                            screen.blit(each.image,each.rect)
                        if each.rect.bottom > -30:
                            enemy3_fly_sound.play(-1)
                        

                        #血槽
                        if each.hitted:
                            pygame.draw.line(screen,BLACK,\
                                    (each.rect.left,each.rect.top - 5),\
                                    (each.rect.right,each.rect.top-5),\
                                    2)
                            Hp_remain = each.Hp / enemy.BigEnemy.Hp
                            if Hp_remain > 0.2:
                                Hp_color = GREEN
                            else :
                                Hp_color = RED
                            pygame.draw.line(screen,Hp_color,\
                                    (each.rect.left,each.rect.top - 5),\
                                    (each.rect.left + each.rect.width*Hp_remain,each.rect.top-5),\
                                    2)
                    else :
                        if life_num :
                            enemy3_fly_sound.stop()
                            enemy3_down_sound.play()
                            if not(delay%3):
                                if e3_destroy_index == 0:
                                    enemy3_down_sound.play()
                                screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                                e3_destroy_index = (e3_destroy_index + 1)%5
                                if e3_destroy_index == 0:
                                    each.Reset()
                                    score+=10000


                
                for each in Mid_enemies:
                    if each.live:
                        each.Move()
                        if each.hit:
                                screen.blit(each.image_hit,each.rect)
                                each.hit = False
                        else :
                            screen.blit(each.image,each.rect)
                        
                        
                        #血槽
                        if each.hitted:
                            pygame.draw.line(screen,BLACK,\
                                    (each.rect.left,each.rect.top - 5),\
                                    (each.rect.right,each.rect.top-5),\
                                    2)
                            Hp_remain = each.Hp / enemy.MidEnemy.Hp
                            if Hp_remain > 0.2:
                                Hp_color = GREEN
                            else :
                                Hp_color = RED
                            pygame.draw.line(screen,Hp_color,\
                                    (each.rect.left,each.rect.top - 5),\
                                    (each.rect.left + each.rect.width*Hp_remain,each.rect.top-5),\
                                    2)
                    else :
                        if life_num :
                            enemy2_down_sound.play()
                            if not(delay%3):
                                if e2_destroy_index == 0:
                                    enemy2_down_sound.play()
                                screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                                e2_destroy_index = (e2_destroy_index + 1)%3
                                if e2_destroy_index == 0:
                                    each.Reset()
                                    score+=6000
            
                for each in Small_enemies:
                    if each.live:
                        each.Move()
                        screen.blit(each.image,each.rect)
                    else :
                        if life_num :
                            if not(delay%3):
                                if e1_destroy_index == 0:
                                    enemy1_down_sound.play()
                                screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                                e1_destroy_index = (e1_destroy_index + 1)%3
                                if e1_destroy_index == 0:
                                    each.Reset()
                                    score+=1000

                #检测我方飞机是否被撞
                enemies_down = pygame.sprite.spritecollide(player,enemies,False,pygame.sprite.collide_mask)
                if enemies_down and not player.invincible:
                    for e in enemies_down:
                        if e.live:
                            e.live = False
                            player.live =False
                    
                
                #绘制飞机
                if player.live:
                    if switch_playerplane:
                        screen.blit(player.image1,player.rect)
                    else :
                        screen.blit(player.image2,player.rect)
                else :
                    if not (delay % 3):
                        if player_destroy_index == 0:
                            me_down_sound.play()
                        screen.blit(player.destroy_images[player_destroy_index],player.rect)
                        player_destroy_index = (player_destroy_index + 1) % 3
                        if player_destroy_index == 0:
                            player.Reset()
                            pygame.time.set_timer(INVINCIBLE_TIME,3*1000)
                            if life_num:
                                life_num-=1
                
                #绘制炸弹
                bomb_text = bomb_font.render("X %d" % bomb_num,True,WHITE)
                bomb_text_rect = bomb_text.get_rect()
                screen.blit(bomb_image,(10, height - 10 - bomb_rect.height))
                screen.blit(bomb_text,(20 + bomb_text_rect.width,height - 5 -bomb_text_rect.height))
            
                #绘制生命数量
                if life_num:
                    for i in  range(life_num):
                        screen.blit(life_image,(width - 10 -(i+1)*life_image_rect.width,height - 10 - life_image_rect.height))
                
                #绘制得分
                score_text = score_font.render("Score: %s" % str(score),True,WHITE)
                screen.blit(score_text,(10,5))

                #绘制暂停按钮
                screen.blit(pause_image,pause_rect)
            elif pause:
                #显示得分
                score_final_text = score_final_font.render("Target Score: ",True,WHITE)
                screen.blit(score_final_text,(50,135))
                score_record_text = score_final_font.render("Now Score: " ,True,WHITE)
                screen.blit(score_record_text,(50,290))
                score_final_score = score_final_font.render("%s" % str(target_score),True,WHITE)
                screen.blit(score_final_score,(50,175))
                score_record_text = score_final_font.render("%s" % str(score),True,WHITE)
                screen.blit(score_record_text,(50,330))
                #绘制重新开始与结束游戏
                screen.blit(restart_image,(80,525))
                screen.blit(quit_image,(265,525))
                #绘制暂停按钮
                screen.blit(pause_image,pause_rect)
                
            elif life_num==0:
                #停止音效
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                #停止补给
                pygame.time.set_timer(SUPPLY_TIME,0)
                #消灭敌人
                has_dead = True
                for i in enemies:
                    i.live = False
                #最高得分
                if not recorded:
                    recorded = True
                    with open("record.txt","r") as f:
                        record_score = int(f.read())
                    
                    if score > record_score:
                        with open("record.txt","w") as f:
                            f.write(str(score))

                #绘制结束界面
                screen.blit(background,(0,0))
                #显示得分
                score_final_text = score_final_font.render("Top Score: ",True,WHITE)
                screen.blit(score_final_text,(50,135))
                score_record_text = score_final_font.render("Final Score: ",True,WHITE)
                screen.blit(score_record_text,(50,290))
                score_final_score = score_final_font.render("%s" % str(record_score),True,WHITE)
                screen.blit(score_final_score,(50,175))
                score_record_text = score_final_font.render("%s" % str(score),True,WHITE)
                screen.blit(score_record_text,(50,330))
                #绘制重新开始与结束游戏
                screen.blit(restart_image,(80,525))
                screen.blit(quit_image,(265,525))


            #切换图片
            if not (delay % 5):
                switch_playerplane = not switch_playerplane
            delay -= 1
            if not delay:
                delay = 100
            
            pygame.display.flip()

            clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()





