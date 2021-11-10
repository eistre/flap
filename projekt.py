import pygame
import sys
import random

def tekita_värav():
    punkt = random.randint((ekraan_y * 0.42) // 1 , (ekraan_y * 0.85) // 1)
    alumine_värav = värav.get_rect(midtop = (ekraan_x + 100, punkt))
    ülemine_värav = värav.get_rect(midbottom = (ekraan_x + 100, punkt - random.randint(200, 300)))
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
ekraan_x = 600
ekraan_y = 800

pygame.init()
ekraan = pygame.display.set_mode((ekraan_x, ekraan_y))
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
mängija_rect = mängija.get_rect(center = (150, ekraan_y // 2))
    # väravad
värav = pygame.image.load('images/värav.png').convert()
väravad = []

# loeb txt failist high skoori
f = open('high.txt')
high_skoor = int(f.readline().strip())
f.close()
skoor = 0
font = pygame.font.SysFont('Arial', 100)
text_high_skoor = font.render(f'High score: {high_skoor}', True, (255, 0, 0))
text_skoor = font.render(f'{int(skoor)}', True, (255, 0, 0))

mäng = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # ilma sys.exit() tekitab veateate
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and mäng:
                liikumine = 0
                liikumine -= 10
            elif event.key == pygame.K_SPACE and mäng == False:
                väravad.clear()
                mängija_rect = mängija.get_rect(center = (150, ekraan_y // 2))
                liikumine = 0
                skoor = 0
                text_skoor = font.render(f'{int(skoor)}', True, (255, 0, 0))
                mäng = True
                
        if event.type == värava_tekkimine:
            # iga 1.2 sekundi tagant tekitatakse uus paar väravaid
            väravad.extend(tekita_värav())

    # ekraanile ilmub taust
    ekraan.blit(taust, (0, 0))
    
    
    if mäng:
        # mängija liikumine
        liikumine += 0.3
        mängija_rect.centery += liikumine
        ekraan.blit(mängija, mängija_rect)
        
        # väravad
        väravad = liiguta_värav(väravad)
        joonista_värav(väravad)
        ekraan.blit(text_skoor, (ekraan_x // 2 - 33, ekraan_y // 8))
        # collision väravatega
        for i in väravad:
            if pygame.Rect.colliderect(mängija_rect, i):
                mäng = False
            if mängija_rect.centerx in list(range(i.centerx-2, i.centerx+2)):
                skoor += 0.5
                text_skoor = font.render(f'{int(skoor)}', True, (255, 0, 0))
        # collision põranda, katusega
        if mängija_rect.top <= 0 or mängija_rect.bottom >= ekraan_y - 80:
            mäng = False
        
    else:
        # prindib high skoori ja mängus saavutatud skoori
        # kui skoor on suurem siis kirjutatakse high skoor üle
        ekraan.blit(mängija, (150, ekraan_x // 2))
        if skoor > high_skoor:
            high_skoor = int(skoor)
            text_high_skoor = font.render(f'High score: {high_skoor}', True, (255, 0, 0))
            
            f = open('high.txt', 'w')
            f.write(str(high_skoor))
            f.close()
            
        ekraan.blit(text_high_skoor, (10, 10))
        ekraan.blit(text_skoor, (ekraan_x // 2 - 33, ekraan_y // 8))
        
        
    
    # ekraanile ilmub põrand
    ekraan.blit(põrand, (0, ekraan_y - 80))
    
    pygame.display.update()
    fps.tick(90)