# Investigacion sobre Collatz - Septima Ola: cadenas odd-to-odd y reseteo de cola

Fecha de cierre de esta ola: 2026-04-25 02:32:13 -03:00
Estado: septima ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzSeptimaOla.md](ResumenInvestigacionSobreCollatzSeptimaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Sexta](InvestigacionSobreCollatzSextaOla.md)
Reporte tecnico: [reports/odd_chain_limit_1000000.md](reports/odd_chain_limit_1000000.md)

## 1. Objetivo

La sexta ola estudio un solo salto desde un impar hasta el siguiente impar despues del bloque alternante:

```text
n_i -> n_{i+1}
```

La septima ola encadena esos saltos y se pregunta:

> La salida de un bloque conserva informacion de la cola anterior, o la siguiente cola vuelve a comportarse como generica?

Tambien se mide una version comprimida del primer descenso: cuantos bloques odd-to-odd pasan antes de que el impar actual baje por debajo del impar inicial.

## 2. Metodo

Se agrego:

```text
experiments/analyze_odd_chain.py
```

El script recorre todos los impares:

```text
3 <= n <= 1000000
```

Para cada uno itera bloques:

```text
n_i = 2^s q - 1
n_{i+1} = (3^s q - 1) / 2^r
r = v2(3^s q - 1)
```

La cadena se detiene si:

- llega a `1`;
- el impar actual cae por debajo del impar inicial;
- supera `max_blocks`.

La corrida principal uso:

```powershell
python experiments\analyze_odd_chain.py --limit 1000000 --max-blocks 256 --out-dir reports --prefix odd_chain_limit_1000000
```

## 3. Resultado global

No hubo casos que agotaran `256` bloques.

El maximo observado fue:

```text
41 bloques odd-to-odd hasta bajar
```

Los dos primeros records por duracion fueron:

| n | Cola inicial | Bloques | Max impar/n | Max pico/n |
| ---: | ---: | ---: | ---: | ---: |
| 626331 | 2 | 41 | 2882.774119 | 11531.096478 |
| 667375 | 4 | 41 | 924.574042 | 3698.296166 |

Esto no prueba nada global, pero sirve como mapa local: hasta un millon, el descenso comprimido aparece rapido en escala de bloques.

## 4. Cola inicial y tiempo hasta bajar

El promedio de bloques hasta bajar crece con la cola inicial `s = v2(n + 1)`:

| s inicial | Bloques promedio | Max pico/n promedio |
| ---: | ---: | ---: |
| 1 | 1.000000 | 3.000013 |
| 2 | 1.904776 | 10.717955 |
| 3 | 2.311264 | 18.857756 |
| 4 | 3.111968 | 33.753527 |
| 5 | 3.756736 | 51.386230 |
| 6 | 4.582491 | 101.030774 |
| 7 | 5.283666 | 173.858739 |
| 8 | 5.946237 | 259.607361 |
| 9 | 6.614125 | 281.255882 |
| 10 | 7.182377 | 314.757991 |
| 11 | 8.372951 | 449.403736 |
| 12 | 9.368852 | 852.992984 |

Esto confirma la lectura de las olas anteriores: una cola larga de unos produce expansion y retrasa el primer descenso. Pero el efecto no basta para mantener colas largas indefinidamente.

## 5. Reseteo de cola

La medicion mas importante fue la transicion entre colas.

Promedio de `v2(n_{i+1} + 1)` condicionado por `v2(n_i + 1)`:

| Cola actual | Siguiente cola promedio |
| ---: | ---: |
| 1 | 1.999826 |
| 2 | 1.998718 |
| 3 | 2.001123 |
| 4 | 2.002576 |
| 5 | 1.997530 |
| 6 | 1.995833 |
| 7 | 2.001590 |
| 8 | 2.016988 |
| 9 | 2.026300 |
| 10 | 1.985023 |
| 11 | 1.997468 |
| 12 | 2.105528 |

La cola siguiente vuelve a promedio cercano a `2`. Esto sugiere que cada salto odd-to-odd mezcla fuertemente la informacion 2-adica: una cola larga causa expansion, pero no parece producir automaticamente otra cola larga.

## 6. Duracion y altura son metricas distintas

El record de duracion no coincide con el record de altura.

Por altura relativa, los primeros casos fueron:

| n | Cola inicial | Bloques | Max impar/n | Max pico/n |
| ---: | ---: | ---: | ---: | ---: |
| 159487 | 8 | 14 | 13482.586161 | 107860.689285 |
| 270271 | 6 | 38 | 11399.705248 | 91197.641982 |
| 288615 | 3 | 36 | 10675.154573 | 85401.236582 |
| 704511 | 14 | 13 | 1578.200277 | 80895.093930 |

Esto importa para evitar un error de estrategia. Si buscamos posibles avances, no alcanza con buscar "el numero mas dificil". Hay por lo menos dos dificultades:

- mantenerse mucho tiempo por encima del inicio;
- subir extremadamente alto antes de bajar.

Esas dos propiedades se solapan a veces, pero no son equivalentes.

## 7. Primer lemma pequeno detectado

Hay un caso exacto simple:

Si `s = v2(n + 1) = 1` y `n > 1`, entonces el siguiente impar despues del bloque baja por debajo de `n`.

En efecto:

```text
n = 2q - 1
q impar, q > 1
e = 3q - 1
m = e / 2^r <= (3q - 1) / 2 < 2q - 1 = n
```

Esto explica por que toda la clase `1 mod 4` cae en un bloque odd-to-odd.

## 8. Que se logro

- Se implemento un analizador de cadenas odd-to-odd.
- Se midieron todos los impares `3 <= n <= 1000000`.
- Se verifico que todos bajan antes de `256` bloques en esta escala.
- Se encontro maximo observado de `41` bloques.
- Se separaron records de duracion y records de altura.
- Se reforzo experimentalmente la hipotesis de reseteo de cola.

## 9. Que falta

La siguiente ola deberia producir trazas detalladas y comparar contra un modelo estocastico:

- secuencias de colas para records;
- productos logaritmicos de factores locales;
- correlacion real contra independencia;
- simulador geometrico comparable;
- busqueda de desviaciones sistematicas.

Si hay una contribucion publicable de este repositorio, probablemente no sea "encontre un numero raro", sino una descripcion clara de por que los numeros raros se construyen con ciertos patrones de bloques.
