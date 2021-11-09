import pygame
import sys
import random

def tekita_värav():
    punkt = random.randint(300, 700)
    alumine_värav = värav.get_rect(midtop = (700, punkt))
    ülemine_värav = värav.get_rect(midbottom = (700, punkt - 250))
    return alumine_värav, ülemine_värav

def liiguta_värav(väravad):
    for i in väravad:
        i.centerx -= 4
    return väravad

def joonista_värav(väravad):
    for i in väravad:
        ekraan.blit(värav, i)
    return väravad

# algsätted
pygame.init()
ekraan = pygame.display.set_mode((600, 800))
fps = pygame.time.Clock()
värava_tekkimine = pygame.USEREVENT
pygame.time.set_timer(värava_tekkimine, 1200)
liikumine = 0

# vajalikud pildid ja hitboxid
    # taustapilt
taust = pygame.image.load('images/background.png').convert()
    # põranda pilt
põrand = pygame.image.load('images/põrand.png').convert()
    # mängija pilt ja hitbox
mängija = pygame.image.load('images/kast.png').convert()
mängija_rect = mängija.get_rect(center = (150, 400))
    # väravad
värav = pygame.image.load('images/värav.png').convert()
väravad = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # ilma sys.exit() tekitab veateate
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                liikumine = 0
                liikumine -= 10
        if event.type == värava_tekkimine:
            # iga 1.2 sekundi tagant tekitatakse uus paar väravaid
            väravad.extend(tekita_värav())

    # ekraanile ilmub taust
    ekraan.blit(taust, (0, 0))
    
    # mängija liikumine
    liikumine += 0.3
    mängija_rect.centery += liikumine
    ekraan.blit(mängija, mängija_rect)
    
    # väravad
    väravad = liiguta_värav(väravad)
    joonista_värav(väravad)
    
    # ekraanile ilmub põrand
    ekraan.blit(põrand, (0, 720))
    
    pygame.display.update()
    fps.tick(90)