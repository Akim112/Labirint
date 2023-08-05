
from pygame import*
class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image=transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

bullets = sprite.Group()
monsters = sprite.Group()


class Player(GameSprite):
    def __init__(self,picture,w,h,x,y,x_speed,y_speed):
        super().__init__(picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet1.png',40,40,self.rect.right,self.rect.centery,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self,picture,w,h,x,y,speed):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
    def update(self):
        if self.rect.x <= 340:
            self.direction = 'right'
        if self.rect.x >= 490:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self,picture,w,h,x,y,speed):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 710:
            self.kill()

walls = sprite.Group()
player = Player('character2.png',45,60,150,300,0,0)
final = GameSprite('final.png',70,70,600,420)
wall_1 = GameSprite('wall.png',30,300,300,250)
wall_2 = GameSprite('wall.png',200,30,120,250)
wall_3 = GameSprite('wall.png',30,130,120,250)
wall_4 = GameSprite('wall.png',70,30,120,380)
wall_5 = GameSprite('wall.png',30,130,120,120)
wall_6 = GameSprite('wall.png',30,110,240,0)
wall_7 = GameSprite('wall.png',210,30,240,100)
wall_8 = GameSprite('wall.png',30,200,430,100)
wall_9 = GameSprite('wall.png',30,350,550,150)
enemy = Enemy('enemy2.png',50,70,339,320,4)
walls.add(wall_1)
walls.add(wall_2)
walls.add(wall_3)
walls.add(wall_4)
walls.add(wall_5)
walls.add(wall_6)
walls.add(wall_7)
walls.add(wall_8)
walls.add(wall_9)
monsters.add(enemy)

display.set_caption('Labirint')
window = display.set_mode((700,500))
back = (59,105,184)
finish = False
win = transform.scale(image.load('win.jpg'),(700,500))
lose = transform.scale(image.load('lose.jpg'),(700,500))

run = True
while run:
    if finish != True:
        window.fill(back)
        wall_1.reset()
        player.reset()
        player.update()
        bullets.update()
        bullets.draw(window)
        wall_2.reset()
        wall_3.reset()
        wall_4.reset()
        wall_5.reset()
        wall_6.reset()
        enemy.reset()
        enemy.update()
        final.reset()
        wall_7.reset()
        wall_8.reset()
        wall_9.reset()
        sprite.groupcollide(bullets,walls,True,False)
        sprite.groupcollide(bullets,monsters,False,False)
        if sprite.collide_rect(player,final):
            finish = True
            window.blit(win,(0,0))
        if sprite.collide_rect(player,enemy):
            finish = True
            window.blit(lose,(0,0))
    
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                player.y_speed = -10
            if e.key == K_DOWN:
                player.y_speed = +10
            if e.key == K_LEFT:
                player.x_speed = -10
            if e.key == K_RIGHT:
                player.x_speed = +10
            if e.key == K_SPACE:
                player.fire()
        if e.type == KEYUP:
            if e.key == K_UP:
                player.y_speed = 0
            if e.key == K_DOWN:
                player.y_speed = 0
            if e.key == K_LEFT:
                player.x_speed = 0
            if e.key == K_RIGHT:
                player.x_speed = 0
    display.update()
