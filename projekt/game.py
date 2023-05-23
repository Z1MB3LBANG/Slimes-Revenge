import os 

import pygame


class Settings():
    WINDOW = pygame.rect.Rect(0, 0, 800, 400)
    FPS = 60


class Background(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/background1.png")
        self.image = pygame.transform.scale(self.image, (Settings.WINDOW.size))
        self.rect = self.image.get_rect()


class Slime(pygame.sprite.Sprite):

    def __init__(self, speedx):
        super().__init__()
        self.farbe =1
        self.change_sound = pygame.mixer.Sound("sounds/change3.wav")
        self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        self.image = pygame.image.load(f"images/player/slime{self.farbe}.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.startpos()
        self.speedx = speedx
        self.speedy = 10
        self.jumping = False
        self.sprunghöhe = 10

    
    def imagee(self, farbe):
        x,y = self.rect.left,self.rect.top
        self.image = pygame.image.load(f"images/player/slime{farbe}.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y


    def update(self):
        self.pressed = pygame.key.get_pressed()
        
        if self.pressed[pygame.K_RIGHT]:
            self.rect.left += self.speedx
            if self.pressed[pygame.K_SPACE]:
                self.jumping = True
        if self.pressed[pygame.K_LEFT]:
            self.rect.left -= self.speedx
            if self.pressed[pygame.K_SPACE]:
                self.jumping = True
        if self.pressed[pygame.K_d]:
            self.rect.left += self.speedx
            if self.pressed[pygame.K_SPACE]:
                self.jumping = True
        if self.pressed[pygame.K_a]:
            self.rect.left -= self.speedx
            if self.pressed[pygame.K_SPACE]:
                self.jumping = True    
        if self.pressed[pygame.K_SPACE]:
            self.jumping = True


        if self.rect.right > Settings.WINDOW.right:
            self.rect.right = Settings.WINDOW.right
        if self.rect.left < 0:
            self.rect.left = 0


        if self.jumping:
            self.rect.top -= self.speedy*2
            self.speedy -= 1
            #pygame.mixer.Sound.play(self.jump_sound)
            if self.speedy < -self.sprunghöhe:
                self.jumping = False
                self.speedy = self.sprunghöhe


        if self.pressed[pygame.K_c]:
            self.farbe += 1
            pygame.mixer.Sound.play(self.change_sound)
            pygame.mixer.music.stop()
            Slime.imagee(self, self.farbe)
            pygame.time.delay(1000)
            if self.farbe >= 6:
                self.farbe = 0


    def startpos(self):
        self.rect.centerx = Settings.WINDOW.centerx
        self.rect.bottom = Settings.WINDOW.height 

class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.left = True
        self.richtung = 1
        self.image = pygame.image.load(f"images/enemy/cat{self.richtung}.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.startpos()

    def imagee(self, richtung):
        x,y = self.rect.left,self.rect.top
        self.image = pygame.image.load(f"images/enemy/cat{richtung}.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        if self.left == True:
            self.richtung = 1
            Cat.imagee(self, self.richtung)
            self.rect.left -= 3
        if self.rect.left <= Settings.WINDOW.left:
            self.left = False
        if self.left == False:
            self.richtung = 2
            Cat.imagee(self, self.richtung)
            self.rect.left += 3
            if self.rect.right >= Settings.WINDOW.right:
                self.left = True


    def startpos(self):
        self.rect.right = Settings.WINDOW.right - 1
        self.rect.bottom = Settings.WINDOW.height - 1

class Watermelon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(f"images/power_ups/watermelon1.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.startpos()

    def startpos(self):
        self.rect.left = Settings.WINDOW.left +1
        self.rect.bottom = Settings.WINDOW.height - 10

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(f"images/power_ups/apple1.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.startpos()

    def startpos(self):
        self.rect.right = Settings.WINDOW.right -10
        self.rect.bottom = Settings.WINDOW.height - 1

class Timer():

    def __init__(self, duration: int, with_start: bool = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self) -> bool:
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

class Tod(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.frames: list[pygame.surface.Surface] = []
        for i in range(17):                                  
            self.ded = pygame.image.load((f"ded/frame{i}.png")).convert()
            self.ded = pygame.transform.scale(self.ded, (256, 256))
            self.frames.append(self.ded)
        self.imageindex = 0
        self.image = pygame.surface.Surface = self.frames[self.imageindex]
        self.rect = pygame.rect.Rect = self.image.get_rect()
        self.rect.center = Settings.WINDOW.center
        self.animation_time = Timer(500)

    def update(self):
        if self.animation_time.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.frames):
                self.imageindex = 0
            self.image = self.frames[self.imageindex]


class Game():

    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Slimes Revenge")
        self.clock = pygame.time.Clock()
        self.speedx = 3
        self.jum = 10
        self.slime = pygame.sprite.GroupSingle(Slime(self.speedx))
        self.cat = pygame.sprite.GroupSingle(Cat())
        self.powerupw = pygame.sprite.GroupSingle(Watermelon())
        self.powerupa = pygame.sprite.GroupSingle(Apple())
        self.slimee = Slime(self.speedx)
        self.background = pygame.sprite.GroupSingle(Background())
        self.running = False
        self.lebendig = True
        self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        self.damage_sound = pygame.mixer.Sound("sounds/damage.wav")
        self.watermelon_sound = pygame.mixer.Sound("sounds/watermelon.wav")
        self.teleport_sound = pygame.mixer.Sound("sounds/teleport.wav")
        self.tod = pygame.sprite.GroupSingle(Tod())
        #self.leben = 3


    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(Settings.FPS)
            self.watch_for_events()
            self.update()
            self.draw()
            
            
        pygame.quit()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(self.jump_sound)
                if self.lebendig == True:
                    if event.key == pygame.K_t:
                        self.slime = pygame.sprite.GroupSingle(Slime(self.speedx))
                        pygame.mixer.Sound.play(self.teleport_sound)

    def treffer(self):
        for self.identity in self.slime.sprites():
            if pygame.sprite.spritecollideany(self.identity, self.cat):
                self.identity.kill()
                pygame.mixer.Sound.play(self.damage_sound)
                self.lebendig = False


    def powerw(self):
        for identity in self.powerupw.sprites():
            if pygame.sprite.spritecollideany(identity, self.slime):
                identity.kill()
                pygame.mixer.Sound.play(self.watermelon_sound)
                self.slime.sprite.speedx += 2

    def powera(self):
        for identity in self.powerupa.sprites():
            if pygame.sprite.spritecollideany(identity, self.slime):
                identity.kill()
                pygame.mixer.Sound.play(self.watermelon_sound)
                self.slime.sprite.speedy += 2
                self.slime.sprite.sprunghöhe += 2

    def update(self):
        self.slime.update()
        self.cat.update()
        self.treffer()
        self.powerw()
        self.powera()
        if self.lebendig == False:
            self.tod.update()
        

    def draw (self):
        self.background.draw(self.screen)
        self.slime.draw(self.screen)
        self.cat.draw(self.screen)
        self.powerupw.draw(self.screen)
        self.powerupa.draw(self.screen)
        if self.lebendig == False:
            self.tod.draw(self.screen)
        pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.run()