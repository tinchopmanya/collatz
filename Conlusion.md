# Conlusion dinamica

Ultima actualizacion: 2026-04-25 09:45:21 -03:00
Tema activo: Collatz - Undecima Ola cerrada

## Preguntas antes de la iteracion

```text
Estoy en algo virgen?
No en el marco general. Bloques de Mersenne, salida r(x), mezcla y clases modulo potencias de 2 ya estan en el ecosistema reciente.

Puedo descubrir algo con esto?
Si, pero probablemente como descarte: saber si `exit_v2 = 5` era una causa local o un efecto de seleccion.

Ya alguien estuvo buscando esto?
Si a nivel de marco. Campbell 2025 ya propone estudiar dinamica residual y mezcla del mapa de bloques.

Que tan lejos estoy de descubrir algo?
Muy lejos de probar Collatz. Cerca de limpiar una pista concreta y evitar sobreinterpretarla.
```

## Hallazgo principal

La undecima ola comparo dos muestras para `prev_exit_v2 = 5` hasta `n <= 5000000`:

| Fuente | Pares | P siguiente expansion | Diff vs geometrico | Avg next_tail |
| --- | ---: | ---: | ---: | ---: |
| `local_all_starts` | 78124 | 0.28628846 | 0.00001396 | 2.00011520 |
| `chain_before_descent` | 5385 | 0.25979573 | -0.02647877 | 1.92423398 |

La senal de la decima ola no es una ley local de `exit_v2 = 5`. En todos los bloques locales, la clase vuelve al modelo geometrico. La diferencia aparece solo en cadenas condicionadas por seguir vivas antes del primer descenso.

## Congruencia

Para:

```text
n = 2^s q - 1
```

se tiene:

```text
exit_v2 = 5
<=> v2(3^s q - 1) = 5
<=> 3^s q = 33 mod 64
<=> q = 3^(-s) + 32 mod 64
```

Esto fija una clase residual, pero no fuerza por si sola menor expansion siguiente.

## Preguntas despues de la iteracion

```text
La originalidad cambio?
Si, a la baja para esta pista. `exit_v2 = 5` no parece ser un mecanismo local nuevo.

La probabilidad de relevancia subio?
Bajo para una nota sobre `exit_v2 = 5`; subio para estudiar sesgo de supervivencia orbital.

Senal robusta o seleccion?
Seleccion. La senal es real en cadenas antes del primer descenso, pero desaparece en la muestra local.

Que aprendimos?
El modelo local estatico funciona muy bien. La brecha esta en como las orbitas largas seleccionan transiciones.

Seguir o abandonar?
Abandonar `exit_v2 = 5` como lemma local candidato. Seguir con M13: sesgo de supervivencia orbital.
```

## Siguiente paso

Abrir M13:

```text
medir como cambia next_tail segun profundidad, duracion y supervivencia antes del primer descenso.
```

La pregunta nueva no es "que clase local es especial?", sino:

```text
que filtro orbital hace que las cadenas largas no vean las transiciones locales como una muestra uniforme?
```
