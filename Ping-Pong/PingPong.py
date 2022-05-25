from pygame import *
from random import randint

mixer.init()
bounce = mixer.Sound('bounce.ogg')

#Картинки
img_back = 'Background.jpg' #фон
img_ball = 'Ball.png' #мяч
img_racket1 = 'Racket1.png' #Ракетка 1
img_racket2 = 'Racket2.png' #Ракетка 2

speed_x = 2
speed_y = 2
score_1 = 0
score_2 = 0
goal = 5

#Класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #Конструктор класса
    def __init__(self, player_image, player_x, player_y, wight, height, player_speed):
        super().__init__()
        #Каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (wight, height))
        self.speed = player_speed
        #Каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #Метод для отрисовки героя на экране
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Класс самого игрока
class Player(GameSprite):
    def update_1(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
    def update_2(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 80:
            self.rect.y += self.speed



#Создание окна
win_width = 700
win_height = 500
display.set_caption('PingPong')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#Флаги, отвечающие за состояние игры
run = True
finish = False
clock = time.Clock()
FPS = 60

#Ракетка и мяч
racket1 = Player(img_racket1, 10, 250, 30, 100, 5)
racket2 = Player(img_racket2, 680, 250, 20, 100, 5)
ball = GameSprite(img_ball, 350, 250, 50, 50, 1)

#Текст
font.init()
font = font.Font(None, 35)
player1_lose = font.render('Player 1 lose!', True, (30, 75, 255))
player2_lose = font.render('Player 2 lose!', True, (255, 0, 50))
text1 = font.render('Счет:' + str(score_1), 1, (255, 255, 255))
text2 = font.render('Счет:' + str(score_2), 1, (255, 255, 255))

while run:
    #Событие нажатия на кнопку "Закрыть"
    for e in event.get():
        if e.type == QUIT:
            run = False

    #Сама игра - действие спрайтов, проверка правил игры, перерисовка
    if finish != True:
        window.blit(background, (0,0))
        window.blit(text1, (10, 10))
        window.blit(text2, (620, 10))
        racket1.update_1()
        racket2.update_2()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
            bounce.play()
            
        #Если мяч достиг границ экрана - меняем направление его движения
        if ball.rect.y > win_height or ball.rect.y < 0:
            speed_y *= -1
            bounce.play()

        if ball.rect.x < 0:
            finish = False
            score_2 += 1

        if ball.rect.x > win_width:
            finish = False
            score_1 += 1

        if score_1 >= goal:
            finish = True
            window.blit(player2_lose, (280, 240))

        if score_2 >= goal:
            finish = True
            window.blit(player1_lose, (280, 240))


        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)