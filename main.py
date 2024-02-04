import asyncio, pygame, random, threading
from math import sqrt


class Player():
    def __init__(self, screen, x, y, color, movekeys):
        self.player_pos = pygame.Vector2(x, y)
        self.player_size = int(screen.get_width() / 75)
        self.player_speed = 10
        self.speed_mult = 1
        self.color = color
        self.movekeys = movekeys

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.player_pos, self.player_size)

    def move(self, coll):
        global sprint1, sprint2
        keys = pygame.key.get_pressed()
        if self.movekeys == "WASD":
            if keys[pygame.K_w] and not coll[0]:
                self.player_pos.y -= self.player_speed * self.speed_mult * dt
            if keys[pygame.K_s] and not coll[1]:
                self.player_pos.y += self.player_speed * self.speed_mult * dt
            if keys[pygame.K_a] and not coll[2]:
                self.player_pos.x -= self.player_speed * self.speed_mult * dt
            if keys[pygame.K_d] and not coll[3]:
                self.player_pos.x += self.player_speed * self.speed_mult * dt
            if keys[pygame.K_LSHIFT]: #and sprint1 > 0:
                self.speed_mult = 2.5
                #sprint1 -= 5
            else:
                self.speed_mult = 1
                #sprint1 += 10
            
        if self.movekeys == "UDLR":
            if keys[pygame.K_UP] and not coll[0]:
                self.player_pos.y -= self.player_speed * self.speed_mult * dt
            if keys[pygame.K_DOWN] and not coll[1]:
                self.player_pos.y += self.player_speed * self.speed_mult * dt
            if keys[pygame.K_LEFT] and not coll[2]:
                self.player_pos.x -= self.player_speed * self.speed_mult * dt
            if keys[pygame.K_RIGHT] and not coll[3]:
                self.player_pos.x += self.player_speed * self.speed_mult * dt
            if keys[pygame.K_SPACE]:# and sprint2 > 0:
                self.speed_mult = 2.5
                #sprint2 -= 5
            else:
                self.speed_mult = 1
                #sprint2 += 10

async def main():
    pygame.init()
    pygame.display.set_caption('   Colliding Circles')
    pygame.display.set_icon(pygame.image.load('vikinghacks.webp')
)
    height, width = 1000/2, 1000/2
    screen = pygame.display.set_mode((height, width), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True
    global dt, red_pos, cyan_pos, red, cyan, redcoll, cyancoll, room, time, wall1pos, scrollpos, time, sprint1, sprint2
    time = 20 * 60
    sprint1 = 100
    sprint2 = 100
    scrollpos = screen.get_width()*2.6
    wall1e = {
        "x" : random.randint(5, screen.get_width()-11),
        "y" : random.randint(5,screen.get_height()-11),
        "width" : random.randint(5,screen.get_width()-11),
        "height" : random.randint(5,screen.get_height()-11)}
    
    Startfont = pygame.font.Font('freesansbold.ttf', 50)
    Standardfont = pygame.font.Font('freesansbold.ttf', 15)
    Timefont = pygame.font.Font('freesansbold.ttf', 10)
    Winfont = pygame.font.Font('freesansbold.ttf', 32)
    
    red_pos = [random.randint(10, screen.get_height()-10), random.randint(10,screen.get_width()-10)]
    cyan_pos = [random.randint(10, screen.get_height()-(10+red_pos[0])), random.randint(10,screen.get_width()-(10+red_pos[1]))]

    red = Player(screen, red_pos[0], red_pos[1], "red", "WASD")
    cyan = Player(screen, cyan_pos[0], cyan_pos[1], "cyan", "UDLR")
    red_mask = pygame.mask.from_surface(pygame.Surface((red.player_size, red.player_size)))
    cyan_mask = pygame.mask.from_surface(pygame.Surface((cyan.player_size, cyan.player_size)))
    
    room = "start"
    
    redcoll = [False, False, False, False] # up, down, left, right
    cyancoll = [False, False, False, False] # up, down, left, right

    def wallcoll(wall):
        redcoll[0] = bool(red.player_pos.y - red.player_size <= wall.y)
        redcoll[1] = bool(red.player_pos.y + red.player_size >= wall.y + wall.height)
        redcoll[2] = bool(red.player_pos.x - red.player_size <= wall.x)
        redcoll[3] = bool(red.player_pos.x + red.player_size >= wall.x + wall.width)
        cyancoll[0] = bool(cyan.player_pos.y - cyan.player_size <= wall.y)
        cyancoll[1] = bool(cyan.player_pos.y + cyan.player_size >= wall.y + wall.height)
        cyancoll[2] = bool(cyan.player_pos.x - cyan.player_size <= wall.x)
        cyancoll[3] = bool(cyan.player_pos.x + cyan.player_size >= wall.x + wall.width)

    #def obstaclecoll(obst):
        #redcoll[0] = bool(red.player_pos.y - red.player_size <= obst.y+obst.height and red.player_pos.y - red.player_size >= obst.y)
        
    def distance_formula(x1, y1, x2, y2):
        answer = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return answer

    def obstcoll(radii_dist, radii_sum):
        return radii_dist <= 2*radii_sum
    
    def win():
        if obstcoll(distance_formula(red.player_pos.x, red.player_pos.y, cyan.player_pos.x, cyan.player_pos.y), (red.player_size)):
            global room
            room = "win1"

    def countdown():
        global time, room
        time -= 1
        if time <= 0:
            room = "win2"
    
    def instscrollleft():
        global scrollpos
        scrollpos = scrollpos - 1 if scrollpos > 0-screen.get_width()*2.6 else screen.get_width()*2.6
        return (scrollpos, screen.get_height()-10)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if room == "start":
            screen.fill("black")
            button = Startfont.render('Press ENTER', True, "white", "black")
            button_rect = button.get_rect()
            button_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
            screen.blit(button, button_rect)
            insts = Standardfont.render("""
            Press 'Enter' to start
            Red: WASD to move, L_SHIFT to boost
            Cyan: Arrow Keys to Move, SPACE to boost
            There is a limited amount of boost
            Cyan wins if time runs out""",\
            True, "white", "black")
            insts_rect = insts.get_rect()
            insts_rect.center = instscrollleft()
            screen.blit(insts, insts_rect)
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                room = "game"

        if room == "game":
            screen.fill("white")
            bg_rect = pygame.Rect(5, 5, screen.get_width() - 10, screen.get_height() - 10)
            pygame.draw.rect(screen, (125, 101, 255), bg_rect)
            wallcoll(bg_rect)
            #wall1 = pygame.draw.rect(screen, "black", pygame.Rect(wall1e["x"], wall1e["y"], wall1e["width"], wall1e["height"]))
            
            red.move(redcoll)
            cyan.move(cyancoll)
            win()
            countdown()
            text = Timefont.render("Time Remaining: " + str(int(time/60)), True, "red", "purple")
            textRect = text.get_rect()
            screen.blit(text, textRect)
            red.draw(screen)
            cyan.draw(screen)
            
        elif room == "win1":
            screen.fill("black")
            text = Winfont.render('Red Won', True, "red", "purple")
            textRect = text.get_rect()
            textRect.center = (screen.get_width() // 2, screen.get_height() // 2)
            screen.blit(text, textRect)
            red.draw(screen)
            cyan.draw(screen)
        elif room == "win2":
            screen.fill("black")
            text = Winfont.render('Cyan Won', True, "cyan", "purple")
            textRect = text.get_rect()
            textRect.center = (screen.get_width() // 2, screen.get_height() // 2)
            screen.blit(text, textRect)
            red.draw(screen)
            cyan.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(60) / 100
        await asyncio.sleep(0)

    pygame.quit()

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()
