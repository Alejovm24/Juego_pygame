import pygame
import random

pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("THE SURVIVAL OF THE SNAKE")
clock = pygame.time.Clock()

background_image = pygame.image.load("C:/Users/josea/Documents/Pygame/portada.png")
background_image = pygame.transform.scale(background_image, (width, height))
background_image_start_game = pygame.image.load("C:/Users/josea/Documents/Pygame/arena.png")
background_image_start_game = pygame.transform.scale(background_image_start_game, (width, height))

def apply_brightness_to_screen():
    dark_surface = pygame.Surface(screen.get_size()).convert_alpha()
    dark_surface.fill((brillo, brillo, brillo))  
    screen.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

def draw_background():
    screen.blit(background_image_start_game, (0, 0))  
    apply_brightness_to_screen()

arena_left   = 60
arena_top    = 90
arena_right  = width - 30
arena_bottom = height - 90
# Variables de configuración
dificultad = 0  # 0 = Fácil, 1 = Medio, 2 = Difícil
brillo = 100  # Brillo entre 0 y 100

# Función para ajustar el brillo de los colores
def apply_brightness(color):
    factor = brillo / 100  
    return (int(color[0] * factor), int(color[1] * factor), int(color[2] * factor))

def get_colors():
    return {
        "WHITE": apply_brightness((255, 255, 255)),
        "BLUE": apply_brightness((50, 150, 255)),
        "GRAY": apply_brightness((170, 170, 170)),
        "BLACK": apply_brightness((0, 0, 0)),
        "RED": apply_brightness((174, 0, 0)),
        "GREEN": apply_brightness((0, 84, 0)),
    }

FONT = pygame.font.Font(None, 80)

# Clase para botones
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, get_colors()["RED"], self.rect, border_radius=10)
        text_render = FONT.render(self.text, True, get_colors()["WHITE"])
        screen.blit(text_render, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def show_settings():
    global dificultad, brillo
    buttons = [
        Button(width // 2 - 300, height // 2 - 150, 160, 70, "Fácil", lambda: set_difficulty(0)),
        Button(width // 2 - 70, height // 2 - 150, 180, 70, "Medio", lambda: set_difficulty(1)),
        Button(width // 2 + 180, height // 2 - 150, 180, 70, "Difícil", lambda: set_difficulty(2)),
        Button(width // 2 - 300, height // 2 + 100, 350, 70, "Menos brillo", lambda: adjust_brightness(-10)),
        Button(width // 2 + 170, height // 2 + 100, 270, 70, "Más brillo", lambda: adjust_brightness(10)),
        Button(width // 2 - 75, height // 2 + 280, 190, 70, "Volver", lambda: exit_settings()) # Nuevo botón
    ]

    running = True
    while running:
       
        screen.fill( get_colors()["GREEN"])
        difficulty_text = FONT.render("Dificultad:", True, get_colors()["WHITE"])
        brightness_text = FONT.render("Brillo:", True, get_colors()["WHITE"])
        difficulty_level = FONT.render(["Fácil", "Medio", "Difícil"][dificultad], True, get_colors()["WHITE"])
        brightness_level = FONT.render(str(brillo), True, get_colors()["WHITE"])

        screen.blit(difficulty_text, (200, 100))
        screen.blit(brightness_text, (200, 400))
        screen.blit(difficulty_level, (550, 100))
        screen.blit(brightness_level, (550, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            for button in buttons:
                if button.is_clicked(event):
                    button.action()

        for button in buttons:
            button.draw()

        pygame.display.flip()

def exit_settings():
    main_menu()  

# Funciones de configuración
def set_difficulty(level):
    global dificultad
    dificultad = level

def adjust_brightness(amount):
    global brillo
    brillo = max(0, min(100, brillo + amount))  
# Clase para la serpiente
class Snake:
    def __init__(self):
        self.body = [[width//2, height//2]]
        self.direction = (20, 0)  
        self.size = 20

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.direction != (20, 0):  
            self.direction = (-20, 0)
        if keys[pygame.K_RIGHT] and self.direction != (-20, 0):
            self.direction = (20, 0)
        if keys[pygame.K_UP] and self.direction != (0, 20):
            self.direction = (0, -20)
        if keys[pygame.K_DOWN] and self.direction != (0, -20):
            self.direction = (0, 20)

        head = self.body[0][:]
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], self.size, self.size))

    def check_collision(self, enemies):
        head_rect = pygame.Rect(self.body[0][0], self.body[0][1], self.size, self.size)
        for enemy in enemies:
            if isinstance(enemy, Turtle):
                img = turtle_img
            elif isinstance(enemy, Crab):
                img = crab_img
            elif isinstance(enemy, Crocodile):
                img = crocodile_img
            else:
                continue
            # Reducir el área de colisión 
            w, h = img.get_width(), img.get_height()
            shrink_factor = 0.8  
            new_w, new_h = int(w * shrink_factor), int(h * shrink_factor)
            offset_x = (w - new_w) // 2
            offset_y = (h - new_h) // 2
            enemy_rect = pygame.Rect(
                enemy.position[0] + offset_x,
                enemy.position[1] + offset_y,
                new_w, new_h
            )
            if head_rect.colliderect(enemy_rect):
                return True
        return False

# Clase para la manzana
class Apple:
    def __init__(self):
        self.size = 30  
        self.position = [
            random.randrange(arena_left, arena_right - self.size + 1, self.size),
            random.randrange(arena_top, arena_bottom - self.size + 1, self.size)
        ]

    def draw(self):
        screen.blit(apple_img, (self.position[0], self.position[1]))

# Cuando la serpiente come la manzana:
# if snake_head_rect.colliderect(apple_rect):
#     snake.grow()
#     puntaje += 10
#     apple.position = [
#         random.randrange(arena_left, arena_right - apple.size + 1, apple.size),
#         random.randrange(arena_top, arena_bottom - apple.size + 1, apple.size)
#     ]

# Clases para enemigos
class Turtle:
    def __init__(self):
        self.position = [random.randint(arena_left, arena_right-40), random.randint(arena_top, arena_bottom-40)]
        self.speed = 2

    def move(self):
        self.position[1] += self.speed
        if self.position[1] > arena_bottom - 40 or self.position[1] < arena_top:
            self.speed *= -1

    def draw(self):
        screen.blit(turtle_img, (self.position[0], self.position[1]))

class Crab:
    def __init__(self):
        self.position = [random.randint(arena_left, arena_right-40), random.randint(arena_top, arena_bottom-40)]
        self.speed = random.choice([-4, 4])

    def move(self):
        self.position[0] += self.speed
        if self.position[0] > arena_right - 40 or self.position[0] < arena_left:
            self.speed *= -1

    def draw(self):
        screen.blit(crab_img, (self.position[0], self.position[1]))

class Crocodile:
    def __init__(self):
        self.position = [random.randint(arena_left, arena_right-125), random.randint(arena_top, arena_bottom-125)]
        self.speed = random.choice([-6, 6])

    def move(self):
        self.position[0] += self.speed
        if self.position[0] > arena_right - 125 or self.position[0] < arena_left:
            self.speed *= -1

    def draw(self):
        screen.blit(crocodile_img, (self.position[0], self.position[1]))

# Cargar imágenes para enemigos (esto debe estar antes de usarlas)
crab_img = pygame.image.load("C:/Users/josea/Documents/Pygame/crab.png")
turtle_img = pygame.image.load("C:/Users/josea/Documents/Pygame/turtle.png")
crocodile_img = pygame.image.load("C:/Users/josea/Documents/Pygame/crocodile.png")
apple_img= pygame.image.load("C:/Users/josea/Documents/Pygame/apple.png")

# Configuración de enemigos según dificultad
def create_enemies():
    enemies = [Turtle()]
    if dificultad >= 1:
        enemies.append(Crab())
    if dificultad == 2:
        enemies.append(Crocodile())
    return enemies

def pause_menu():
    resume_button = Button(width // 2 - 180, height // 2 - 50, 350, 70, "REANUDAR", None)
    menu_button = Button(width // 2 - 100, height // 2 + 50, 180, 70, "MENÚ", None)
    paused = True
    while paused:
        screen.fill(get_colors()["GREEN"])
        pause_text = FONT.render("PAUSA", True, get_colors()["WHITE"])
        screen.blit(pause_text, (width // 2 - 100, height // 2 - 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if resume_button.is_clicked(event):
                paused = False
            if menu_button.is_clicked(event):
                main_menu()
                return
        resume_button.draw()
        menu_button.draw()
        pygame.display.flip()
        clock.tick(10)


def start_game():
    global puntaje  
    puntaje=0
    snake = Snake()
    apple = Apple()
    enemies = create_enemies()
    pause_button = Button(width - 220, 20, 320, 70, "PAUSA", None)

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_background()
       
        
        keys = pygame.key.get_pressed()
        snake.move(keys)

        # Comprobar si la serpiente toca el muro de la arena
        head_x, head_y = snake.body[0]
        if (
            head_x < arena_left or
            head_x + snake.size > arena_right or
            head_y < arena_top or
            head_y + snake.size > arena_bottom
        ):
            running = False  # Pierde si toca el muro

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if pause_button.is_clicked(event):
                pause_menu()

        apple.draw()
        snake.draw()
        pause_button.draw()

        for enemy in enemies:
            enemy.move()
            enemy.draw()

        if snake.check_collision(enemies):
            running = False  

        if pygame.Rect(snake.body[0][0], snake.body[0][1], snake.size, snake.size).colliderect(pygame.Rect(apple.position[0], apple.position[1], 30, 30)):
            snake.grow()
            puntaje += 10
            apple.position = [
                random.randrange(arena_left, arena_right - apple.size + 1, apple.size),
                random.randrange(arena_top, arena_bottom - apple.size + 1, apple.size)
            ]
        score_text = pygame.font.Font(None, 40).render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  

        pygame.display.flip()
        clock.tick(10)
# Menú principal
def main_menu():
    start_button = Button(width // 2 - 120, height // 2 + 200, 220, 70, "JUGAR", start_game)
    settings_button = Button(width // 2 - 180, height // 2 + 300, 325, 70, "OPCIONES", show_settings)

    running = True
    while running:
        
        screen.blit(background_image, (0, 0)) 


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if start_button.is_clicked(event):
                start_game()
            if settings_button.is_clicked(event):
                show_settings()

        start_button.draw()
        settings_button.draw()
        pygame.display.flip()

# Ejecutar el menú principal
main_menu()
pygame.quit()

