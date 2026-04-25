# Investigacion sobre Collatz - Cuarta Ola: laboratorio computacional y familias residuales

Fecha de cierre de esta ola: 2026-04-25 01:57:35 -03:00
Estado: cuarta ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzCuartaOla.md](ResumenInvestigacionSobreCollatzCuartaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Olas anteriores: [Primera](InvestigacionSobreElProblemaDeCollatz.md) | [Segunda](InvestigacionSobreCollatzSegundaOla.md) | [Tercera](InvestigacionSobreCollatzTerceraOla.md)

## 1. Objetivo

La cuarta ola cambia el modo de trabajo. Las primeras olas fueron principalmente bibliograficas y exploratorias. Esta ola abre un laboratorio computacional reproducible para estudiar orbitas extremas de Collatz.

El objetivo no fue probar la conjetura. El objetivo fue construir una base verificable para medir:

- pasos totales;
- stopping time o primer descenso por debajo de `n`;
- altura maxima;
- clases residuales modulo potencias de 2;
- prefijos de paridad;
- excursion temprana.

La pregunta concreta fue:

> Que estructura tienen las orbitas que mas se apartan del comportamiento promedio?

## 2. Estado actualizado del campo

Antes de interpretar resultados, se verifico actualidad y originalidad. La conclusion es importante:

- estamos trabajando con fuentes actualizadas hasta el 25 de abril de 2026;
- hay preprints muy recientes de marzo y abril de 2026;
- la conjetura de Collatz sigue abierta;
- la estructura por clases residuales modulo potencias de 2 es clasica y activa;
- la familia `-1 mod 2^k` no debe presentarse como descubrimiento nuevo.

Fuentes recientes relevantes:

- Katharina Lodders, "Selection Rules and Channel Structure in a Base Octave Model of Collatz Dynamics", enviado el 22 de abril de 2026: <https://arxiv.org/abs/2604.20181>
- Edward Y. Chang, "Exploring Collatz Dynamics with Human-LLM Collaboration", revision v6 del 22 de abril de 2026: <https://arxiv.org/abs/2603.11066>
- Edward Y. Chang, "A Structural Reduction of the Collatz Conjecture to One-Bit Orbit Mixing", enviado el 24 de marzo de 2026: <https://arxiv.org/abs/2603.25753>
- Bonacorsi y Bordoni, "Bayesian Modeling of Collatz Stopping Times", enviado el 4 de marzo de 2026: <https://arxiv.org/abs/2603.04479>
- Angeltveit, "An improved algorithm for checking the Collatz conjecture for all n < 2^N", enviado el 11 de febrero de 2026: <https://arxiv.org/abs/2602.10466>

Fuentes clasicas o de referencia:

- Terras, "A stopping time problem on the positive integers": <https://eudml.org/doc/205476>
- Klee-Wagon via OEIS A324248: <https://oeis.org/A324248>
- Winkler, "New results on the stopping time behaviour of the Collatz 3x + 1 function": <https://arxiv.org/abs/1504.00212>
- Lagarias, "The 3x+1 Problem: An Overview": <https://arxiv.org/abs/2111.02635>

## 3. Construccion del laboratorio

Se agrego un paquete minimo en Python:

- [src/collatz/core.py](src/collatz/core.py)
- [tests/test_core.py](tests/test_core.py)

Funciones implementadas:

- `classic_step(n)`;
- `accelerated_step(n)`;
- `orbit(n)`;
- `compute_metrics(n)`.

Metricas de `compute_metrics`:

- `total_steps`;
- `stopping_time`;
- `max_value`;
- `odd_steps`;
- `even_steps`;
- `parity_prefix`;
- `reached_one`;
- `terminal_value`.

Tests basicos:

- pasos clasicos conocidos;
- pasos acelerados conocidos;
- orbita de `27`;
- metricas de `1`, `3` y `27`;
- validacion de inputs invalidos.

Verificacion:

```powershell
python -m unittest discover -s tests
```

Resultado: 5 tests pasan.

## 4. Records hasta un millon

Script:

- [experiments/generate_records.py](experiments/generate_records.py)

Reportes:

- [reports/records_limit_100000.md](reports/records_limit_100000.md)
- [reports/records_limit_1000000.md](reports/records_limit_1000000.md)

Para `n <= 1000000`, los records fueron:

| Tipo de record | n | Pasos totales | Stopping time | Maximo alcanzado |
| --- | ---: | ---: | ---: | ---: |
| Tiempo total | 837799 | 524 | 171 | 2974984576 |
| Stopping time | 626331 | 508 | 287 | 7222283188 |
| Altura maxima | 704511 | 242 | 119 | 56991483520 |

Lectura:

- El record clasico de pasos totales dentro del millon, `837799`, fue reproducido.
- El maximo de pasos totales, el maximo de stopping time y la maxima altura no son el mismo numero.
- Por lo tanto, las orbitas extremas no son un fenomeno unico: hay que separar duracion, primer descenso y crecimiento maximo.

## 5. Residuos modulo potencias de 2

Script:

- [experiments/analyze_residues.py](experiments/analyze_residues.py)

Reportes:

- [reports/residue_mod_128_limit_100000.md](reports/residue_mod_128_limit_100000.md)
- [reports/residue_mod_128_limit_1000000.md](reports/residue_mod_128_limit_1000000.md)
- [reports/residue_mod_256_limit_1000000.md](reports/residue_mod_256_limit_1000000.md)
- [reports/residue_mod_512_limit_1000000.md](reports/residue_mod_512_limit_1000000.md)

Resultado central:

| Modulo | Clase con mayor promedio de pasos totales | Clase con mayor promedio de stopping time |
| ---: | ---: | ---: |
| 128 | 127 | 127 |
| 256 | 255 | 255 |
| 512 | 511 | 511 |

La familia `-1 mod 2^k` domina en promedio para las metricas comparadas.

Pero este no es un descubrimiento nuevo. Esta familia ya esta conectada con resultados clasicos y tablas de dropping/stopping time, especialmente via Terras, Klee-Wagon y OEIS A324248.

El aporte de esta ola es distinto:

- reproducir la senal con codigo versionado;
- medirla contra controles;
- cuantificar promedios, records y excursion temprana;
- dejar datos regenerables.

## 6. Prefijos de paridad

Script:

- [experiments/analyze_parity_prefixes.py](experiments/analyze_parity_prefixes.py)

Reporte:

- [reports/parity_prefix_mod_512_limit_1000000.md](reports/parity_prefix_mod_512_limit_1000000.md)

Clases comparadas:

- `511`, `510`;
- `255`, `254`;
- `127`, `126`;
- `447`, `283`;
- `167`, `155`;
- `1`, `0`.

Resultado:

| Residuo | Promedio pasos | Promedio stopping time | Tasa impar primeros 16 | Tasa impar primeros 32 |
| ---: | ---: | ---: | ---: | ---: |
| 511 | 189.547875 | 59.422939 | 0.500000 | 0.430828 |
| 510 | 175.530466 | 1.000000 | 0.500000 | 0.409850 |
| 127 | 174.738351 | 46.279058 | 0.500000 | 0.409802 |
| 255 | 173.979007 | 46.601126 | 0.500000 | 0.409786 |
| 0 | 75.987711 | 1.000000 | 0.152394 | 0.232031 |

Lectura:

- Las clases `2^k - 1` muestran un arranque alternante `1,0,1,0...`.
- `511 mod 512` mantiene mayor tasa impar en los primeros 32 pasos que controles cercanos.
- La clase `510 mod 512` tiene alternancia alta pero stopping time 1, porque baja inmediatamente por ser par.

Esto separa tres conceptos:

- alternancia de paridad;
- crecimiento temprano;
- primer descenso.

## 7. Longitud alternante y excursion temprana

Script:

- [experiments/analyze_alternating_prefix.py](experiments/analyze_alternating_prefix.py)

Reporte:

- [reports/alternating_prefix_mod_512_limit_1000000.md](reports/alternating_prefix_mod_512_limit_1000000.md)

Resultado principal:

| Residuo mod 512 | Longitud alternante promedio | Pico temprano promedio | Promedio pasos totales | Promedio stopping time |
| ---: | ---: | ---: | ---: | ---: |
| 511 | 19.993856 | 347.125344 | 189.547875 | 59.422939 |
| 510 | 18.993856 | 136.859853 | 175.530466 | 1.000000 |
| 255 | 16.000000 | 175.302741 | 173.979007 | 46.601126 |
| 254 | 15.000000 | 54.801260 | 161.331797 | 1.000000 |
| 127 | 14.000000 | 150.722211 | 174.738351 | 46.279058 |
| 126 | 13.000000 | 17.771604 | 149.414235 | 1.000000 |

Lectura:

- `511 mod 512` tiene casi 20 pasos alternantes promedio.
- `511 mod 512` tambien tiene el mayor pico temprano promedio entre las clases comparadas.
- Los controles pares `510`, `254`, `126` ayudan a mostrar que alternancia no equivale a stopping time alto.
- La estructura `2^k - 1` induce crecimiento temprano, pero el comportamiento posterior decide el tiempo total.

## 8. Que es aporte y que no

No es aporte original:

- observar que clases tipo `2^k - 1` son especiales;
- usar residuos modulo potencias de 2;
- conectar stopping time con clases residuales;
- notar la importancia de trailing ones o Mersenne tails.

Si es aporte operativo de esta ola:

- dejar un laboratorio reproducible;
- redetectar un patron conocido con scripts propios;
- medir promedios por clase hasta `n <= 1000000`;
- comparar clases Mersenne-like contra controles pares y no Mersenne;
- conectar residuos, paridad, excursion temprana y stopping time en reportes navegables;
- corregir el encuadre de originalidad.

## 9. Hipotesis candidata para formalizacion

La siguiente pieza matematica pequena podria ser:

> Si `n == -1 mod 2^k`, entonces bajo el mapa clasico de Collatz los primeros pasos presentan un prefijo alternante de paridad de longitud controlada. Ese prefijo induce una cota inferior explicita para la excursion temprana.

Esta hipotesis no prueba Collatz. Pero si puede convertirse en un lemma util para explicar por que las clases `-1 mod 2^k` tienen alto promedio de crecimiento temprano y stopping time.

Un segundo lemma podria comparar `2^k - 1` con `2^k - 2`:

> Las clases pares vecinas heredan parte de la alternancia, pero tienen stopping time 1 porque descienden inmediatamente.

Eso ayudaria a formalizar la distincion entre crecimiento temprano y primer descenso.

## 10. Riesgos

- Confundir redeteccion con originalidad.
- Sobrerreclamar sobre una muestra finita.
- Usar preprints recientes como resultados establecidos.
- Mezclar mapa clasico, acelerado y reducido sin especificar.
- Medir promedios donde hacen falta distribuciones completas.

## 11. Conclusion de la cuarta ola

La cuarta ola logro convertir el repo en un laboratorio computacional real. El laboratorio reprodujo records conocidos, detecto una familia estructural conocida (`-1 mod 2^k`), la comparo contra controles y encontro una explicacion empirica clara: prefijos de paridad alternantes y crecimiento temprano.

El resultado no es revolucionario todavia, pero si es un avance metodologico. Ahora hay codigo, tests, reportes y una hipotesis pequena para formalizar.

La siguiente ola deberia intentar convertir la observacion en lemmas:

- lemma de prefijo alternante para `2^k - 1`;
- lemma de excursion temprana;
- comparacion formal entre clases impares Mersenne-like y controles pares;
- vinculacion con Terras/Klee-Wagon/OEIS para no duplicar literatura.
