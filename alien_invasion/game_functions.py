import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """按下键盘响应"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit(0)            

def fire_bullet(ai_settings, screen, ship, bullets):
    """若子弹数未超过限制，发射一颗子弹"""
    #创建一颗子弹并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """松开键盘响应"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False    

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                    bullets):
    #监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings,screen,ship,bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                 ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
     aliens, bullets, mouse_x, mouse_y):
    """在玩家点击play时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()

        #隐藏光标
        pygame.mouse.set_visible(False)

        #重置游戏的统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人 飞船重置到底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                    play_button):
    """更新屏幕图案，并切换到新屏幕"""
    #重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()    
    ship.blitme()
    aliens.draw(screen)

    #显示得分
    sb.show_score()

    #如果游戏处于非活动状态，显示play按钮
    if not stats.game_active:
        play_button.draw_button()

    #显示最近绘制的屏幕 
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置 并删除消失的子弹"""
    bullets.update()

    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:#子弹已经穿过边界
            bullets.remove(bullet)
    
    #检查是否有子弹击中了外星人
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                     aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                     aliens, bullets):
    """响应子弹和外星人的碰撞"""
    #剔除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)            
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #删除现有的子弹 加快游戏节奏 并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()

        #提高一个等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings,alien_width):
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算外星人的列数"""
    available_space_y = (ai_settings.screen_height -
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建第一个外星人并将其加入到当前行中"""
    alien = Alien(ai_settings, screen)
    alien_width=alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                    alien.rect.height)
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number) 

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """外星人撞击飞船时的响应"""
    if stats.ship_left > 0:
        #ship_left减一
        stats.ship_left -= 1

        #更新飞船数量
        sb.prep_ships()
        
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人 飞船重置到底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
        bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #情况形如外星人撞到飞船
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """
        检查是否有外星人到达屏幕边缘
        更新所有外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边界时改变方向"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= - 1

def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score >= stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()