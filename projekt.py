import pygame
import sys
import random

def tekita_värav(item, y, h, a):
    alumine_värav = item.get_rect(midtop = (a, y))
    ülemine_värav = item.get_rect(midbottom = (a, h))
    return alumine_värav, ülemine_värav

def tekita_tekst(item, y, h, a):
    alumine_tekst = item.get_rect(midtop = (a, y))
    ülemine_tekst = item.get_rect(midbottom = (a, h))
    return alumine_tekst, ülemine_tekst

def liiguta_värav(väravad):
    for i in väravad:
        i.centerx -= 4
    return väravad

def joonista_värav(väravad):
    for i in väravad:
        ekraan.blit(värav, i)
    return väravad

def joonista_aine1(ained):
    for i in ained:
        ekraan.blit(aine1, i)
    return ained

def joonista_aine2(ained):
    for i in ained:
        ekraan.blit(aine2, i)
    return ained

# algsätted
ekraan_x = 600
ekraan_y = 800
raskusaste = [(120, 800), (60, 1800), (90, 1200), (175, 600)]
raskus_sõne = ['Hard', 'Easy', 'Medium', 'Ultra']
raskus_indeks = 2

pygame.init()
ekraan = pygame.display.set_mode((ekraan_x, ekraan_y))
fps = pygame.time.Clock()
värava_tekkimine = pygame.USEREVENT
pygame.time.set_timer(värava_tekkimine, raskusaste[raskus_indeks][1])

liikumine = 0

# vajalikud pildid ja hitboxid
    # taustapilt
taust = pygame.image.load('images/background.png').convert_alpha()
taust = pygame.transform.scale(taust, (2844, 800))
    # põranda pilt
põrand = pygame.image.load('images/floor.png').convert_alpha()
põrand = pygame.transform.scale(põrand, (600,80))
    # mängija pilt ja hitbox
mängija1 = pygame.image.load('images/kast1.png').convert_alpha()
mängija2 = pygame.image.load('images/kast2.png').convert_alpha()
mängija1 = pygame.transform.scale(mängija1,(50,50))
mängija2 = pygame.transform.scale(mängija2,(50,50))
mängija_rect = mängija1.get_rect(center = (150, ekraan_y // 2))
    # väravad
värav = pygame.image.load('images/pillar.png').convert_alpha()
värav = pygame.transform.scale(värav, (100, 549))
väravad = []
ained1 = []
ained2 = []

# loeb txt failist high skoori
f = open('high.txt')
high_skoor = int(f.readline().strip())
f.close()
skoor = 0

# fondid
text = ['  MMP  ', '  AAR  ', '  OOP  ', '  KM1  ', '   DM1   ', '   TMS   ', '   SSE   ',\
        '   ALGO   ', '   OPSÜS   ', '   PR1   ', '   PR2   ']
font = pygame.font.SysFont('cambria', 88)
font_skoor = pygame.font.SysFont('Roboto', 100)
font_text = pygame.font.SysFont('Roboto', 38)
text_high_skoor = font_text.render(f'Parim tulemus: {high_skoor} EAP', True, (11, 74, 184))
text_skoor = font_skoor.render(f'{int(skoor)}', True, (11, 74, 184))
text_raskus = font_text.render(f'Raskus: {raskus_sõne[raskus_indeks]}', True, (11, 74, 184))
text_raskus_hint = font_text.render('''Vajuta 'K', et muuta raskustaset''', True, (11, 74, 184))

mängija = mängija1
a = 0
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
                väravad.clear()
                ained1.clear()
                ained2.clear()
                if raskus_indeks > 2:
                    raskus_indeks = 0
                text_raskus = font_text.render(f'Raskus: {raskus_sõne[raskus_indeks]}', True, (11, 74, 184))
            elif event.key == pygame.K_q and mäng == False:
                raskus_indeks = 3
                väravad.clear()
                ained1.clear()
                ained2.clear()
                text_raskus = font_text.render(f'Raskus: {raskus_sõne[raskus_indeks]}', True, (11, 74, 184))
            elif event.key == pygame.K_SPACE and mäng == False:
                f = 2
                c = 802
                g = 3
                h = 603
                väravad.clear()
                ained1.clear()
                ained2.clear()
                mängija_rect = mängija.get_rect(center = (150, ekraan_y // 2))
                liikumine = -10
                skoor = 0
                text_skoor = font_skoor.render(f'{int(skoor)}', True, (11, 74, 184))
                pygame.time.set_timer(värava_tekkimine, raskusaste[raskus_indeks][1])
                mäng = True
 
        if event.type == värava_tekkimine:
            if a == 0:
                # tekitatakse uus paar väravaid
                punkt = random.randint((ekraan_y * 0.42) // 1 , (ekraan_y * 0.85) // 1)
                kõrgus = punkt - random.randint(220, 300)
                kaugus = ekraan_x + 100
                väravad.extend(tekita_värav(värav, punkt, kõrgus, kaugus))
                
                choice = random.choice(text)
                aine1 = font.render(choice, True, (11, 74, 184))
                aine1 = pygame.transform.rotate(aine1, -90)
                ained1.extend(tekita_värav(aine1, punkt, kõrgus, kaugus))
                a = 1
            elif a == 1:
                # tekitatakse uus paar väravaid
                punkt = random.randint((ekraan_y * 0.42) // 1 , (ekraan_y * 0.85) // 1)
                kõrgus = punkt - random.randint(220, 300)
                kaugus = ekraan_x + 100
                väravad.extend(tekita_värav(värav, punkt, kõrgus, kaugus))
                
                choice = random.choice(text)
                aine2 = font.render(choice, True, (11, 74, 184))
                aine2 = pygame.transform.rotate(aine2, -90)
                ained2.extend(tekita_värav(aine2, punkt, kõrgus, kaugus))
                a = 0
                
    if mäng:
        #taust liigub
        f -= 2
        if f <= -2844:
            f = 2
            c = 802
        ekraan.blit(taust, (f, 0))
        if f < -2044 and f > -2844:
            c -= 2
            ekraan.blit(taust, (c,0))
        
        # põrand liigub
        g -= 3
        h -= 3
        if g <= -600:
            g = 0
            h = 600
        ekraan.blit(põrand, (g, ekraan_y - 80))
        ekraan.blit(põrand, (h, ekraan_y - 80))
            
        # mängija liikumine
        if liikumine < 0:
            mängija = mängija2
        else:
            mängija = mängija1
        liikumine += 0.3
        mängija_rect.centery += liikumine
        ekraan.blit(mängija, mängija_rect)
        
        # väravad
        väravad = liiguta_värav(väravad)
        ained1 = liiguta_värav(ained1)
        ained2 = liiguta_värav(ained2)
        joonista_värav(väravad)
        joonista_aine1(ained1)
        joonista_aine2(ained2)
        ekraan.blit(text_skoor, (ekraan_x // 2 - 33, ekraan_y // 8))
        # collision väravatega
        for i in väravad:
            if pygame.Rect.colliderect(mängija_rect, i):
                mäng = False
            if mängija_rect.centerx in list(range(i.centerx-2, i.centerx+2)):
                skoor += 0.5
                text_skoor = font_skoor.render(f'{int(skoor)}', True, (11, 74, 184))
        # collision põranda, katusega
        if mängija_rect.top <= 0 or mängija_rect.bottom >= ekraan_y:
            mäng = False
        
    else:
        # prindib high skoori ja mängus saavutatud skoori
        # kui skoor on suurem siis kirjutatakse high skoor üle
        ekraan.blit(taust, (0, 0))
        ekraan.blit(mängija, (150, ekraan_x // 2))
        if skoor > high_skoor:
            high_skoor = int(skoor)
            text_high_skoor = font_text.render(f'Parim tulemus: {high_skoor} EAP', True, (11, 74, 184))
            
            f = open('high.txt', 'w')
            f.write(str(high_skoor))
            f.close()
        
        text_skoor = font_skoor.render(f'{int(skoor)}', True, (11, 74, 184))
        ekraan.blit(text_raskus_hint, (100, 600))
        ekraan.blit(text_raskus, (375, 20))
        ekraan.blit(text_high_skoor, (20, 20))
        ekraan.blit(text_skoor, (ekraan_x // 2 - 33, ekraan_y // 8))
    
        # ekraanile ilmub põrand
        ekraan.blit(põrand, (0, ekraan_y - 80))
    
    pygame.display.update()
    fps.tick(raskusaste[raskus_indeks][0])
