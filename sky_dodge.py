import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.shield = False
        self.changed_controls = False

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update_changed_controls(self, pressed_keys):
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self, shield):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

        if player.shield == True:
            if pygame.sprite.spritecollide(shield, enemies, True):
                self.kill()
                shield.kill()
                player.shield = False

    def update2(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Shield, self).__init__()
        self.surf = pygame.image.load("images/shield.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.rect = self.surf.get_rect(
            center=(
                player.rect.center
            )
        )

    def update(self, player):
        if player.shield == True:
            self.rect = self.surf.get_rect(
                center=(
                    player.rect.center
                )
            )
        else:
            shield.kill()


class RandomPower(pygame.sprite.Sprite):
    def __init__(self):
        super(RandomPower, self).__init__()
        self.surf = pygame.image.load("images/question-mark.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (40, 40))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


pygame.mixer.init()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDRANDOMPOWER = pygame.USEREVENT + 3
pygame.time.set_timer(ADDRANDOMPOWER, 1000)

player = Player()

effect_3 = False

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
random_power = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.01)

move_up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sound/Boom.ogg")

move_up_sound.set_volume(0.01)
move_down_sound.set_volume(0.01)
collision_sound.set_volume(0.01)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == ADDRANDOMPOWER:
            new_random_power = RandomPower()
            random_power.add(new_random_power)
            all_sprites.add(new_random_power)


    pressed_keys = pygame.key.get_pressed()
    if player.changed_controls == False:
        player.update(pressed_keys)
    else:
        player.update_changed_controls(pressed_keys)

    if player.shield == True:
        enemies.update(shield)
        shield.update(player)
    else:
        for enemy in enemies:
            enemy.update2()


    clouds.update()
    random_power.update()

    if effect_3 == False:
        screen.fill((135, 206, 250))
    else:
        screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollide(player, random_power, True):
        random_effect = random.randint(1, 3)
        if random_effect == 1:
            print("Shield")
            player.changed_controls = False
            effect_3 = False
            player.shield = True
            shield = Shield(player)
            shield.update(player)
        elif random_effect == 2:
            print("Changed controls")
            player.shield = False
            effect_3 = False
            player.changed_controls = True
        else:
            print("Blik blik")
            player.shield = False
            player.changed_controls = False
            effect_3 = True


    if player.shield == True:
        screen.blit(shield.surf, shield.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

        move_up_sound.stop()
        move_down_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        collision_sound.play()
        pygame.time.delay(500)

        running = False

    pygame.display.flip()

    clock.tick(60)

pygame.mixer.quit()
