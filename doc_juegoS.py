import pygame
import sys
import random

# Inicializamos Pygame
pygame.init()

# Definimos colores
WHITE = (153, 153, 204)  # Color de fondo
BLACK = (0, 0, 0)        # Color de texto negro
BLUE = (0, 0, 255)       # Color del enemigo
RED = (255, 0, 0)        # Color del jugador

# Tamaño de la pantalla
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Configuración de la ventana
pygame.display.set_caption("Juego - Pantalla de Bienvenida")  # Título de la ventana

# Fuente para el texto
font = pygame.font.SysFont(None, 55)  # Fuente predeterminada para el texto del juego

# Función para mostrar el texto en pantalla
def show_message(text, font, color, x, y):
    """
    Renderiza el texto en la pantalla.

    :param text: Texto a mostrar.
    :param font: Fuente del texto.
    :param color: Color del texto.
    :param x: Posición X del texto.
    :param y: Posición Y del texto.
    """
    message = font.render(text, True, color)
    screen.blit(message, (x, y))

# Función principal para la pantalla de bienvenida
def welcome_screen():
    """
    Muestra una pantalla de bienvenida con un botón para comenzar el juego.
    La pantalla espera a que el usuario haga clic en el botón "Comenzar".
    """
    welcome = True
    while welcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Salida del programa si se cierra la ventana

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si se hace clic en el botón, comienza el juego
                x, y = event.pos
                if 220 <= x <= 420 and 350 <= y <= 400:  # Coordenadas del botón "Comenzar"
                    welcome = False

        # Fondo blanco
        screen.fill(WHITE)

        # Mostrar el mensaje de bienvenida
        show_message("BIENVENIDOS AL JUEGO ", font, BLACK, 120, 150)
        
        # Dibujar el botón "Comenzar"
        pygame.draw.rect(screen, BLUE, [220, 350, 245, 50])
        show_message("Comenzar", font, WHITE, 250, 360)

        # Actualizar la pantalla
        pygame.display.update()

# Función principal del juego
def main_game():
    """
    Lógica principal del juego donde el jugador controla un cuadrado rojo y esquiva un cuadrado azul.
    El juego termina si el jugador colisiona con el enemigo.
    """
    # Configuraciones iniciales del jugador
    jugador_size = 50
    jugador_pos = [WIDTH // 2, HEIGHT - 2 * jugador_size]  # Posición inicial del jugador
    velocidad = 10  # Velocidad de movimiento del jugador

    # Configuración del enemigo
    enemigo_size = 50
    enemigo_pos = [random.randint(0, WIDTH - enemigo_size), 0]  # Posición inicial del enemigo
    enemigo_velocidad = 5  # Velocidad de movimiento del enemigo

    # Reloj para controlar los FPS
    clock = pygame.time.Clock()
    
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controles del jugador (movimiento con teclas de dirección)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador_pos[0] -= velocidad
        if keys[pygame.K_RIGHT]:
            jugador_pos[0] += velocidad

        # Limitar al jugador a la pantalla
        if jugador_pos[0] < 0:
            jugador_pos[0] = 0
        if jugador_pos[0] > WIDTH - jugador_size:
            jugador_pos[0] = WIDTH - jugador_size

        # Movimiento del enemigo
        enemigo_pos[1] += enemigo_velocidad
        if enemigo_pos[1] >= HEIGHT:  # Si el enemigo llega al fondo, reaparece arriba
            enemigo_pos[1] = 0
            enemigo_pos[0] = random.randint(0, WIDTH - enemigo_size)

        # Detectar colisión entre el jugador y el enemigo
        if detectar_colision(jugador_pos, enemigo_pos, jugador_size, enemigo_size):
            game_over_screen()  # Mostrar la pantalla de "Game Over"
            game_over = True

        # Llenar la pantalla de blanco
        screen.fill(WHITE)

        # Dibujar al jugador
        pygame.draw.rect(screen, RED, (jugador_pos[0], jugador_pos[1], jugador_size, jugador_size))

        # Dibujar al enemigo
        pygame.draw.rect(screen, BLUE, (enemigo_pos[0], enemigo_pos[1], enemigo_size, enemigo_size))

        # Actualizar pantalla
        pygame.display.update()

        # Limitar a 30 FPS
        clock.tick(30)

# Función para detectar colisiones
def detectar_colision(jugador_pos, enemigo_pos, jugador_size, enemigo_size):
    """
    Comprueba si el jugador ha colisionado con el enemigo.

    :param jugador_pos: Posición [x, y] del jugador.
    :param enemigo_pos: Posición [x, y] del enemigo.
    :param jugador_size: Tamaño del jugador (ancho y alto).
    :param enemigo_size: Tamaño del enemigo (ancho y alto).
    :return: True si hay colisión, False en caso contrario.
    """
    jx, jy = jugador_pos
    ex, ey = enemigo_pos
    if (ex >= jx and ex < (jx + jugador_size)) or (jx >= ex and jx < (ex + enemigo_size)):
        if (ey >= jy and ey < (jy + jugador_size)) or (jy >= ey and jy < (ey + enemigo_size)):
            return True
    return False

# Modificación para la pantalla de "Game Over"
def game_over_screen():
    """
    Muestra la pantalla de 'Game Over' y ofrece la opción de reiniciar o salir.
    """
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 220 <= x <= 420 and 350 <= y <= 400:  # Botón de reiniciar
                    main_game()  # Reinicia el juego
                    game_over = False
                if 220 <= x <= 420 and 450 <= y <= 500:  # Botón de salir
                    pygame.quit()
                    sys.exit()

        # Fondo blanco
        screen.fill(WHITE)

        # Mostrar el mensaje de 'Game Over'
        show_message("Game Over", font, BLACK, 220, 150)

        # Dibujar el botón "Reiniciar"
        pygame.draw.rect(screen, BLUE, [220, 350, 245, 50])
        show_message("Reiniciar", font, WHITE, 250, 360)

        # Dibujar el botón "Salir"
        pygame.draw.rect(screen, RED, [220, 450, 245, 50])
        show_message("Salir", font, WHITE, 250, 460)

        # Actualizar pantalla
        pygame.display.update()

# Llamada a la pantalla de bienvenida
welcome_screen()

# Inicia el juego principal
main_game()

# Salir de Pygame
pygame.quit()

