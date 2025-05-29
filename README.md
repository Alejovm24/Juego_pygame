# Juego_pygame_The Survival of the Snake
# The Survival of the Snake

**The Survival of the Snake** es una reinvención del clásico juego *Snake*, desarrollada en Python con Pygame. Este juego agrega acción, estrategia y supervivencia al mezclar el tradicional objetivo de comer para crecer con enemigos dinámicos que intentan atraparte. ¡Solo los jugadores más atentos y rápidos lograrán sobrevivir!

---

## 🎮 ¿De qué trata el juego?

Eres una serpiente en un entorno hostil. Para sobrevivir debes:

- Comer manzanas para crecer.
- Evitar chocar con los enemigos que se mueven por la pista.
- Mantenerte dentro del área de juego, delimitada por muros.
- Escoger sabiamente el nivel de dificultad para desafiar tus reflejos.

El juego termina si colisionas con un enemigo o sales del área de juego. ¡Tu objetivo es obtener el puntaje más alto posible antes de caer!

---

## 🧠 Mecánica del juego

- Te mueves usando las flechas del teclado.
- Al comer una manzana, ganas 10 puntos y la serpiente se hace más larga.
- Cada enemigo tiene un patrón de movimiento diferente:
  - 🐢 **Tortuga:** baja lentamente desde la parte superior.
  - 🦀 **Cangrejo:** se mueve aleatoriamente hacia la izquierda y derecha.
  - 🐊 **Cocodrilo:** se mueve con velocidad variable en línea recta horizontal.

---

## 🔥 Dificultades

En el menú de **Opciones**, puedes elegir entre tres niveles de dificultad:

| Dificultad | Enemigos activos       |
|------------|-------------------------|
| Fácil      | Solo la tortuga         |
| Medio      | Tortuga y cangrejo      |
| Difícil    | Tortuga, cangrejo y cocodrilo |

También puedes ajustar el **brillo** para cambiar el estilo visual del juego.

---

## 📦 Requisitos

- Python 3.8 o superior
- [Pygame](https://www.pygame.org/) — instala con:

```bash
pip install pygame

