import pygame
import random

#okreslanie okna
WYS, SZER = 600, 600
pygame.init() #inicjowanie pygame
WIN = pygame.display.set_mode((WYS, SZER))
clock = pygame.time.Clock()
pygame.font.init()
pygame.display.set_caption("Game")

#PLANSZA
plansza = []
for i in range(WYS//50):
    plansza.append(SZER//50*[0])

#art
glowa = pygame.image.load("sssss.png")

# KOLORY

pretty_VIOLET = (167, 173, 242)
NOT_VIOLET = (100,100,100)
NOT_VIOLET2 = (100,100,150)
ALSO_NOT_VIOLET = (120,120,120)
ALSO_NOT_VIOLET2 = (120,120,150)
VERY_NOT_VIOLET = (50,250,200)
CZERWONY = (201,44,44)
CZERWONY_NOTRLLY = (201,144,44)
PINK = (214,77,125)
PINK2 = (242,111,155)
# KONSTANTY
FPS = 10
start_x, start_y = 200, 200
speed = 50
high_score = 0

# NOT KONTANSTY
KIERUNEK = 1
czy_owoc = False
sos_flaga = False
licznik = 0
licznik2 = 0
path=[]
halp = []
reserve = []
playerx =0
playery=0
owocx=0
owocy=0
myfont = pygame.font.SysFont('Comic Sans MS', 30)
TA_FLAGA = True
# --- OBIEKTY -----
ogon = [[pygame.Rect(start_x, start_y, 50, 50),1],[pygame.Rect(start_x-50, start_y, 50, 50),1],[pygame.Rect(start_x-80, start_y, 50, 50),1]]
for i in range(2,len(ogon)-1):
    #print(plansza[i])
    plansza[ogon[i][0].x//50][ogon[i][0].y//50] = 1
Player = pygame.Rect(start_x, start_y, 50, 50)

OwOc = pygame.Rect(600,600,50,50)

def rotate_head(kierunek):
    if kierunek == 1:
        angle = 90
    if kierunek == 2:
        angle = 0
    if kierunek == 3:
        angle = 270
    if kierunek == 4:
        angle = 180
    glowa_kopia = pygame.image.load("sssss.png")
    rotated = pygame.transform.rotate(glowa_kopia, angle)
    return rotated

def draw(): #funkcja rysująca
    global licznik
    WIN.fill(pretty_VIOLET)
    tekst = myfont.render(str(Player.x)+ " " + str(Player.y), False, (0,0,0))
    tekst2 =  myfont.render(str(OwOc.x)+ " " + str(OwOc.y), False, (0,0,0))
    tekst3 = myfont.render(str(licznik),False,(0,0,0))
    tekst4 = myfont.render(str(high_score),False,(0,0,0))
    WIN.blit(tekst,(10,10))
    WIN.blit(tekst2,(450,10))
    WIN.blit(tekst3, (250, 10))
    WIN.blit(tekst4, (200, 10))
    pygame.draw.rect(WIN, CZERWONY, OwOc)
    licznikx = 0
    for i in ogon:
        licznikx+=1
        if licznik%2==0:
            pygame.draw.rect(WIN, PINK2, i[0])
        else:
            pygame.draw.rect(WIN, PINK, i[0])
    WIN.blit(rotate_head(KIERUNEK),(Player.x,Player.y))
    #pygame.draw.rect(WIN, ALSO_NOT_VIOLET, Player)
    pygame.display.update()

def handle_przydzial():
    global czy_owoc, licznik
    if Player.colliderect(OwOc):
        czy_owoc = False
        if ogon[len(ogon)-1][1] == 1:
            temx = ogon[len(ogon)-1][0].x-50
            temy = ogon[len(ogon)-1][0].y
        if ogon[len(ogon)-1][1] == 2:
            temx = ogon[len(ogon)-1][0].x
            temy = ogon[len(ogon)-1][0].y-50
        if ogon[len(ogon)-1][1] == 3:
            temx = ogon[len(ogon)-1][0].x+50
            temy = ogon[len(ogon)-1][0].y
        if ogon[len(ogon)-1][1] == 4:
            temx = ogon[len(ogon)-1][0].x
            temy = ogon[len(ogon)-1][0].y+50
        licznik+=1
        print(licznik)
        ogon.append([pygame.Rect(temx,temy,50,50),ogon[len(ogon)-1][1]])

def handle_ogon_ruszanie():

    global plansza
    for i in range(len(ogon)-1,0,-1):
        ogon[i][0].x,ogon[i][0].y = ogon[i-1][0].x,ogon[i-1][0].y
        ogon[i][1]=ogon[i-1][1]
    plansza = []
    for i in range(WYS // 50):
        plansza.append(SZER // 50 * [0])
    for i in range(2,len(ogon)-1):
        plansza[ogon[i][0].y // 50][ogon[i][0].x // 50] = 1

def handle_owoc():
    global czy_owoc, SZER, WYS, ogon
    flaga = True
    while flaga:
        tx = random.randint(51, SZER-100)
        tem = tx//50
        tx = tem*50
        ty = random.randint(51, WYS-100)
        tem = ty//50
        ty = tem*50
        OwOc.x = tx
        OwOc.y = ty
        flaga = False
        for i in ogon:
            if i[0].colliderect(OwOc):
                flaga = True
    czy_owoc = True

def umieranie(player):
    global WYS, SZER
    if player.x < 0 or player.y < 0 or player.x > WYS-50 or player.y > SZER-50:
        return True
    for i in range(2,len(ogon)):
        if player.colliderect(ogon[i][0]):
            return True
        if player.x == ogon[i][0].x and player.y == ogon[i][0].y:
            return True
        if plansza[player.y//50][player.x//50] == 1:
            return True
    return False

def tryright(probnik):
    probnik.x+=50
    if umieranie(probnik):
        return False
    probnik.x-=50
    return True


def tryleft(probnik):
    probnik.x-=50
    if umieranie(probnik):
        return False
    probnik.x+=50
    return True


def tryup(probnik):
    probnik.y-=50
    if umieranie(probnik):
        return False
    probnik.y+=50
    return True

def trydown(probnik):
    probnik.y+=50
    if umieranie(probnik):
        return False
    probnik.y-=50
    return True

def followtemp(kierunek):
    global Player, OwOc, ogon, KIERUNEK, path
    if kierunek == "up" and KIERUNEK !=4:
            Player.y -= 50
            ogon[0][0].y -= 50
            KIERUNEK = 4
    if kierunek == "down"and KIERUNEK !=2:
            Player.y += 50
            ogon[0][0].y += 50
            KIERUNEK = 2
    if kierunek == "left"and KIERUNEK !=3:
            Player.x -= 50
            ogon[0][0].x -= 50
            KIERUNEK = 3
    if kierunek == "right"and KIERUNEK !=1:
            Player.x += 50
            ogon[0][0].x += 50
            KIERUNEK = 1
    ogon[0][1] = KIERUNEK


def followpath():
    global Player, OwOc, ogon, KIERUNEK, path
    probnik = pygame.Rect(Player.x,Player.y,50,50)
    i = path[0]
    if i == "up":
        probnik.y-=50
        if umieranie(probnik):
            temp = kod_jaskrawo_czerwony()
            if len(temp) > 0:
                followtemp(temp[0])
                print("where am goinh")
        else:
            Player.y-=50
            ogon[0][0].y-=50
            KIERUNEK =4
    if i == "down":
        probnik.y += 50
        if umieranie(probnik):
            temp = kod_jaskrawo_czerwony()
            if len(temp) > 0:
                followtemp(temp[0])

        else:
            Player.y+=50
            ogon[0][0].y += 50
            KIERUNEK = 2
    if i == "left":
        probnik.x -= 50
        if umieranie(probnik):
            temp = kod_jaskrawo_czerwony()
            if len(temp) > 0:
                followtemp(temp[0])
                print("where am goinh")
        else:
            Player.x -=50
            ogon[0][0].x -= 50
            KIERUNEK = 3
    if i == "right":
        probnik.x += 50
        if umieranie(probnik):
            temp = kod_czerwony()
            if len(temp) > 0:
                followtemp(temp[0])
                print("where am goinh")
        else:
            Player.x +=50
            ogon[0][0].x += 50
            KIERUNEK = 1
    ogon[0][1]= KIERUNEK


def kod_czerwony():
    global ogon,path, Player,KIERUNEK,sos_flaga
    tem = []
    sos_flaga= True
    print("sos")
    probnik = pygame.Rect(Player.x,Player.y,50,50)
    if tryup(probnik) and KIERUNEK != 2:
        tem.append("up")
    elif trydown(probnik) and KIERUNEK != 4:
        tem.append("down")
    elif tryleft(probnik) and KIERUNEK != 1:
        tem.append("left")
    elif tryright(probnik) and KIERUNEK != 3:
        tem.append("right")
    print(tem)
    return tem

def kod_jaskrawo_czerwony():
    global ogon
    return pathfin(ogon[len(ogon)-1][0])

def quarry(kierunek, probnik):
    global ogon, reserve
    tem = []
    tem2 = []
    mini = []
    reserve = []
    probnik2 = pygame.Rect(probnik.x,probnik.y,50,50)
    up = 0
    right = 0
    print("im lost")
    if kierunek == "up" or kierunek == "down":
        flagagora = True
        flagadol = True
        if kierunek == "down":
            up = 1
        if kierunek == "up":
            up = -1
        probnik.y += 50 * up
        for i in range(1,len(ogon)-1):
            probnik.x+=i*50
            probnik2.x+=i*50
            if flagagora:
                if umieranie(probnik2):
                    flagagora = False
                if umieranie(probnik):
                    continue
                else:
                    if checkfortunnels(probnik,kierunek,"right"):
                        tem.append(pygame.Rect(probnik.x,probnik.y,50,50))
                    else:
                        continue
            probnik.x-=2*i*50
            probnik2.x -= 2 * i * 50
            if flagadol:
                if umieranie(probnik2):
                    flagadol = False
                if umieranie(probnik):
                    continue
                else:
                    if checkfortunnels(probnik,kierunek,"left"):
                        tem2.append(pygame.Rect(probnik.x,probnik.y,50,50))
                    else:
                        continue

            probnik.x+=i*50
            probnik2.x += i * 50
        probnik.y-=50*up
    if kierunek == "right" or kierunek == "left":
        flagagora = True
        flagadol = True
        if kierunek == "right":
            right = 1
        if kierunek == "left":
            right = -1
        probnik.x += 50 * up
        for i in range(1,len(ogon)-1):
            probnik.y+=i*50
            probnik2.y += i * 50
            if flagagora:
                if umieranie(probnik2):
                    flagagora = False
                if umieranie(probnik):
                    continue
                else:
                    if checkfortunnels(probnik, kierunek, "down"):
                        tem2.append(pygame.Rect(probnik.x, probnik.y, 50, 50))
                    else:
                        continue
            probnik.y-=2*i*50
            probnik2.y -= 2 * i * 50
            if flagadol:
                if umieranie(probnik2):
                    flagadol = False
                if umieranie(probnik):
                    continue
                else:
                    if checkfortunnels(probnik, kierunek, "up"):
                        tem2.append(pygame.Rect(probnik.x, probnik.y, 50, 50))
                    else:
                        continue
            probnik.y+=i*50
            probnik2.y += i * 50
        probnik.x-=50*up
    if len(tem2) >0 or len(tem)>0:
        if len(tem)>0:
            reserve = shortpath(tem[0],probnik,kierunek)
            mini = [len(reserve),reserve]
            for i in tem:
                reserve = shortpath(i,probnik,kierunek)
                if len(reserve)<mini[0]:
                    mini = [len(reserve),reserve]
        if len(mini) == 0 and len(tem2)>0:
            reserve = shortpath(tem2[0], probnik, kierunek)
            mini = [len(reserve), reserve]
        if len(tem2)>0:
            for i in tem2:
                reserve = shortpath(i,probnik,kierunek)
                if len(reserve) < mini[0]:
                    mini = [len(reserve), reserve]
        return mini[1]
    else:
        return kod_czerwony()

def checkfortunnels(probnik,kierunek, kierunek2):
    nowy_probnik = pygame.Rect(probnik.x,probnik.y,50,50)
    if kierunek == "up" or kierunek == "down":
        if kierunek2 == "right":
            nowy_probnik.x+=50
            if umieranie(nowy_probnik):
                return False
            nowy_probnik.x-=50
        else:
            nowy_probnik.x -= 50
            if umieranie(nowy_probnik):
                return False
            nowy_probnik.x += 50
    else:
        if kierunek2 == "down":
            nowy_probnik.y+=50
            if umieranie(nowy_probnik):
                return False
            nowy_probnik.y-=50
        else:
            nowy_probnik.y -= 50
            if umieranie(nowy_probnik):
                return False
            nowy_probnik.y += 50
    return True


def shortpath(tutaj,probnik,kierunek):
    short =[]
    if kierunek == "up" or kierunek == "down":
        if probnik.x>tutaj.x:
            tem = probnik.x-tutaj.x
            #print(tem)
            for i in range(tem // 50+1):
                short.append("right")
        else:
            tem = -1*( probnik.x - tutaj.x)
            for i in range(tem//50+1):
                short.append("left")
        if kierunek == "up":
            tem = probnik.y - tutaj.y
            for i in range(tem // 50+1):
                short.append("up")
        else:
            tem = -1 * (probnik.y - tutaj.y)
            for i in range(tem // 50+1):
                short.append("down")
    if kierunek == "right" or kierunek == "left":
        if probnik.y>tutaj.y:
            tem = probnik.y-tutaj.y
            for i in range(tem // 50+1):
                short.append("up")
        else:
            tem = -1*( probnik.y - tutaj.y)
            for i in range(tem // 50+1):
                short.append("down")
        if kierunek == "left":
            tem = -1 * (probnik.x - tutaj.x)
            for i in range(tem // 50+1):
                short.append("left")
        else:
            tem = 1 * (probnik.x - tutaj.x)
            for i in range(tem // 50+1):
                short.append("right")
    #print(short)
    return short


def pathfin(OwOc):
    global ogon, Player, halp, TA_FLAGA, KIERUNEK
    probnik = pygame.Rect(Player.x, Player.y, 50, 50)
    pathw = []
    flaga = True
    while flaga:
        if probnik.y != OwOc.y:
            if probnik.y<OwOc.y:
                if trydown(probnik):
                    probnik.y+=50
                    pathw.append("down")
                else:
                    #TA_FLAGA = False
                    x = quarry("down",probnik)
                    if len(x)>0:
                        pathw.append(x[0])
                    #halp = quarry("down",probnik)
                    flaga = False
            if probnik.y > OwOc.y :
                if tryup(probnik):
                    probnik.y-=50
                    pathw.append("up")
                else:
                    #TA_FLAGA = False
                    x = quarry("up", probnik)
                    if len(x) > 0:
                        pathw.append(x[0])
                    #halp = quarry("up",probnik)
                    flaga = False
        if probnik.x != OwOc.x:
            if probnik.x<OwOc.x:
                if tryright(probnik):
                    probnik.x+=50
                    pathw.append("right")
                else:
                    #TA_FLAGA = False
                    x = quarry("right", probnik)
                    if len(x) > 0:
                        pathw.append(x[0])
                    #halp = quarry("right",probnik)
                    flaga = False
            if probnik.x > OwOc.x:
                if tryleft(probnik):
                    probnik.x-=50
                    pathw.append("left")
                else:

                    x = quarry("left", probnik)
                    if len(x) > 0:
                        pathw.append(x[0])

                    flaga = False
        if probnik.x==OwOc.x and probnik.y==OwOc.y:
            flaga = False

    return pathw


def init():
    global Player, ogon, licznik, high_score
    ogon = [[pygame.Rect(start_x, start_y, 50, 50), 1], [pygame.Rect(start_x - 50, start_y, 50, 50), 1],
            [pygame.Rect(start_x - 80, start_y, 50, 50), 1]]
    if licznik>high_score:
        high_score = licznik
    licznik = 0
    Player = pygame.Rect(start_x, start_y, 50, 50)

def draw_path():
    global Player, TA_FLAGA

    red = pygame.Rect(Player.x+10,Player.y+10,30,30)
    for i in range(len(path)-2):
        if path[i] == "up":
            red.y -= 50

        if path[i] == "down":
            red.y += 50

        if path[i] == "left":
            red.x -= 50

        if path[i] == "right":
            red.x += 50
        pygame.draw.rect(WIN, CZERWONY_NOTRLLY, red)
    pygame.display.update()

def main(): #funkcja main
    global licznik2, TA_FLAGA, path, plansza, sos_flaga
    run = True
    flagusia = True
    licznikosiem = 0
    while run: #pętla gry
        #for i in range(len(plansza) - 1):
         #   print(plansza[i])
        draw()
        draw_path()
        #if len(path)>0:
         #   draw_path()
        if czy_owoc == False:
            handle_owoc()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                init()

        if TA_FLAGA:
            path = pathfin(OwOc)

        print(TA_FLAGA, path)
        if len(path)>0:
            followpath()
        handle_ogon_ruszanie()
        handle_przydzial()

        if umieranie(Player):
            print("=====================")
            init()

    pygame.quit()
main()