# Estado de actualidad y originalidad Collatz

Fecha: 2026-04-25
Motivo: verificar si la senal `-1 mod 2^k` ya era conocida y si estamos trabajando con literatura reciente.

## Veredicto

La senal `-1 mod 2^k` no debe tratarse como descubrimiento original. Es una redeteccion computacional de una estructura conocida o, al menos, muy cercana a resultados y tablas existentes sobre dropping time, stopping time, clases residuales modulo potencias de 2 y numeros con cola binaria de unos.

El trabajo sigue valiendo, pero cambia de categoria:

- no es "descubrimos una familia nueva";
- si es "construimos un laboratorio reproducible que redetecta, cuantifica y puede extender una familia estructural conocida".

## Evidencia de que ya habia antecedentes

### 1. OEIS y Klee-Wagon

OEIS A324248 lista numeros impares con dropping time de la iteracion reducida de Collatz mayor que 5. La secuencia empieza:

`27, 31, 47, 63, 71, 91, 103, 111, 127, 155, 159, 167, 191, 207, 223, 231, 239, 251, 255, ...`

Esto ya incluye `127`, `255` y luego `511`, que aparecen alineados con nuestra senal de clases `-1 mod 2^k`.

La entrada remite a Victor Klee y Stan Wagon, *Old and New Unsolved Problems in Plane Geometry and Number Theory*, MAA, 1991, pp. 191-194, 225-229, 308-309.

Fuente: https://oeis.org/A324248

### 2. Terras y estructura de stopping time

Riho Terras estudio stopping times y clases residuales en "A stopping time problem on the positive integers". Esta linea es base clasica para entender por que los tiempos de bajada se organizan por congruencias modulo potencias de 2.

Fuente: https://eudml.org/doc/205476

### 3. Winkler y clases de stopping time

Mike Winkler estudia conjuntos de clases residuales modulo `2^sigma_n` asociadas a stopping time finito. No es exactamente nuestro analisis de promedios por clase, pero esta en la misma familia conceptual.

Fuente: https://arxiv.org/abs/1504.00212

### 4. Bonacorsi y Bordoni, marzo 2026

El preprint "Bayesian Modeling of Collatz Stopping Times" estudia `tau(n)` hasta `n <= 10^7` y reporta heterogeneidad aritmetica fuerte. Su modelo usa `log n` y `n mod 8` como covariables, y encuentra que la estructura modular de bajo orden ayuda a explicar la distribucion.

Fuente: https://arxiv.org/abs/2603.04479

### 5. Chang, marzo/abril 2026

Edward Y. Chang publico dos preprints relevantes:

- "Exploring Collatz Dynamics with Human-LLM Collaboration", enviado el 10 de marzo de 2026 y revisado el 22 de abril de 2026.
- "A Structural Reduction of the Collatz Conjecture to One-Bit Orbit Mixing", enviado el 24 de marzo de 2026.

Estos trabajos enfatizan mezcla orbital, clases modulo potencias de 2 y residuos modulo 32. Son recientes y deben tratarse como preprints, no como resultados establecidos por revision por pares.

Fuentes:

- https://arxiv.org/abs/2603.11066
- https://arxiv.org/abs/2603.25753

### 6. Literatura muy reciente a fines de abril de 2026

Consulta arXiv API ordenada por fecha de envio al 25 de abril de 2026:

- 2026-04-22: "Selection Rules and Channel Structure in a Base Octave Model of Collatz Dynamics", Katharina Lodders.
- 2026-04-22: revision v6 de "Exploring Collatz Dynamics with Human-LLM Collaboration", Edward Y. Chang.
- 2026-04-13: revision v4 de "Paradoxical behavior in Collatz sequences", Olivier Rozier y Claude Terracol, con referencia a Discrete Mathematics 2026.
- 2026-03-24: "A Structural Reduction of the Collatz Conjecture to One-Bit Orbit Mixing", Edward Y. Chang.
- 2026-03-04: "Bayesian Modeling of Collatz Stopping Times", Bonacorsi y Bordoni.
- 2026-02-11: "An improved algorithm for checking the Collatz conjecture for all n < 2^N", Vigleik Angeltveit.

Fuentes:

- https://arxiv.org/abs/2604.20181
- https://arxiv.org/abs/2603.11066
- https://arxiv.org/abs/2502.00948
- https://arxiv.org/abs/2603.25753
- https://arxiv.org/abs/2603.04479
- https://arxiv.org/abs/2602.10466

## Como cambia nuestro plan

El patron `127 -> 255 -> 511` debe pasar de "posible descubrimiento" a "benchmark estructural conocido".

La linea util ahora es:

1. Reproducirlo limpiamente.
2. Compararlo contra clases control.
3. Medir prefijos de paridad y primeras excursiones.
4. Conectar la observacion con Mersenne tails o trailing ones.
5. Ver si nuestro analisis de promedios por clase y records aporta una forma clara de visualizar o cuantificar el fenomeno.

## Que no vamos a afirmar

- No vamos a afirmar que descubrimos una familia nueva.
- No vamos a afirmar que esto apunta directamente a una prueba.
- No vamos a afirmar que los preprints de 2026 resuelven Collatz.
- No vamos a usar claims de IA/startups como base matematica.

## Que si podemos afirmar

- Estamos trabajando con fuentes actualizadas hasta el 25 de abril de 2026.
- La conjetura sigue abierta.
- La estructura modular por potencias de 2 es una linea legitima y activa.
- Nuestro laboratorio ya redetecta una familia conocida y puede seguir con analisis reproducible de paridad/residuos.

## Siguiente paso recomendado

Continuar con M3:

- medir prefijos de paridad para clases `2^k - 1`;
- comparar contra clases control cercanas: `2^k - 2`, `2^k - 3`, residuos altos no Mersenne y residuos aleatorios;
- producir un reporte que explique si el promedio alto viene de trailing ones, sesgo de impares temprano o combinacion de ambos.
