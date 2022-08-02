
from urllib import response
import pygame
from random import randint

pygame.init()

#variavels
triggered = False
pontos = 1

#escrever na tela

font = pygame.font.SysFont('./fontes/font.ttf',50)


#tamanho tela

x = 1280
y = 720

#cord nave

naveX = 60
naveY = 360 - 40

#cord asteroid
asteroidX = 1000
asteroideY = 360 - 40

#vel e cord missil
missil_x_vel = 0 
missilY = 337
missilX = 60 

screen = pygame.display.set_mode((x,y))
pygame.display.set_caption("Meu primeiro jogo")

#carregando background
bg = pygame.image.load("img/background.jpg").convert_alpha()
bg = pygame.transform.scale(bg,(x,y))

#carregando nave
nave = pygame.image.load("img/nave.png").convert_alpha()
nave = pygame.transform.scale(nave,(80,80))
nave = pygame.transform.rotate(nave,-90)

#carregar asteroide
asteroide = pygame.image.load("img/asteroide.png").convert_alpha()
asteroide = pygame.transform.scale(asteroide,(120,120))

#carregar missil
missil = pygame.image.load("img/missil.png").convert_alpha()
missil = pygame.transform.scale(missil,(50,50))

#colisoes
def colision():
    global pontos
    if nave_rect.colliderect(asteroid_rect) or asteroid_rect.x == 30:
        pontos -= 1
        return True
    if missil_rect.colliderect(asteroid_rect):
        pontos += 1
        return True
    else:
        return False


#funçoes respawn

#respawn asteroid
def respawn():
    x = 1350
    y = randint(1,640)
    return [x,y]

#respawn missil
def respawn_missil():
    triggered = False
    respawn_missil_x = naveX
    respawn_missil_y = naveY + 15
    respawn_vel_x = 0
    return [respawn_missil_x,respawn_missil_y,triggered,respawn_vel_x]

#transformando em objetos
nave_rect = nave.get_rect()
asteroid_rect = asteroide.get_rect()
missil_rect = missil.get_rect()

#loop principal

rodando = True

while rodando:
    #eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    #teclas
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and naveY > 1:
        naveY -= 1
        if not triggered:
            missilY -= 1
    if tecla[pygame.K_DOWN] and naveY < 640:
        naveY +=1
        if not triggered:
            missilY += 1
    if tecla[pygame.K_SPACE]:
        triggered = True
        missil_x_vel = 1

    nave_rect.y = naveY
    nave_rect.x = naveX

    missil_rect.y = missilY
    missil_rect.x = missilX

    asteroid_rect.x = asteroidX
    asteroid_rect.y = asteroideY

    #movimentos
    asteroidX -= 0.1 * pontos
    missilX += missil_x_vel

    #respawn
    if asteroidX == 30:
        asteroidX = respawn()[0]
        asteroideY = respawn()[1]

    if missilX == 1300:
        missilX,missilY,triggered,missil_x_vel = respawn_missil()

    #colisoes
    if asteroid_rect == 30 or colision():
        asteroidX= respawn()[0]
        asteroideY = respawn()[1]
        missilX,missilY,triggered,missil_x_vel = respawn_missil()
    #perder
    if pontos < 1:
        rodando = False

    #desenhar os pontos na tela
    score = font.render(f'Pontos: {int(pontos)}',True,(0,0,255))

    #Criar images
    screen.blit(bg,(0,0))
    screen.blit(missil,(missilX,missilY))
    screen.blit(score,(50,50))
    screen.blit(nave,(naveX,naveY))
    screen.blit(asteroide,(asteroidX,asteroideY))


    pygame.draw.rect(screen,(255,0,0), missil_rect,4)
    pygame.draw.rect(screen,(255,0,0), asteroid_rect,4)
    pygame.draw.rect(screen,(255,0,0),  nave_rect,4)

    
    
    pygame.display.update()
