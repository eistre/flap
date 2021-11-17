import pygame
import sys
import random

def tekita_värav(item, y, h, a):
    alumine_värav = item.get_rect(midtop = (a, y))
    ülemine_värav = item.get_rect(midbottom = (a, h))
    return alumine_värav, ülemine_värav

def tekita_tekst(item, y, h, a):
    alumine_tekst = choice.get_rect(midtop = (a-3, y))
    ülemine_tekst = choice.get_rect(midbottom = (a-3, h))
    return alumine_tekst, ülemine_tekst

def liiguta_värav(väravad):
    for i in väravad:
        i.centerx -= 4
    return väravad

def joonista_värav(väravad):
    for i in väravad:
        ekraan.blit(värav, i)
    return väravad

def joonista_aine(ained):
    for i in ained:
        ekraan.blit(aine, i)
    return väravad

def rotate(pilt, nurk, y):
    keeratud_pilt = pygame.transform.rotozoom(pilt, nurk, 1)
    keeratud_rect = keeratud_pilt.get_rect(center = (150, y))
    return keeratud_pilt, keeratud_rect

# algsätted
ekraan_x = 600
ekraan_y = 800
raskusaste = [(60, 1800), (90, 1200), (120, 800), (175, 600)]
raskus_sõne = ['Easy', 'Medium', 'Hard', 'Ultra']
raskus_indeks = 1

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
põrand = pygame.image.load('images/porand.png').convert()
    # mängija pilt ja hitbox
mängija = pygame.image.load('images/kast.png').convert_alpha()
mängija = pygame.transform.scale(mängija,(40,40))
mängija_rect = mängija.get_rect(center = (150, ekraan_y // 2))
nurk = 0
    # väravad
värav = pygame.image.load('images/varav.png').convert()
väravad = []
ained = []

text = [' MMP ', ' AAR ', ' OOP ', ' KM1 ']
font = pygame.font.SysFont(None, 150)

# loeb txt failist high skoori
f = open('high.txt')
high_skoor = int(f.readline().strip())
f.close()
skoor = 0
font = pygame.font.SysFont('Arial', 100)
text_high_skoor = font.render(f'High score: {high_skoor}', True, (255, 0, 0))
text_skoor = font.render(f'{int(skoor)}', True, (255, 0, 0))
text_raskus = font.render(f'Raskus: {raskus_sõne[raskus_indeks]}', True, (255, 0, 0))

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
            elif event.key == pygame.K_k and mäng == False:
                raskus_indeks += 1
                if raskus_indeks > 2:
                    raskus_indeks = 0
                väravad.clear()
                ained.clear()
                text_raskus = font.render(f'Raskus: {raskus_sõne[raskus_indeks]}', True, (255, 0, 0))
                pygame.time.set_timer(värava_tekkimine, raskusaste[raskus_indeks][1])
            elif event.key == pygame.K_q and mäng == False:
                raskus_indeks = 3
                väravad.clear()
                ained.clear()
                text_raskus = font.render(f'Raskus: {raskus_sõne[raskus_indeks]}', True, (255, 0, 0))
                pygame.time.set_timer(värava_tekkimine, raskusaste[raskus_indeks][1])
            elif event.key == pygame.K_SPACE and mäng == False:
                väravad.clear()
                ained.clear()
                mängija_rect = mängija.get_rect(center = (150, ekraan_y // 2))
                liikumine = -10
                skoor = 0
                text_skoor = font.render(f'{int(skoor)}', True, (255, 0, 0))
                mäng = True
 
        if event.type == värava_tekkimine:
            # iga 1.2 sekundi tagant tekitatakse uus paar väravaid
            punkt = random.randint((ekraan_y * 0.42) // 1 , (ekraan_y * 0.85) // 1)
            kõrgus = punkt - random.randint(220, 300)
            kaugus = ekraan_x + 100
            väravad.extend(tekita_värav(värav, punkt, kõrgus, kaugus))
            
            choice = random.choice(text)
            aine = font.render(choice, True, (255,0,0))
            aine = pygame.transform.rotate(aine, -90)
            ained.extend(tekita_värav(aine, punkt, kõrgus, kaugus))

    # ekraanile ilmub taust
    ekraan.blit(taust, (0, 0))
    
    
    if mäng:
        # mängija liikumine
        liikumine += 0.3
        mängija_rect.centery += liikumine
        nurk -= 1
        y_suurus = mängija_rect.centery
        mängija_rotated, mängija_rotated_rect = rotate(mängija, nurk, y_suurus)
        ekraan.blit(mängija_rotated, mängija_rotated_rect)
        
        # väravad
        väravad = liiguta_värav(väravad)
        ained = liiguta_värav(ained)
        joonista_värav(väravad)
        joonista_aine(ained)
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
        
        ekraan.blit(text_raskus, (10, 600))
        ekraan.blit(text_high_skoor, (10, 10))
        ekraan.blit(text_skoor, (ekraan_x // 2 - 33, ekraan_y // 8))
        
        
    
    # ekraanile ilmub põrand
    ekraan.blit(põrand, (0, ekraan_y - 80))
    
    pygame.display.update()
    fps.tick(raskusaste[raskus_indeks][0])