import math

G = 6.67408E-11
dCollision = 6E9

dScale = 1.5E9  #number of meters per pixel
tScale = 5E3    #number of seconds per milisecond
vScale = 6E2    #number of m/s per dragged pixel

white = (255, 255, 255)
black = (0, 0, 0)

gray1 = (170, 170, 170)
gray2 = (100, 100, 100)

class Star:
    def __init__(self, x, y, m):
        self.x = x
        self.y = y
        self.m = m
        
class Planet:
    collided = False
    
    def __init__(self, x, y, vx, vy, m):
        self.x = x
        self.y = y
        self.m = m
        self.vx = vx
        self.vy = vy
    
    def setVelocity(self, x1, y1):
        self.vx = (x1 - self.x) * vScale
        self.vy = (y1 - self.y) * vScale
        
    def gravity(self, stars, planets, dt):
        for i in range(len(stars)):
            rx = (self.x - stars[i].x) * dScale
            ry = (self.y - stars[i].y) * dScale
            r = math.sqrt((rx ** 2 + ry ** 2))
            
            F = -G * stars[i].m * self.m / (r ** 2)
            ax = F * rx / r / self.m
            ay = F * ry / r / self.m
            
            if r < dCollision:
                self.collided = True
            
            self.vx = self.vx + ax * dt * tScale
            self.vy = self.vy + ay * dt * tScale
            
        for i in range(len(planets)):
            if not planets[i].collided:
                rx = (self.x - planets[i].x) * dScale
                ry = (self.y - planets[i].y) * dScale
                r = math.sqrt((rx ** 2 + ry ** 2))
                
                if(r != 0):
                    F = -G * planets[i].m * self.m / (r ** 2)
                    ax = F * rx / r / self.m
                    ay = F * ry / r / self.m
                    
                    if r < dCollision:
                        planets[i].collided = True
                        self.collided = True
                    
                    self.vx = self.vx + ax * dt * tScale
                    self.vy = self.vy + ay * dt * tScale
        
    def move(self, dt):
        self.x = self.x + self.vx * dt * tScale / dScale
        self.y = self.y + self.vy * dt * tScale / dScale
        
        return (self.x, self.y)
        
class Button:
    clicked = False
    
    def __init__(self, x, y, width, height, font, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = font.render(text, True, white)
        
    def hovering(self, mx, my):
        if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
            return True
        else:
            return False
        
    def color(self, mx, my):
        if self.hovering(mx, my) or self.clicked:
            return gray1
        else:
            return gray2
    
    def shape(self):
        return (self.x, self.y, self.width, self.height)
    
    def textRect(self):
        return self.text.get_rect(center = (self.x + self.width / 2, self.y + self.height / 2 + 1))
        