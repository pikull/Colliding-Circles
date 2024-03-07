import asyncio, pygame, random
from math import sqrt


def distance_formula(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def obstcoll(radii_dist, radii_sum):
    return radii_dist <= radii_sum

def rrint(a, b):
    return random.randint(a, b)

def wrd(screen):
    return random.choice([
        [random.randint(5,screen.get_width()-11), 
         random.randint(5, screen.get_height()-11),
         random.randint(int(screen.get_width()/60), int(screen.get_width()/35)), 
         random.randint(5,int(screen.get_height()/1.2))],
        [random.randint(5,screen.get_width()-11),
         random.randint(5, screen.get_height()-11),
         random.randint(5, int(screen.get_width()/1.2)), 
         random.randint(int(screen.get_width()/60),int(screen.get_width()/45))]])

class SpriteSheet():
    def __init__(self, image):
            self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

class Player():

    def __init__(self, screen, x, y, color, movekeys):
        self.player_pos = pygame.Vector2(x, y)
        self.player_size = int(screen.get_width() / 75)
        self.player_speed, self.speed_mult = 10, 1
        self.color = color
        self.movekeys = movekeys
        self.coll = [False, False, False, False] #up, down, left, right

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.player_pos, self.player_size)

    def move(self):
        global sprint1, sprint2
        keys = pygame.key.get_pressed()
        if self.movekeys == "WASD":
            if keys[pygame.K_w] and not self.coll[0]:
                self.player_pos.y -= self.player_speed * self.speed_mult * dt
            if keys[pygame.K_s] and not self.coll[1]:
                self.player_pos.y += self.player_speed * self.speed_mult * dt
            if keys[pygame.K_a] and not self.coll[2]:
                self.player_pos.x -= self.player_speed * self.speed_mult * dt
            if keys[pygame.K_d] and not self.coll[3]:
                self.player_pos.x += self.player_speed * self.speed_mult * dt
            if keys[pygame.K_LSHIFT] and sprint1 > 11:
                self.speed_mult = 2.5
                sprint1 -= 10
            else:
                self.speed_mult = 1.1
                if sprint1 < 1000:
                    sprint1 += 4

        if self.movekeys == "UDLR":
            if keys[pygame.K_UP] and not self.coll[0]:
                self.player_pos.y -= self.player_speed * self.speed_mult * dt
            if keys[pygame.K_DOWN] and not self.coll[1]:
                self.player_pos.y += self.player_speed * self.speed_mult * dt
            if keys[pygame.K_LEFT] and not self.coll[2]:
                self.player_pos.x -= self.player_speed * self.speed_mult * dt
            if keys[pygame.K_RIGHT] and not self.coll[3]:
                self.player_pos.x += self.player_speed * self.speed_mult * dt
            if keys[pygame.K_SPACE] and sprint2 > 11:
                self.speed_mult = 2.5
                sprint2 -= 10
            else:
                self.speed_mult = 1
                if sprint2 < 1000:
                    sprint2 += 4


class Teleporter():

    def __init__(self, screen, pos1, pos2):
        self.pos1, self.pos2 = pygame.Vector2(pos1), pygame.Vector2(pos2)
        self.size = int(screen.get_width() / 100)
        self.delay = 90
        self.color = "white"
        self.teleporting = None

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos1, self.size)
        pygame.draw.circle(screen, self.color, self.pos2, self.size)

    def teleport(self, player):
        if 1 < self.delay:
            if obstcoll(distance_formula(player.player_pos.x, player.player_pos.y, self.pos1[0], self.pos1[1]), player.player_size + self.size):
                self.teleporting = [player, self.pos2]
            elif obstcoll(distance_formula(player.player_pos.x, player.player_pos.y, self.pos2[0], self.pos2[1]), player.player_size + self.size):
                self.teleporting = [player, self.pos1]

    def exteleport(self):
        if self.delay == 1 and self.teleporting is not None:
            self.teleporting[0].player_pos = pygame.Vector2(self.teleporting[1])
            self.delay, self.color, self.teleporting = -300, "black", None

class Landmine():

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.exploded = False
        self.size = 25
        self.scale = 1
        self.touched = False
        self.touching = False
        self.delay = 30
        self.frame = 0
        self.expdur = 53
        self.expr = (2*self.scale)

    def draw(self, screen):
        if self.exploded:
            screen.blit(landmine_sheet.get_image(1, self.size, self.size, self.scale, (0,0,0)), self.pos)
        else: screen.blit(landmine_sheet.get_image(0, self.size, self.size, self.scale, (0,0,0)), self.pos)

    def explode(self, player1, player2):
        if not self.exploded:
            if obstcoll(
                    distance_formula(player1.player_pos.x, player1.player_pos.y,
                                     self.pos[0]+(self.size*self.scale/2), self.pos[1]+(self.size*self.scale/2)),
                    player1.player_size + self.size*self.scale/2):
                self.touching, self.touched = True, True
            elif obstcoll(
                    distance_formula(player2.player_pos.x, player2.player_pos.y,
                                     self.pos[0]+(self.size*self.scale/2), self.pos[1]+(self.size*self.scale/2)),
                    player2.player_size + self.size*self.scale/2):
                self.touching, self.touched = True, True
            else: self.touching = False

    def draw_explosion(self, screen):
        screen.blit(explosion_sheet.get_image(self.frame, self.size, self.size, self.scale*8, (0,0,0)), (self.pos[0]-(self.size*self.scale*3.55), self.pos[1]-(self.size*self.scale*3.55)))

    def playerexplode(self, red, cyan):
        global room, winmsg
        if obstcoll(
                    distance_formula(cyan.player_pos.x, cyan.player_pos.y,
                                     self.pos[0]+(self.size*self.scale/2), self.pos[1]+(self.size*self.scale/2)),
                    cyan.player_size + self.expr):
            winmsg = ["Red Won (Cyan Exploded)", "red"]
        elif obstcoll(
                    distance_formula(red.player_pos.x, red.player_pos.y,
                                     self.pos[0]+(self.size*self.scale/2), self.pos[1]+(self.size*self.scale/2)),
                    red.player_size + self.expr):
            winmsg = ["Cyan Won (Red Exploded)", "cyan"]
        else: return
        room = "win"

class Wall():

    def __init__(self, data):#x, y, width, height):
        self.x, self.y = data[0], data[1]
        self.width, self.height = data[2], data[3]

    def draw(self, screen):
        pygame.draw.rect(screen, "brown", pygame.Rect(self.x, self.y, self.width, self.height))

async def main():
    pygame.init()
    pygame.display.set_caption('   Colliding Circles')
    pygame.display.set_icon(pygame.image.load('images/vikinghacks.webp'))
    height, width = int(1920 / 3), int(1080 / 3)
    screen = pygame.display.set_mode((height, width), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True
    global dt, red_pos, cyan_pos, red, cyan, room, time, scrollpos, sprint1, sprint2, tele1, explosion_sheet, landmine_sheet, titletxt, ttletxt, winmsg
    time = 60 * 60
    sprint1 = 1000
    sprint2 = 1000
    scrollpos = screen.get_width() * 1.2
    wall1 = Wall(wrd(screen))
    wall2 = Wall(wrd(screen))
    wall3 = Wall(wrd(screen))
    wall4 = Wall(wrd(screen))
    wall5 = Wall(wrd(screen))
    wall6 = Wall(wrd(screen))
    wall7 = Wall(wrd(screen))
    wall8 = Wall(wrd(screen))
    walls = [wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8]

    landmine_sheet_image = pygame.image.load('images/Landmine.png').convert_alpha()
    landmine_sheet = SpriteSheet(landmine_sheet_image)
    bomb_sheet_image = pygame.image.load('images/Bomb.png').convert_alpha()
    bomb_sheet = SpriteSheet(bomb_sheet_image)
    explosion_sheet_image = pygame.image.load('images/Explosion.png').convert_alpha()
    explosion_sheet = SpriteSheet(explosion_sheet_image)


    Startfont = pygame.font.Font('freesansbold.ttf', 50)
    Standardfont = pygame.font.Font('freesansbold.ttf', 15)
    Timefont = pygame.font.Font('freesansbold.ttf', 10)
    Winfont = pygame.font.Font('freesansbold.ttf', 32)
    winmsg = ["winmsg", "red"]

    cyan_pos = red_pos = [
        random.randint(10, screen.get_width() - 10),
        random.randint(10, screen.get_height() - 10)
    ]

    red = Player(screen, red_pos[0], red_pos[1], "red", "WASD")
    cyan = Player(screen, cyan_pos[0], cyan_pos[1], "cyan", "UDLR")
    tele1 = Teleporter(screen,\
        (random.randint(10, screen.get_width()-10),\
         random.randint(10, screen.get_height()-10)),\
        (random.randint(10, screen.get_width()-10),\
         random.randint(10, screen.get_height()-10)))
    tele2 = Teleporter(screen,\
        (random.randint(10, screen.get_width()-10),\
         random.randint(10, screen.get_height()-10)),\
        (random.randint(10, screen.get_width()-10),\
         random.randint(10, screen.get_height()-10)))
    land1 = Landmine((random.randint(10,screen.get_width()-10), random.randint(10, screen.get_height()-10)))
    
    room = "start"

    titletxt = ["press ENTER or RETURN To START", "Red: WASD to move, L_SHIFT to BOOST", "Cyan: Arrow Keys to Move, SPACE to BOOST", "There is a limited amount of Boost", "RED WINS if it tags CYAN", "Cyan WINS if time runs out", "White are teleporters", "Teleporters have a delay"]
    ttletxt = random.choice(titletxt)

    def wallcoll(wall):
        for plr in [red, cyan]:
            plr.coll[0] = bool(plr.player_pos.y - plr.player_size <= wall.y)
            plr.coll[1] = bool(plr.player_pos.y + plr.player_size >= wall.y + wall.height)
            plr.coll[2] = bool(plr.player_pos.x - plr.player_size <= wall.x)
            plr.coll[3] = bool(plr.player_pos.x + plr.player_size >= wall.x + wall.width)

    def somewallscoll(obst):
        for plr in [red, cyan]:
            plr.coll[0] = bool(obst.y <= plr.player_pos.y - plr.player_size <= obst.y + obst.height and obst.x <= plr.player_pos.x <= obst.x + obst.width) if not plr.coll[0] else True
            plr.coll[1] = bool(obst.y <= plr.player_pos.y + plr.player_size <= obst.y + obst.height and obst.x <= plr.player_pos.x <= obst.x + obst.width) if not plr.coll[1] else True
            plr.coll[2] = bool(obst.x <= plr.player_pos.x - plr.player_size <= obst.x + obst.width and obst.y <= plr.player_pos.y <= obst.y + obst.height) if not plr.coll[2] else True
            plr.coll[3] = bool(obst.x <= plr.player_pos.x + plr.player_size <= obst.x + obst.width and obst.y <= plr.player_pos.y <= obst.y + obst.height) if not plr.coll[3] else True

    def explodeplayer():
        if land1.exploded:
            if 49 < land1.expdur:
                land1.frame = 0
            elif 45 < land1.expdur <= 49:
                land1.frame, land1.expr = 1, (6*land1.scale)
            elif 41 < land1.expdur <= 45:
                land1.frame, land1.expr = 2, (18*land1.scale)
            elif 37 < land1.expdur <= 41:
                land1.frame, land1.expr = 3, (32*land1.scale)
            elif 33 < land1.expdur <= 37:
                land1.frame, land1.expr = 4, (48*land1.scale)
            elif 27 < land1.expdur <= 33:
                land1.frame, land1.expr = 5, (62*land1.scale)
            elif 19 < land1.expdur <= 27:
                land1.frame, land1.expr = 6, (74*land1.scale)
            elif 10 < land1.expdur <= 19:
                land1.frame, land1.expr = 7, (86*land1.scale)
            elif 0 < land1.expdur <= 10:
                land1.frame, land1.expr = 8, (110*land1.scale)
            else:
                return
            land1.playerexplode(red, cyan)
            land1.expdur -= 1
            land1.draw_explosion(screen)
    
    def win():
        if obstcoll(
                distance_formula(red.player_pos.x, red.player_pos.y,
                                 cyan.player_pos.x, cyan.player_pos.y),
            (red.player_size+cyan.player_size)):
            global room, winmsg, time
            winmsg = ["Red Won (Cyan Tagged)", "red"]
        elif time == 0: winmsg = ["Cyan Won (Timer)", "cyan"]
        else:
            time -= 1
            return
        room = "win"

    def instscrollleft():
        global scrollpos, ttletxt
        if scrollpos > 0 - screen.get_width() * 1.2:
            scrollpos = scrollpos - 1
        else:
            scrollpos = screen.get_width() * 1.2
            ttletxt = random.choice(titletxt)
        return (scrollpos, screen.get_height() - 10)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if room == "start":
            screen.fill("black")
            button = Startfont.render('Press ENTER', True, "white", "black")
            button_rect = button.get_rect()
            button_rect.center = (screen.get_width() // 2,
                                  screen.get_height() // 2)
            screen.blit(button, button_rect)
            insts = Standardfont.render(ttletxt, True, "white", "black")
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
            
            for wall in walls:
                somewallscoll(wall)
            
            red.move()
            cyan.move()
            
            for drawitem in [tele1, tele2, land1, red, cyan]:
                drawitem.draw(screen)
            CyanSB = pygame.draw.rect(screen, "orange", pygame.Rect(cyan.player_pos.x - int(sprint2/25), cyan.player_pos.y, int(sprint2/cyan.player_size/5), 2))
            RedSB = pygame.draw.rect(screen, "orange", pygame.Rect(red.player_pos.x - int(sprint1/25), red.player_pos.y, int(sprint1/red.player_size/5), 2))
            text = Timefont.render(f"Time Remaining: {str(int(time / 60))}", True, "red", "purple")
            textRect = text.get_rect()
            screen.blit(text, textRect)
            
            win()
            
            for tp in [tele1, tele2]:
                if 1 < tp.delay and tp.teleporting is not None:
                    tp.delay -= 1
                elif tp.delay == 1:
                    tp.exteleport()
                elif tp.delay < 0 and tp.teleporting is None:
                    tp.delay +=1
                else:
                    tp.color = "white"
                    tp.delay = 90

            if land1.touched and not land1.touching:
                if land1.delay > 0:
                    land1.delay -= 1
                else:
                    land1.exploded = True

            explodeplayer()
            tele1.teleport(red)
            tele1.teleport(cyan)
            tele2.teleport(red)
            tele2.teleport(cyan)
            land1.explode(red, cyan)
            
            for wall in walls:
                wall.draw(screen)

        elif room == "win":
            screen.fill("black")
            text = Winfont.render(winmsg[0], True, winmsg[1], "purple")
            textRect = text.get_rect()
            textRect.center = (screen.get_width() // 2, screen.get_height() // 2)
            screen.blit(text, textRect)
            red.draw(screen)
            cyan.draw(screen)
            insts = Standardfont.render("press ENTER or RETURN To RESTART", True, "white", "black")
            insts_rect = insts.get_rect()
            insts_rect.center = (screen.get_width() // 2, screen.get_height()/5)
            screen.blit(insts, insts_rect)
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                red.player_pos, cyan.player_pos = pygame.Vector2(random.randint(11,screen.get_width() - 11),random.randint(11,screen.get_height() - 11)), pygame.Vector2(random.randint(11,screen.get_width() - 11),random.randint(11,screen.get_height() - 11))
                land1.expdur, land1.exploded, land1.touched, land1.touching = 53, False, False, False
                land1.frame, land1.expr = 0, (1*land1.scale)/2
                tele1.teleporting = tele2.teleporting = None
                tele1.delay = tele2.delay = 90
                sprint1, sprint2, time, room = 1000, 1000, 60 * 60, "game"

        pygame.display.flip()
        dt = clock.tick(60) / 100
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
