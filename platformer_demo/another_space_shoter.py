import pgzrun
import random

WIDTH = 1200
HEIGHT = 800

difficulty = 1
lives = 5
score = 0
count = 0
level = 1
speed = 8
start = False
mission = False

button_start = Rect((405, 480), (385, 85))
button_exit = Rect((405, 635), (385, 85))

button_reset = Rect((140, 615), (385, 85))
button_menu = Rect((675, 615), (385, 85))
button_continue = Rect((820, 25), (300, 85))

menu = Actor("menu_image.png", (WIDTH // 2, HEIGHT // 2))

background_1 = Actor("background_1.png", (1760 // 2, HEIGHT // 2))
background_2 = Actor("background_2.png", (1760 // 2 + 1760, HEIGHT // 2))

aircraft = Actor("aircraft.png", (150, HEIGHT // 2))

meteor_1 = Actor("meteor.png", (WIDTH, HEIGHT // 2))
meteor_2 = Actor("meteor.png", (WIDTH + 900, HEIGHT // 2))
stone_1 = Actor("stone.png", (WIDTH , HEIGHT // 2))
stone_2 = Actor("stone.png", (WIDTH , HEIGHT // 2))

repair = Actor("repair.png", (10000, random.randint(150, 650)))

star = Actor("star.png", (3000, random.randint(150, 650)))

game_over = Actor("game_over.png", (WIDTH // 2, HEIGHT // 2))

spaceship = Actor("inside_spaceship.png", (WIDTH // 2, HEIGHT // 2))
message = Actor("message.png", (WIDTH // 2, HEIGHT // 2))
person_1 = Actor("person_1.png", (1005, 310))
person_2 = Actor("person_2.png", (100, 450))

def reset_game():
    global difficulty, lives, score, count, level, speed, start, mission, background_1, background_2, aircraft, meteor_1, meteor_2, stone_1, stone_2, repair, star

    difficulty = 1
    lives = 5
    score = 0
    count = 0
    level = 1
    speed = 8
    mission = False

    background_1 = Actor("background_1.png", (1760 // 2, HEIGHT // 2))
    background_2 = Actor("background_2.png", (1760 // 2 + 1760, HEIGHT // 2))
    aircraft = Actor("aircraft.png", (150, HEIGHT // 2))
    meteor_1 = Actor("meteor.png", (WIDTH, HEIGHT // 2))
    meteor_2 = Actor("meteor.png", (WIDTH + 900, HEIGHT // 2))
    stone_1 = Actor("stone.png", (WIDTH , HEIGHT // 2))
    stone_2 = Actor("stone.png", (WIDTH , HEIGHT // 2))
    repair = Actor("repair.png", (10000, random.randint(150, 650)))
    star = Actor("star.png", (3000, random.randint(150, 650)))

def draw():
    screen.clear()

    if not start:
        menu.draw()
        screen.draw.rect(button_start, 'black')
        screen.draw.rect(button_exit, 'black')
        screen.draw.text("Start Game", center=button_start.center, color='black', fontsize=50)
        screen.draw.text("Exit the Game", center=button_exit.center, color='black', fontsize=50)

    elif start:
        if lives > 0:
            background_1.draw()
            background_2.draw()
            aircraft.draw()
            meteor_1.draw()
            meteor_2.draw()
            repair.draw()
            star.draw()
            if difficulty > 3:
                stone_1.draw()
            if difficulty > 4:
                stone_2.draw()

            if aircraft.left > 1200:
                music.stop()
                spaceship.draw()
                message.draw()
                person_1.draw()
                person_2.draw()
                screen.draw.rect(button_continue, 'black')
                screen.draw.text("Continue", center=button_continue.center, color='black', fontsize=50)

                if mission:
                    game_over.draw()
                    screen.draw.text("MISSION PASS", color="Green", center=(WIDTH // 2, 250), fontsize=200)
                    screen.draw.text(f"FINAL SCORE: {score}", color="Black", center=(WIDTH // 2, 400), fontsize=90)
                    screen.draw.rect(button_reset, 'black')
                    screen.draw.rect(button_menu, 'black')
                    screen.draw.text("Play Again", center=button_reset.center, color='black', fontsize=50)
                    screen.draw.text("Go to menu", center=button_menu.center, color='black', fontsize=50)

            else:
                screen.draw.text(f"Score: {score}", color="White", topleft=(10, 20), fontsize=40)
                screen.draw.text(f"Lives: {lives}", color="White", topleft=(10, 50), fontsize=40)
                screen.draw.text(f"LEVEL: {level}", (500, 20), color="White", fontsize=100)

        elif lives == 0:
            music.stop()
            game_over.draw()
            screen.draw.text("MISSION FAIL", color="Red", center=(WIDTH // 2, 250), fontsize=200)
            screen.draw.text(f"FINAL SCORE: {score}", color="Black", center=(WIDTH // 2, 400), fontsize=90)
            screen.draw.rect(button_reset, 'black')
            screen.draw.rect(button_menu, 'black')
            screen.draw.text("Play Again", center=button_reset.center, color='black', fontsize=50)
            screen.draw.text("Go to menu", center=button_menu.center, color='black', fontsize=50)

def on_mouse_down(pos):
    global start, mission

    if button_start.collidepoint(pos):
        start = True
        play_music()

    elif button_reset.collidepoint(pos):
        reset_game()
        start = True
        mission = False
        play_music()

    elif button_menu.collidepoint(pos):
        reset_game()
        start = False

    elif button_continue.collidepoint(pos):
        start = True
        mission = True

    elif button_exit.collidepoint(pos):
        exit()

def get_x(meteor):
    if meteor == meteor_1:
        return meteor_1.x
    elif meteor == meteor_2:
        return meteor_2.x

def update():
    global lives, score, count, level, speed, difficulty, start

    if not start or mission:
        return

    if lives == 0:
        return

    if aircraft.left > 1200:
        return

    if count == 10 * difficulty and difficulty < 3:
        difficulty += 1
        level += 1
    if count == 15 * difficulty and difficulty >= 3:
        difficulty += 1
        level += 1

    if 1 < difficulty < 4:
        speed = difficulty * 6

    elif difficulty >= 4:
        speed = 15

    if difficulty <= 5 :
        background_1.x -= 5

        if background_1.right < 1:
            background_1.left = 1760

        background_2.x -= 5

        if background_2.right < 1:
            background_2.left = 1760

    elif difficulty > 5:
        aircraft.x += 4

    meteor_1.x -= speed

    if meteor_1.right < 1 and aircraft.right < 400:
        meteor_2_x = get_x(meteor_2)
        meteor_1.x = meteor_2_x + 900
        meteor_1.y = random.randint(150, 650)
        score += 2
        count += 1

    meteor_2.x -= speed

    if meteor_2.right < 1 and aircraft.right < 400:
        meteor_x = get_x(meteor_1)
        meteor_2.x = meteor_x + 900
        meteor_2.y = random.randint(150, 650)
        score += 2
        count += 1

    repair.x -= speed

    if repair.right < 1:
        repair.left = 10000
        repair.y = random.randint(150, 650)

    if difficulty > 3 :
        stone_1.x -= speed

        if stone_1.right < 1 and aircraft.right < 400:
            meteor_x = get_x(meteor_1)
            stone_1.x = meteor_x + 450
            stone_1.y = random.randint(150, 650)
            score += 5

    if difficulty > 4 :
        stone_2.x -= speed

        if stone_2.right < 1 and aircraft.right < 400:
            meteor_2_x = get_x(meteor_2)
            stone_2.x = meteor_2_x + 450
            stone_2.y = random.randint(150, 650)
            score += 5

    star.x -= speed

    if star.right < 1:
        star.left = 3000
        star.y = random.randint(150, 650)

    if meteor_1.colliderect(aircraft):
        meteor_2_x = get_x(meteor_2)
        meteor_1.x = meteor_2_x + 900
        meteor_1.y = random.randint(150, 650)
        lives -= 1
        sounds.crashing_sound.play()

    if meteor_2.colliderect(aircraft):
        meteor_x = get_x(meteor_1)
        meteor_2.x = meteor_x + 900
        meteor_2.y = random.randint(150, 650)
        lives -= 1
        sounds.crashing_sound.play()

    if repair.colliderect(aircraft):
        repair.x = 10000
        repair.y = random.randint(150, 650)
        if lives < 5:
            lives += 1
        else:
            score += 5
        sounds.repair_sound.play()

    if difficulty > 3 and stone_1.colliderect(aircraft):
        meteor_x = get_x(meteor_1)
        stone_1.x = meteor_x + 450
        stone_1.y = random.randint(150, 650)
        lives -= 1
        sounds.crashing_sound.play()

    if difficulty > 4 and stone_2.colliderect(aircraft):
        meteor2_x = get_x(meteor_2)
        stone_2.x = meteor2_x + 450
        stone_2.y = random.randint(150, 650)
        lives -= 1
        sounds.crashing_sound.play()

    if star.colliderect(aircraft):
        star.x = 3000
        star.y = random.randint(150, 650)
        score += 10
        sounds.star_sound.play()

    if keyboard.down:
        if aircraft.y < 650:
            aircraft.y += 10

    elif keyboard.up:
        if aircraft.y > 150:
            aircraft.y -= 10

def play_music():
    music.play("aircraft_sound")
    music.set_volume(1.0)

pgzrun.go()
