# Auditoria de originalidad: bloques Mersenne, salida y modelo geometrico

Fecha de auditoria: 2026-04-25 02:51:27 -03:00
Estado: auditoria inicial con busqueda web

## Pregunta

Verificar si alguien habia visto antes las ideas investigadas en las olas quinta a novena:

- prefijo/bloque inducido por `v2(n + 1)`;
- descomposicion `n = 2^s q - 1`;
- salida `3^s q - 1`;
- exponente de salida `r = v2(3^s q - 1)`;
- mapa entre inicios de bloques;
- modelo geometrico independiente para `(s, r)`;
- mediciones de dependencia o anti-persistencia entre bloques.

## Veredicto corto

Si: el nucleo estructural ya habia sido visto, y muy recientemente.

La coincidencia mas directa encontrada es el preprint:

- Stephen R. Campbell, *Mersenne Block Dynamics: A Framework for the Collatz Conjecture*, fechado el 18 de diciembre de 2025, subido a ResearchGate el 6 de febrero de 2026, DOI informado por ResearchGate: `10.5281/ZENODO.17971540`.

Ese trabajo usa casi la misma arquitectura conceptual:

- `n(x) = v2(x + 1)` como longitud de cola Mersenne;
- decomposicion de impares por cola binaria;
- bloques Mersenne dentro del mapa Syracuse;
- formula cerrada dentro del bloque;
- exponente de salida `r(x) = v2(3^n a - 1)`;
- mapa de bloque `B(x)`;
- estadistica geometrica para `n` y `r`;
- hipotesis de mezcla/orbit-mixing para sucesivos bloques.

Por lo tanto, no conviene presentar como original el marco general "bloques Mersenne + salida + modelo geometrico".

## Que ya era clasico antes de 2025

### Mapas acelerados y odd-to-odd

Kontorovich y Lagarias describen el mapa acelerado sobre impares:

```text
U(n) = (3n + 1) / 2^ord2(3n + 1)
```

La idea de mirar solo impares y remover todas las potencias de dos es anterior; ellos indican que Crandall estudio `U` en 1978.

Fuente:

- Alex V. Kontorovich y Jeffrey C. Lagarias, *Stochastic Models for the 3x+1 and 5x+1 Problems*, arXiv:0910.1944, 2009.

### Modelos estocasticos y random walks

El uso de modelos probabilisticos para Collatz tambien es clasico. Lagarias y otros explican que un modelo basico trata los pasos como una caminata aleatoria con drift negativo. Kontorovich y Lagarias desarrollan modelos de producto multiplicativo, biased random walk y repeated random walk.

Fuentes:

- Jeffrey C. Lagarias, *The 3x+1 Problem: An Overview*, arXiv:2111.02635, version arXiv 2021 de material publicado en 2010.
- Alex V. Kontorovich y Jeffrey C. Lagarias, *Stochastic Models for the 3x+1 and 5x+1 Problems*, arXiv:0910.1944, 2009.

### Casi todos bajan

El resultado de que "casi todo" numero baja eventualmente por debajo de su inicio aparece en la literatura temprana.

Fuentes:

- Riho Terras, *A stopping time problem on the positive integers*, Acta Arithmetica 30, 1976, 241-252.
- C. J. Everett, *Iteration of the number-theoretic function f(2n)=n, f(2n+1)=3n+2*, Advances in Mathematics 25, 1977, 42-45.

## Coincidencia directa con Campbell 2025

Campbell define:

```text
n(x) := v2(x + 1)
x + 1 = 2^n a
```

y llama a `n(x)` la longitud de la cola Mersenne. Luego define bloques:

```text
x, S(x), ..., S^(n(x)-1)(x)
```

y el mapa de bloque:

```text
B(x) = S^(n(x))(x)
```

Tambien da la salida:

```text
r(x) = v2(3^n a - 1)
B(x) = (3^n a - 1) / 2^r
```

Esto coincide con nuestras olas quinta a séptima, con diferencias de notacion:

| Nuestro repo | Campbell |
| --- | --- |
| `s = v2(n + 1)` | `n(x) = v2(x + 1)` |
| `q = (n + 1)/2^s` | `a(x)` |
| `3^s q - 1` | `3^n a - 1` |
| `exit_v2` | `r(x)` |
| `next_odd` | `B(x)` |
| bloque alternante / odd-to-odd | Mersenne block / Syracuse block |

Campbell tambien informa la ley de densidad:

```text
Pr(n(x) = n, r(x) = r) = 2^-(n+r)
```

y modela sucesivos parametros como i.i.d. geometricos bajo una hipotesis de mezcla.

## Que podria quedar como aporte propio

Todavia no encontre, en esta busqueda inicial, una coincidencia exacta para nuestras mediciones de:

- comparacion real/modelo con `499999` cadenas hasta `n <= 1000000`;
- tablas de cola tipo `bloques >= 40`, `max pico/n >= 100000`;
- test explicito de anti-persistencia entre factores consecutivos;
- resultado negativo: `corr(log_i, log_{i+1})` casi cero;
- condicionamiento por `exit_v2 >= 5` mostrando posible menor expansion siguiente.

Pero esto debe tratarse como "no encontrado aun", no como "original". Campbell ya propone estudiar mezcla/residue-class dynamics y dependencia debil entre bloques, asi que nuestras mediciones encajan como experimento de seguimiento dentro de esa agenda.

## Fecha de prioridad aproximada

- Terras: 1976, stopping time y densidad.
- Everett: 1977, casi todos tienen un iterado menor que el inicio.
- Crandall: 1978, mapa acelerado sobre impares segun cita Kontorovich-Lagarias.
- Lagarias-Weiss: 1992, modelos estocasticos del problema.
- Kontorovich-Lagarias: 2009/2010, modelos estocasticos modernos y escalas random walk.
- Campbell: 18 de diciembre de 2025, marco "Mersenne Block Dynamics" casi identico al nucleo estructural de nuestras olas.
- Nuestro repo: 25 de abril de 2026, reproduccion independiente, experimentos comparativos y anti-persistencia.

## Decision practica

No conviene decir:

```text
descubrimos una nueva teoria de bloques Mersenne
```

Si conviene decir:

```text
reconstruimos independientemente un marco muy cercano al de Campbell 2025, lo implementamos en un laboratorio reproducible, y agregamos pruebas experimentales sobre mezcla, modelo geometrico y anti-persistencia.
```

El proximo trabajo util deberia citar explicitamente a Campbell y reposicionar el proyecto como:

- reproduccion independiente;
- verificacion computacional;
- extension experimental sobre dependencia entre bloques;
- busqueda de un posible sesgo asociado a `exit_v2` alto.
