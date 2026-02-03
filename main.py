import pgzrun, math, pygame

WIDTH, HEIGHT = 800, 600
game_state = "MENU"

class Entity:
    def __init__(self, name, x, y, ext):
        self.x, self.y, self.name, self.ext = x, y, name, ext
        self.frame, self.timer = 1, 0

    def draw(self):
        try:
            img = pygame.image.load(f"images/{self.name}{self.ext}")
            img = pygame.transform.scale(img, (80, 80))
            screen.blit(img, (self.x - 40, self.y - 40)) # type: ignore
        except:
            screen.draw.filled_circle((self.x, self.y), 20, "red") # type: ignore

class Hero(Entity):
    def update(self, target):
        dx, dy = target[0] - self.x, target[1] - self.y
        dist = math.sqrt(dx**2 + dy**2)
        self.timer += 1
        if dist > 5:
            self.x += (dx/dist) * 5; self.y += (dy/dist) * 5
            if self.timer > 8:
                self.frame = (self.frame % 3) + 1
                self.name = f"hero_walk{self.frame}"; self.timer = 0
        elif self.timer > 15:
            self.frame = (self.frame % 3) + 1
            self.name = f"hero_idle{self.frame}"; self.timer = 0

class Enemy(Entity):
    def __init__(self, name, cx, cy, r, speed):
        super().__init__(f"{name}_walk1.", cx, cy, ext=".jpg") 
        self.base, self.cx, self.cy, self.r, self.speed, self.angle = name, cx, cy, r, speed, 0

    def update(self):
        self.angle += self.speed
        self.x = self.cx + math.cos(self.angle) * self.r
        self.y = self.cy + math.sin(self.angle) * self.r
        self.timer += 1
        if self.timer > 10:
            self.frame = (self.frame % 3) + 1
            self.name = f"{self.base}_walk{self.frame}." 
            self.timer = 0

player = Hero("hero_idle1", 100, 100, ext=".png")
monster = Enemy("enemy", 400, 300, 150, 0.03) 
target_pos = [100, 100]

def draw():
    screen.clear() # type: ignore
    if game_state == "MENU":
        screen.draw.text("VOCE FOI PEGO! CLIQUE PARA RECOMECAR", center=(400, 300), fontsize=40, color="red") # type: ignore
    else:
        player.draw(); monster.draw()

def update():
    global game_state
    if game_state == "PLAYING":
        player.update(target_pos); monster.update()
        if math.sqrt((player.x - monster.x)**2 + (player.y - monster.y)**2) < 70:
            game_state = "MENU"
            # PARA A MUSICA NA COLISAO
            try: sounds.jump.stop() # type: ignore
            except: pass

def on_mouse_down(pos):
    global game_state, target_pos
    if game_state == "MENU":
        player.x, player.y = 100, 100
        target_pos = [100, 100]
        game_state = "PLAYING"
        # TENTA TOCAR EM LOOP QUANDO RECOMEÇA
        try: sounds.jump.play(-1) # type: ignore (O -1 faz a música repetir)
        except: pass
    else:
        target_pos = pos

pgzrun.go()