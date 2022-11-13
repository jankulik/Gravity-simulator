import pygame
from pygame import gfxdraw
from objects import Star, Planet, Button, white, black, dScale

def drawCircle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

mSun = 1.989E30
mEarth = 5.9724E24

mStar = 1.0       #mass of generated stars w.r.t. mass of the Sun
mPlanet = 1.0     #mass of generated planets w.r.t mass of Earth

rStar = 10
rPlanet = 4

yellow1 = (153, 149, 96)
yellow2 = (232, 218, 32)

blue1 = (53, 104, 130)
blue2 = (34, 145, 230)

pygame.init()
screen = pygame.display.set_mode((1350, 760))
screen.fill(black)
canvas = screen.copy()

width = screen.get_width()
height = screen.get_height()

font = pygame.font.SysFont('Hack', 24)
icon = pygame.image.load('apple.jpg')
pygame.display.set_icon(icon)
pygame.display.set_caption("Gravity Simulator")

stars = []
planets = []
buttonStar = Button(10, 10, 110, 28, font, 'Star')
buttonPlanet = Button(10, 48, 110, 28, font, 'Planet')
buttonSystem = Button(10, 86, 110, 28, font, 'Solar System')
buttonClear = Button(10, 124, 110, 28, font, 'Clear')

buttonSun = Button(180, height - 60, 80, 24, font, 'The Sun')
buttonEarth = Button(270, height - 60, 80, 24, font, 'Earth')

text1 = font.render('Mass with respect to', True, white)
text2 = font.render('Mass:', True, white)

mousePressed = False
solarSystem = False
buttonSun.clicked = True
running = True

oldTime = pygame.time.get_ticks()

while running:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx0, my0 = event.pos
            button = event.button
                            
            if (button == 1 and
                buttonPlanet.clicked and not
                buttonStar.hovering(mx0, my0) and not
                buttonPlanet.hovering(mx0, my0) and not
                buttonSystem.hovering(mx0, my0) and not
                buttonClear.hovering(mx0, my0) and not
                buttonSun.hovering(mx0, my0) and not
                buttonEarth.hovering(mx0, my0)):
                    
                mousePressed = True
                
                planets.append(Planet(mx0, my0, 0, 0, 0))
                
            elif button == 4 and (buttonStar.clicked or buttonPlanet.clicked):
                if buttonSun.clicked:
                    if mStar < 1:
                        mStar += 0.05
                    elif mStar >= 1:
                        mStar += 1
                else:
                    if mPlanet < 1:
                        mPlanet += 0.05
                    elif mPlanet >= 1:
                        mPlanet += 1
                    
            elif button == 5 and (buttonStar.clicked or buttonPlanet.clicked):
                if buttonSun.clicked:
                    if 0 < mStar <= 1:
                        mStar -= 0.05
                    elif mStar > 1:
                        mStar -= 1
                else:
                    if 0 < mPlanet <= 1:
                        mPlanet -= 0.05
                    elif mPlanet > 1:
                        mPlanet -= 1
                
        elif event.type == pygame.MOUSEBUTTONUP:
            mx1, my1 = event.pos
            button = event.button
            
            if button == 1:
                if buttonStar.hovering(mx1, my1):
                    buttonStar.clicked = not buttonStar.clicked
                    
                    if buttonStar.clicked and buttonPlanet.clicked:
                        buttonPlanet.clicked = False
                
                elif buttonPlanet.hovering(mx1, my1):
                    buttonPlanet.clicked = not buttonPlanet.clicked
                    
                    if buttonStar.clicked and buttonPlanet.clicked:
                        buttonStar.clicked = False
                
                elif buttonSystem.hovering(mx1, my1) and not solarSystem:
                    solarSystem = True
                    stars.append(Star(width / 2, height / 2, mSun))
                    
                    planets.append(Planet(width / 2, height / 2 + 6.9817E10 / dScale, 38860, 0, 3.3011E23))
                    planets.append(Planet(width / 2, height / 2 + 1.08939E11 / dScale, 34790, 0, 4.8675E24))
                    planets.append(Planet(width / 2, height / 2 + 1.52099E11 / dScale, 29290, 0, mEarth))
                    planets.append(Planet(width / 2, height / 2 + 2.49229E11 / dScale, 21970, 0, 6.4171E23))
                    planets.append(Planet(width / 2, height / 2 + 8.16618E11 / dScale, 12440, 0, 1.89819E27))
                    
                elif buttonClear.hovering(mx1, my1):
                    solarSystem = False
                    stars.clear()
                    planets.clear()
                    canvas.fill(black)
                    
                elif buttonSun.hovering(mx1, my1) and not buttonSun.clicked:
                    buttonSun.clicked = True
                    buttonEarth.clicked = False
                    
                elif buttonEarth.hovering(mx1, my1) and not buttonEarth.clicked:
                    buttonEarth.clicked = True
                    buttonSun.clicked = False
                    
                elif (buttonStar.clicked and not
                    buttonSun.hovering(mx0, my0) and not
                    buttonEarth.hovering(mx0, my0)):
                    
                    if buttonSun.clicked:
                        stars.append(Star(mx0, my0, mStar * mSun))
                    else:
                        stars.append(Star(mx0, my0, mPlanet * mEarth))
                    
                elif (mousePressed and
                    buttonPlanet.clicked and not
                    buttonStar.hovering(mx0, my0) and not
                    buttonPlanet.hovering(mx0, my0) and not
                    buttonSystem.hovering(mx0, my0) and not
                    buttonClear.hovering(mx0, my0) and not
                    buttonSun.hovering(mx0, my0) and not
                    buttonEarth.hovering(mx0, my0)):
                    
                    planets[-1].setVelocity(mx1, my1)
                    
                    if buttonSun.clicked:
                        planets[-1].m = mStar * mSun
                    else:
                        planets[-1].m = mPlanet * mEarth
                    
                mousePressed = False
                    
    time = pygame.time.get_ticks()
    dt = time - oldTime
    oldTime = time
    
    mx, my = pygame.mouse.get_pos()
    screen.fill(black)
    screen.blit(canvas, (0, 0))
    
    if buttonStar.clicked:
        drawCircle(screen, mx, my, rStar, yellow1)
        
    elif buttonPlanet.clicked and not mousePressed:
        drawCircle(screen, mx, my, rPlanet, blue1)
        
    elif buttonPlanet.clicked and mousePressed:
        pygame.draw.line(screen, white, (mx0, my0), (mx, my), 1)
        
    for i in range(len(planets)):
        if not planets[i].collided:
            if i != len(planets) - 1 or not mousePressed:
                planets[i].gravity(stars, planets, dt)
            
            position = (planets[i].x, planets[i].y)
            newPosition = planets[i].move(dt)
            
            if 0 - rPlanet <= newPosition[0] <= width + rPlanet and 0 - rPlanet <= newPosition[1] <= height + rPlanet:
                pygame.draw.aaline(canvas, blue1, position, newPosition)
                drawCircle(screen, int(newPosition[0]), int(newPosition[1]), rPlanet, blue2)
                
    for i in range(len(stars)):
        drawCircle(screen, int(stars[i].x), int(stars[i].y), rStar, yellow2)
            
    pygame.draw.rect(screen, buttonStar.color(mx, my), buttonStar.shape())
    screen.blit(buttonStar.text, buttonStar.textRect())
    
    pygame.draw.rect(screen, buttonPlanet.color(mx, my), buttonPlanet.shape())
    screen.blit(buttonPlanet.text, buttonPlanet.textRect())
    
    pygame.draw.rect(screen, buttonSystem.color(mx, my), buttonSystem.shape())
    screen.blit(buttonSystem.text, buttonSystem.textRect())
    
    pygame.draw.rect(screen, buttonClear.color(mx, my), buttonClear.shape())
    screen.blit(buttonClear.text, buttonClear.textRect())
    
    if buttonStar.clicked or buttonPlanet.clicked:
        pygame.draw.rect(screen, buttonSun.color(mx, my), buttonSun.shape())
        screen.blit(buttonSun.text, buttonSun.textRect())
        
        pygame.draw.rect(screen, buttonEarth.color(mx, my), buttonEarth.shape())
        screen.blit(buttonEarth.text, buttonEarth.textRect())
        
        if buttonSun.clicked:
            text3 = font.render(str(round(mStar, 2)), True, white)
        else:
            text3 = font.render(str(round(mPlanet, 2)), True, white)
        
        screen.blit(text1, (10, height - 55))
        screen.blit(text2, (10, height - 25))
        screen.blit(text3, (62, height - 25))
    
    pygame.display.flip()
    
pygame.quit()