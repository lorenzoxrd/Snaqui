
import pygame
import random
import sys
from enum import Enum

# Inicializar Pygame
pygame.init()

# Configuración inicial
ANCHO = 600
ALTO = 600
TAMANO_CELDA = 30
FILAS = ALTO // TAMANO_CELDA
COLUMNAS = ANCHO // TAMANO_CELDA

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (200, 200, 200)

# Estados del juego
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

# Configurar ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SNAQUI")

reloj = pygame.time.Clock()

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_actual = color_normal
        self.fuente = pygame.font.SysFont('Arial', 30)
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color_actual, self.rect)
        texto_surf = self.fuente.render(self.texto, True, BLANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)
        
    def esta_sobre(self, pos):
        return self.rect.collidepoint(pos)

def dibujar_texto(texto, tamaño, color, x, y):
    fuente = pygame.font.SysFont('Arial', tamaño)
    texto_surf = fuente.render(texto, True, color)
    texto_rect = texto_surf.get_rect(center=(x, y))
    ventana.blit(texto_surf, texto_rect)

def mostrar_menu(estado_juego):
    ventana.fill(AZUL)
    dibujar_texto("SNAQUI", 50, BLANCO, ANCHO//2, ALTO//4)
    
    boton_jugar = Boton(ANCHO//2 - 100, ALTO//2 - 50, 200, 50, "JUGAR", VERDE, (0, 200, 0))
    boton_salir = Boton(ANCHO//2 - 100, ALTO//2 + 50, 200, 50, "SALIR", ROJO, (200, 0, 0))
    
    boton_jugar.dibujar(ventana)
    boton_salir.dibujar(ventana)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if boton_jugar.esta_sobre(event.pos):
                estado_juego = GameState.PLAYING
            elif boton_salir.esta_sobre(event.pos):
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEMOTION:
            boton_jugar.color_actual = boton_jugar.color_hover if boton_jugar.esta_sobre(event.pos) else boton_jugar.color_normal
            boton_salir.color_actual = boton_salir.color_hover if boton_salir.esta_sobre(event.pos) else boton_salir.color_normal
    
    pygame.display.update()
    return estado_juego

def mostrar_game_over(puntuacion):
    ventana.fill(NEGRO)
    dibujar_texto("GAME OVER", 50, ROJO, ANCHO//2, ALTO//4)
    dibujar_texto(f"Puntuación: {puntuacion}", 30, BLANCO, ANCHO//2, ALTO//3)
    
    boton_reiniciar = Boton(ANCHO//2 - 100, ALTO//2 - 50, 200, 50, "Reiniciar", VERDE, (0, 200, 0))
    boton_menu = Boton(ANCHO//2 - 100, ALTO//2 + 50, 200, 50, "Menú Principal", AZUL, (0, 0, 200))
    boton_salir = Boton(ANCHO//2 - 100, ALTO//2 + 150, 200, 50, "Salir", ROJO, (200, 0, 0))
    
    boton_reiniciar.dibujar(ventana)
    boton_menu.dibujar(ventana)
    boton_salir.dibujar(ventana)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if boton_reiniciar.esta_sobre(event.pos):
                return GameState.PLAYING
            elif boton_menu.esta_sobre(event.pos):
                return GameState.MENU
            elif boton_salir.esta_sobre(event.pos):
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEMOTION:
            boton_reiniciar.color_actual = boton_reiniciar.color_hover if boton_reiniciar.esta_sobre(event.pos) else boton_reiniciar.color_normal
            boton_menu.color_actual = boton_menu.color_hover if boton_menu.esta_sobre(event.pos) else boton_menu.color_normal
            boton_salir.color_actual = boton_salir.color_hover if boton_salir.esta_sobre(event.pos) else boton_salir.color_normal
    
    pygame.display.update()
    return GameState.GAME_OVER

def juego():
    snake = [[4, 4]]
    comida = [random.randint(0, COLUMNAS-1), random.randint(0, FILAS-1)]
    direccion = "derecha"
    puntuacion = 0
    velocidad = 8
    estado_juego = GameState.PLAYING
    
    while estado_juego == GameState.PLAYING:
        ventana.fill(NEGRO)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direccion != "izquierda":
                    direccion = "derecha"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direccion != "derecha":
                    direccion = "izquierda"
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direccion != "abajo":
                    direccion = "arriba"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direccion != "arriba":
                    direccion = "abajo"
        
        # Mover serpiente
        cabeza = snake[0].copy()
        if direccion == "derecha":
            cabeza[0] += 1
        elif direccion == "izquierda":
            cabeza[0] -= 1
        elif direccion == "arriba":
            cabeza[1] -= 1
        elif direccion == "abajo":
            cabeza[1] += 1
        
        # Verificar colisiones
        if (cabeza in snake or
            cabeza[0] < 0 or cabeza[0] >= COLUMNAS or
            cabeza[1] < 0 or cabeza[1] >= FILAS):
            estado_juego = GameState.GAME_OVER
            break
        
        snake.insert(0, cabeza)
        
        # Comer comida
        if cabeza == comida:
            puntuacion += 1
            velocidad += 0.5
            while True:
                comida = [random.randint(0, COLUMNAS-1), random.randint(0, FILAS-1)]
                if comida not in snake:
                    break
        else:
            snake.pop()
        
        # Dibujar elementos
        for segmento in snake:
            pygame.draw.rect(ventana, VERDE, (segmento[0]*TAMANO_CELDA, segmento[1]*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
        pygame.draw.rect(ventana, ROJO, (comida[0]*TAMANO_CELDA, comida[1]*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
        dibujar_texto(f"Puntuación: {puntuacion}", 20, BLANCO, ANCHO//2, 20)
        
        pygame.display.update()
        reloj.tick(velocidad)
    
    return puntuacion

def main():
    estado_juego = GameState.MENU
    puntuacion_final = 0
    
    while True:
        if estado_juego == GameState.MENU:
            estado_juego = mostrar_menu(estado_juego)
        elif estado_juego == GameState.PLAYING:
            puntuacion_final = juego()
            estado_juego = GameState.GAME_OVER
        elif estado_juego == GameState.GAME_OVER:
            estado_juego = mostrar_game_over(puntuacion_final)

if __name__ == "__main__":
    main()