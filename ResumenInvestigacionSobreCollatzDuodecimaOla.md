# Resumen fuerte - Duodecima Ola

La duodecima ola estudio el sesgo de supervivencia orbital. La pregunta era si la senal previa de `next_tail = 1` despues de `prev_exit_v2 = 5` se explicaba solo porque estabamos mirando cadenas antes del primer descenso.

El resultado principal es doble. Primero, el modelo geometrico independiente explica casi perfectamente el sesgo global por posicion: los bloques finales tienen `tail=1` real `0.68311110` vs modelo `0.68213098`; los bloques interiores tienen `0.38646876` vs `0.38606060`. Esto indica que la gran forma de la supervivencia no es una anomalia aritmetica.

Segundo, queda un residuo localizado. Para `prev_exit_v2 = 5` seguido de bloque interior, el real tiene `tail=1` en `0.45271454` contra `0.40614137` del modelo, diferencia `0.04657317` con IC95 `[0.02320157, 0.06994477]`. La expansion siguiente cae de `0.44814600` en el modelo a `0.40834793` real.

Conclusion: `exit_v2 = 5` no es una ley local estatica, pero combinado con supervivencia orbital e interioridad deja una dependencia fina no capturada por el modelo independiente. La siguiente ola debe descomponer esa fila por residuos, margen y profundidad.
