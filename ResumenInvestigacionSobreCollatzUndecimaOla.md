# Resumen fuerte - Undecima Ola

La undecima ola reviso la senal mas prometedora de la decima ola: despues de bloques con `exit_v2 = 5`, las cadenas odd-to-odd antes del primer descenso parecian tener menos expansion siguiente que el modelo geometrico independiente.

El resultado cambia la interpretacion. Para todos los bloques locales con inicio impar `n <= 5000000`, condicionar por `exit_v2 = 5` no produce sesgo: la probabilidad de expansion siguiente es `0.28628846`, practicamente igual al modelo geometrico `0.28627450`. La cola siguiente tambien vuelve a media `2`: `avg_next_tail = 2.00011520`.

La senal aparece solo en la muestra `chain_before_descent`, es decir, en pares de bloques dentro de cadenas que todavia no descendieron por debajo del valor inicial. Alli la expansion siguiente baja a `0.25979573` y `next_tail = 1` sube a `0.54447539` frente al `0.5` geometrico.

Conclusion: `exit_v2 = 5` no parece ser un mecanismo local nuevo. La senal de la decima ola es un efecto de seleccion orbital. Esto descarta una linea demasiado optimista y abre otra mas precisa: estudiar como el condicionamiento por supervivencia antes del primer descenso deforma la distribucion de colas y reduce extremos reales frente al modelo independiente.
