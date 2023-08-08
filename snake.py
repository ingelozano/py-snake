import pygame
import sys
import random

pygame.init()

# Configuración de la ventana
ventana_ancho = 800
ventana_altura = 600
ventana = pygame.display.set_mode((ventana_ancho, ventana_altura))
pygame.display.set_caption('Juego de Snake')

# Colores
COLOR_FONDO = (0, 0, 0)
COLOR_SNAKE = (0, 255, 0)
COLOR_COMIDA = (255, 0, 0)

# Tamaño de los bloques
bloque_tamano = 20

# Velocidad de la serpiente
velocidad = 15

class Snake:
    def __init__(self):
        x, y = ventana_ancho // 2, ventana_altura // 2
        self.cuerpo = [(x, y), (x - bloque_tamano, y), (x - bloque_tamano * 2, y)]
        self.direccion = (1, 0)
        self.crecimiento_pendiente = 0

    def mover(self):
        dx, dy = self.direccion
        x, y = self.cuerpo[0]
        nueva_cabeza = ((x + dx * bloque_tamano) % ventana_ancho, (y + dy * bloque_tamano) % ventana_altura)
        self.cuerpo.insert(0, nueva_cabeza)

        if self.crecimiento_pendiente > 0:
            self.crecimiento_pendiente -= 1
        else:
            self.cuerpo.pop()

    def cambiar_direccion(self, dx, dy):
        if (dx, dy) != (-self.direccion[0], -self.direccion[1]):
            self.direccion = (dx, dy)

    def colision_cuerpo(self):
        return self.cuerpo[0] in self.cuerpo[1:]

    def colision_bordes(self):
        x, y = self.cuerpo[0]
        return x < 0 or x >= ventana_ancho or y < 0 or y >= ventana_altura

    def crecer(self):
        self.crecimiento_pendiente += 1

class Comida:
    def __init__(self):
        self.posicion = (random.randint(0, ventana_ancho // bloque_tamano - 1) * bloque_tamano,
                         random.randint(0, ventana_altura // bloque_tamano - 1) * bloque_tamano)

    def generar(self):
        self.posicion = (random.randint(0, ventana_ancho // bloque_tamano - 1) * bloque_tamano,
                         random.randint(0, ventana_altura // bloque_tamano - 1) * bloque_tamano)

def mostrar_mensaje(mensaje):
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(mensaje, True, (255, 255, 255))
    ventana.blit(texto, ((ventana_ancho - texto.get_width()) // 2, (ventana_altura - texto.get_height()) // 2))
    pygame.display.update()

def main():
    reloj = pygame.time.Clock()

    juego_activo = True  # Variable para controlar el estado del juego

    while juego_activo:
        serpiente = Snake()
        comida = Comida()

        while juego_activo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Control de la serpiente con las teclas de flecha
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        serpiente.cambiar_direccion(0, -1)
                    elif event.key == pygame.K_DOWN:
                        serpiente.cambiar_direccion(0, 1)
                    elif event.key == pygame.K_LEFT:
                        serpiente.cambiar_direccion(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        serpiente.cambiar_direccion(1, 0)

            serpiente.mover()

            # Verificar colisión con la comida
            cabeza = serpiente.cuerpo[0]
            if cabeza == comida.posicion:
                comida.generar()
                serpiente.crecer()

            ventana.fill(COLOR_FONDO)

            # Dibujar serpiente
            for bloque in serpiente.cuerpo:
                pygame.draw.rect(ventana, COLOR_SNAKE, (bloque[0], bloque[1], bloque_tamano, bloque_tamano))

            # Dibujar comida
            pygame.draw.rect(ventana, COLOR_COMIDA, (comida.posicion[0], comida.posicion[1], bloque_tamano, bloque_tamano))

            pygame.display.update()
            reloj.tick(velocidad)

            if serpiente.colision_cuerpo() or serpiente.colision_bordes():
                ventana.fill(COLOR_FONDO)
                mostrar_mensaje("Game Over - Presiona R para Reiniciar o Q para Salir")
                pygame.display.update()
                esperar_tecla = True
                while esperar_tecla:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                esperar_tecla = False
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

if __name__ == "__main__":
    main()
