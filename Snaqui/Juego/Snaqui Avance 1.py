import random

# Variables 
serpiente = [[4, 4]]
comida = [random.randint(0, 9), random.randint(0, 9)]
direccion = "derecha"
puntuacion = 0
# Bucle 
while True:
    # Tablero 
    for y in range(10):
        fila = []
        for x in range(10):
            if [x, y] in serpiente:
                fila.append("O")
            elif x == comida[0] and y == comida[1]:
                fila.append("*")
            else:
                fila.append(".")
        print(" ".join(fila))
    
    # Introducir por teclado
    tecla = input("Dirección (W/A/S/D): ").lower()
    
    # Guardar direccion
    if tecla == "d" and direccion != "izquierda":
        direccion = "derecha"
    elif tecla == "a" and direccion != "derecha":
        direccion = "izquierda"
    elif tecla == "w" and direccion != "abajo":
        direccion = "arriba"
    elif tecla == "s" and direccion != "arriba":
        direccion = "abajo"
    
    # comprobar direccion y movimiento
    cabeza = serpiente[0].copy()
    if direccion == "derecha":
        cabeza[0] += 1
    elif direccion == "izquierda":
        cabeza[0] -= 1
    elif direccion == "arriba":
        cabeza[1] -= 1
    elif direccion == "abajo":
        cabeza[1] += 1
    
    # Verificar colisiones
    if (cabeza in serpiente or 
        cabeza[0] < 0 or cabeza[0] >= 10 or 
        cabeza[1] < 0 or cabeza[1] >= 10):
        print(f"¡Game Over! Puntuación: {puntuacion}")
        break
    
    serpiente.insert(0, cabeza)
    
    # Comer comida 
    if cabeza == comida:
        puntuacion += 1
        comida = [random.randint(0, 9), random.randint(0, 9)]
    else:
        serpiente.pop()
