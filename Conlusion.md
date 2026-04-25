# Conlusion dinamica

Ultima actualizacion: 2026-04-25 09:31:26 -03:00
Tema activo: Collatz - Decima Ola cerrada

## Preguntas antes de la iteracion

```text
Estoy en algo virgen?
No en el marco general. Bloques, salida y modelo geometrico ya existen.

Puedo descubrir algo con esto?
Quizas una desviacion fina del modelo, no una prueba.

Ya alguien estuvo buscando esto?
Si a nivel general: Campbell, Bonacorsi/Bordoni, Chang y literatura de modelos estocasticos.

Que tan lejos estoy de descubrir algo?
Muy lejos de probar Collatz; moderadamente cerca de una nota experimental si el sesgo se formaliza.
```

## Hallazgo principal

La decima ola midio `exit_v2 >= k` y `exit_v2 = k` hasta `n <= 5000000`.

Resultado candidato:

| Condicion previa | P exp real | P exp modelo | Diff | IC95 |
| --- | ---: | ---: | ---: | --- |
| `exit_v2 >= 5` | 0.25968013 | 0.28201954 | -0.02233940 | [-0.03685220, -0.00782660] |
| `exit_v2 = 5` | 0.25979573 | 0.28127273 | -0.02147700 | [-0.03816197, -0.00479203] |

La senal persiste al escalar desde un millon a cinco millones, pero no es monotona para todos los valores altos de `exit_v2`.

## Preguntas despues de la iteracion

```text
La originalidad cambio?
No mucho. Sigue siendo una extension fina de un marco existente.

La probabilidad de relevancia subio?
Subio un poco: `exit_v2 = 5` sobrevivio al escalado.

Senal robusta o ruido?
Senal moderada para `exit_v2 = 5`; muestra insuficiente para valores mas altos.

Que aprendimos?
La variable correcta no es "bloque expansivo previo"; parece mas modular y ligada a ciertos exit_v2.

Seguir o abandonar?
Seguir una iteracion mas, pero derivando congruencias. No fuerza bruta ciega.
```

## Siguiente paso

Derivar la congruencia exacta para:

```text
exit_v2 = 5
```

y medir si esa clase fuerza una menor cola siguiente o menor expansion. Si no aparece una explicacion modular, abandonar esta pista.
