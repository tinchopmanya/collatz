# M21 Angeltveit Verification Route

Fecha: 2026-04-29
Agente: CodexHijo-AngeltveitM21
Rama: main
Commit: no commit
Tarea: evaluar la via Angeltveit 2026 como posible M21

## Fuentes revisadas

Fuente primaria: Vigleik Angeltveit, "An improved algorithm for checking the Collatz conjecture for all n < 2^N", arXiv:2602.10466, enviado el 2026-02-11.

URL: <https://arxiv.org/abs/2602.10466>

Codigo asociado declarado en el paper y visible publicamente: <https://github.com/vigleik0/collatz>

Estado del repositorio externo al 2026-04-29: publico, rama `main`, HEAD observado `f3f09248c7ae7299b8443e112f565f309d97f161`, 18 commits, licencia GPL-3.0, con `main.rs`, `collatz_cudav7.cu`, `collatz_openclv2.cpp`, `compute_kernel2.cl`, `cases_tiny`, `cases_small`, `cases_big` y `Collatzv0.3.pdf`.

No compile el codigo externo en este entorno porque `rustc`/`cargo` no estan instalados localmente. Si hay maquina con Rust o CI, el experimento de reproduccion parece directo. El paper tambien incluye suficiente pseudocodigo y detalles para una reimplementacion corta independiente.

## Resumen tecnico

Angeltveit no propone una prueba de Collatz. Propone un algoritmo de verificacion exhaustiva para todos los `n < 2^N`, con la funcion modificada

```text
T(n) = n/2 si n es par
T(n) = (3n+1)/2 si n es impar
```

La idea central es procesar clases por bits bajos, agregando bits recursivamente desde el bit menos significativo. Usa que la secuencia de ramas par/impar de `T^k(n)` depende solo de los ultimos `k` bits, y que si `n = n0 + a 2^k` entonces

```text
T^k(n) = T^k(n0) + 3^f a
```

donde `f` es el numero de pasos impares en los primeros `k` pasos. Sobre esa estructura combina cuatro filtros:

- `Descent Sieve`: descarta familias completas cuando ya se ve `T^k(n0) < n0`.
- `mod 9 Preimage Sieve`: descarta `n congruente a 2, 4, 5, 8 mod 9` porque caen en la trayectoria de un menor.
- `Path-Merging Sieve`: descarta casos donde `T^k(n)` se une a la trayectoria de un menor.
- `Odd-Even-Even Sieve`: usa un patron de pasos impares seguido de dos pares para detectar union con `(m-1)/2`.

La parte nueva no es cada filtro aislado, sino la orquestacion: una busqueda por bits bajos hasta `N-A`, bitvectors precomputados de largo `2^B` para mirar `B` pasos adicionales, una interseccion bitwise con el filtro mod 9, y luego verificacion manual de los sobrevivientes. En la implementacion reportada usa `A = 6` para CPU, `A = 10` para GPU, `B = 24`, y `306/485` como aproximacion racional a `log(2)/log(3)` para decidir umbrales de descenso.

## Terreno virgen o recorrido

Recorrido en la meta general. La verificacion computacional de Collatz hasta cotas enormes ya tiene una linea madura: Oliveira e Silva 1999, Honda-Ito-Nakano 2017, Barina 2021/2025, Hercher 2023 para consecuencias sobre ciclos, y tablas de path records. El propio paper de Angeltveit se posiciona como mejora sobre Barina, no como paradigma aislado.

Parcialmente virgen en nuestro contexto. M19 estuvo centrado en reescritura, terminacion, AProVE/Matchbox/CeTA y certificacion. Angeltveit abre otra clase de M21: verificacion exhaustiva reproducible, orientada a sieves bitwise y GPU/CPU, con codigo publico pequeno y paper reciente. No es terreno virgen mundial, pero si es una ruta nueva para este repo si queremos pasar de "ideas de prueba" a "artefactos verificables y auditables".

## Potencial cientifico fuerte

Potencial fuerte como contribucion computacional/auditable, no como prueba teorica.

Lo fuerte:

- El paper afirma que, con recursos comparables a Barina para `2^71`, la tecnica podria llegar a `2^77`, y propone como meta modesta `2^75`.
- El repositorio externo tiene implementaciones CPU/GPU y archivos de particion de casos, lo que baja mucho el costo de entrada.
- El metodo es incremental: al subir `N`, la fraccion de enteros que sobreviven a los sieves tiende a bajar, aunque el numero absoluto crece.
- El algoritmo produce artefactos naturales para auditoria: numero de sobrevivientes, checksums, particiones `cases_*`, comparacion CPU/GPU y comparacion contra path records.

Lo debil:

- Aun no reporta verificacion `N >= 72`; el paper dice que espera reportarla en trabajo futuro.
- El codigo Rust declarado es corto pero "no contiene error checking"; para una afirmacion cientifica fuerte necesitamos harness independiente.
- No es facil comparar linealmente contra Barina porque Angeltveit no verifica intervalos `[K,L]`, sino arboles por bits bajos.
- La licencia GPL-3.0 puede condicionar copiar codigo dentro del repo; para evitar contaminacion conviene hacer reimplementacion limpia o tratar el repo externo como dependencia/herramienta separada.

Mi lectura: si M21 busca una contribucion publicable de bajo riesgo, esta ruta es mejor que otra reformulacion teorica especulativa. El objetivo correcto seria "reproduccion independiente y auditoria de un verificador 2026", no "probar Collatz".

## Que aportaria nuestro repo

El aporte diferencial del repo no seria competir por fuerza bruta pura, sino convertir la ruta en artefacto confiable:

- Reimplementacion minimalista e independiente del algoritmo 1/2 en Python o Rust legible, parametrizada por `N`, `A`, `B`, `NUMARRAYS`.
- Tests de equivalencia contra verificacion ingenua para `N` pequenos, por ejemplo `N <= 24`.
- Reproduccion de las cuentas del paper para `N = 35..45`: porcentaje de sobrevivientes y tendencia aproximada `x1.9` por bit.
- Auditoria de checksums y particiones del repo externo (`cases_tiny`, `cases_small`, `cases_big`) con hashes fijos.
- Comparacion automatica contra path records conocidos y contra una implementacion independiente de `T`.
- Registro de entorno, comandos, version de compilador, flags, GPU/CPU, tiempos y hashes para no depender de logs informales.

Esto encaja bien con la filosofia M19 de certificacion: no aceptar "mi GPU corrio" como evidencia, sino empaquetar fuente, parametros, casos, logs y checksums reproducibles.

## Primer experimento reproducible de bajo costo

Experimento M21a recomendado: prototipo CPU pequeno, sin GPU.

Objetivo: validar que entendemos el algoritmo, no batir records.

Pasos:

1. Implementar un script local independiente `m21_angeltveit_probe.py` o equivalente Rust pequeno que reproduzca las tres fases para parametros chicos, por ejemplo `N in {16, 20, 24, 28}`, `A = 4..6`, `B = 8..12`.
2. Comparar el conjunto de numeros descartados/sobrevivientes contra una verificacion ingenua que itera `T` hasta caer por debajo de `n`.
3. Reproducir los cuatro sieves por separado y reportar cuanto elimina cada uno.
4. Descargar el repo externo a una carpeta temporal o submodulo no integrado, fijar HEAD `f3f09248c7ae7299b8443e112f565f309d97f161`, y comparar al menos `cases_tiny` con nuestra interpretacion del estado `(base, sigfig, threepower, number, doubleeven, numevens)`.
5. Si hay Rust disponible, compilar `main.rs` externo sin modificar o con constantes reducidas y correr una particion pequena; si no, mantener el prototipo Python como oraculo auditable.

Criterio de exito barato:

- Para `N <= 24`, el prototipo no deja ningun falso sobreviviente que contradiga la verificacion ingenua y no descarta ningun caso sin poder justificarlo por uno de los sieves.
- Las estadisticas por `N` muestran la misma direccion cualitativa que el paper: el porcentaje sobreviviente baja o se mantiene muy por debajo de un chequeo ingenuo.
- Hay un manifiesto con parametros, tiempos y SHA-256 de cualquier entrada externa usada.

## Podemos reproducir o implementar un prototipo util?

Si. Hay detalles suficientes y codigo suficiente.

El paper da los lemas necesarios, el pseudocodigo de la recursion por bits, los valores concretos `A`, `B`, `306/485`, la organizacion de bitvectors, y la estrategia de verificacion final. El repositorio externo confirma que hay una implementacion compacta en Rust y variantes CUDA/OpenCL. Para un prototipo util no hace falta empezar por GPU: el valor inicial esta en reproducir los sieves y las cuentas chicas con una implementacion independiente y bien testeada.

La unica cautela importante es no convertir un port directo del codigo GPL en codigo propio sin decidir politica de licencia. Para M21a alcanza con un prototipo desde paper, con tests de caja negra contra el repo externo cuando sea posible.

## Criterio de abandono

Abandonar M21 si ocurre cualquiera de estas condiciones:

- No logramos reproducir, en una semana corta de trabajo, los casos pequenos `N <= 24` contra verificacion ingenua con cero discrepancias.
- La interpretacion de `cases_tiny`/estado interno del codigo externo no cuadra con el paper y no encontramos una explicacion simple.
- La reproduccion de `N = 35..45` queda muy lejos de los porcentajes reportados, aun usando los mismos parametros `A = 6`, `B = 24`, `NUMARRAYS = 8`.
- El unico camino viable requiere copiar masivamente codigo GPL al repo sin una decision explicita de licencia.
- La ruta no produce artefactos auditablemente mejores que "ejecutar el repo externo"; en ese caso no hay aporte propio suficiente.

No abandonaria solo porque no tengamos GPU. La primera pregunta cientifica de M21 es de reproducibilidad y auditoria, y esa se puede responder en CPU con cotas pequenas.

## Recomendacion

Abrir M21a con alcance acotado. La via Angeltveit no es terreno virgen mundial, pero si es una oportunidad fuerte para que el repo aporte una reproduccion independiente, parametrizada y auditable de un algoritmo 2026 con codigo publico. Es probablemente mas productiva que buscar otra "prueba" informal de Collatz, siempre que mantengamos el objetivo como verificacion computacional reproducible y no como afirmacion teorica global.
