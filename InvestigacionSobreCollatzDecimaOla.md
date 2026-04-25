# Investigacion sobre Collatz - Decima Ola: salidas con alta valuacion 2-adica

Fecha de cierre de esta ola: 2026-04-25 09:31:26 -03:00
Estado: decima ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzDecimaOla.md](ResumenInvestigacionSobreCollatzDecimaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Novena](InvestigacionSobreCollatzNovenaOla.md)
Reporte tecnico: [reports/high_exit_v2_limit_5000000.md](reports/high_exit_v2_limit_5000000.md)

## 1. Preguntas antes de investigar

```text
1. Estoy en algo virgen?
Respuesta: no en el marco general. Bloques Mersenne, salida r(x), mezcla y modelos geometricos ya existen.

2. Alguien busco esto antes?
Respuesta: si a nivel general: Campbell 2025, Bonacorsi/Bordoni 2026 y Chang 2026 tocan bloques, residuos, mezcla o dependencias. No encontramos una tabla exacta como la de esta ola.

3. Que parte exacta podria ser nueva?
Respuesta: medir exit_v2 >= k y exit_v2 = k contra modelo geometrico independiente con intervalos.

4. Que probabilidad real hay de descubrir algo relevante?
Respuesta: baja para prueba global, moderada-baja para una nota experimental si el sesgo persiste.

5. Que evidencia haria que sigamos?
Respuesta: diferencia real-modelo estable y con intervalo lejos de cero al escalar.

6. Que evidencia haria que abandonemos?
Respuesta: efecto no monotono, cambio de signo o desaparicion al escalar.
```

## 2. Objetivo

La novena ola mostro que no habia anti-persistencia simple despues de bloques expansivos, pero detecto una posible senal cuando el bloque anterior tenia:

```text
exit_v2 >= 5
```

La decima ola separa esa condicion por umbrales y valores exactos.

## 3. Metodo

Se agrego:

```text
experiments/analyze_high_exit_v2.py
```

Se ejecutaron dos rangos:

```powershell
python experiments\analyze_high_exit_v2.py --limit 1000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix high_exit_v2_limit_1000000
python experiments\analyze_high_exit_v2.py --limit 5000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix high_exit_v2_limit_5000000
```

Para cada par de bloques consecutivos se midio:

- `exit_v2` del bloque anterior;
- si el bloque siguiente es expansivo;
- log-factor del bloque siguiente;
- cola siguiente;
- diferencia real-modelo con intervalo aproximado al 95%.

## 4. Resultado principal

En `n <= 5000000`, los umbrales mas relevantes fueron:

| Condicion previa | Pares reales | Pares modelo | P exp real | P exp modelo | Diff | IC95 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| exit_v2 >= 4 | 29008 | 29138 | 0.27633756 | 0.28608690 | -0.00974933 | [-0.01705760, -0.00244107] |
| exit_v2 >= 5 | 7128 | 7269 | 0.25968013 | 0.28201954 | -0.02233940 | [-0.03685220, -0.00782660] |
| exit_v2 >= 6 | 1743 | 1769 | 0.25932301 | 0.28434144 | -0.02501843 | [-0.05443342, 0.00439657] |
| exit_v2 >= 7 | 463 | 443 | 0.23110151 | 0.28668172 | -0.05558020 | [-0.11256877, 0.00140837] |

La senal `>=5` sobrevivio al escalado, aunque mas chica que en `n <= 1000000`.

## 5. Resultado por valor exacto

| Condicion previa | Pares reales | Pares modelo | P exp real | P exp modelo | Diff | IC95 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| exit_v2 = 4 | 21880 | 21869 | 0.28176417 | 0.28743884 | -0.00567467 | [-0.01413109, 0.00278174] |
| exit_v2 = 5 | 5385 | 5500 | 0.25979573 | 0.28127273 | -0.02147700 | [-0.03816197, -0.00479203] |
| exit_v2 = 6 | 1280 | 1326 | 0.26953125 | 0.28355958 | -0.01402833 | [-0.04837162, 0.02031496] |
| exit_v2 = 7 | 332 | 320 | 0.19277108 | 0.29062500 | -0.09785392 | [-0.16324166, -0.03246617] |

El valor exacto `exit_v2 = 5` es el candidato mas limpio por ahora: suficiente muestra y diferencia negativa con intervalo bajo cero.

## 6. Interpretacion

La senal no es simplemente:

```text
mayor exit_v2 -> menor siguiente expansion
```

Si fuera asi, esperariamos monotonia clara. No aparece.

La lectura mas prudente es:

```text
ciertos valores de exit_v2, especialmente 5, podrian dejar clases modulares que sesgan el siguiente bloque.
```

Esto es mas aritmetico que estadistico. El siguiente paso deberia derivar la congruencia exacta asociada a `exit_v2 = 5`.

## 7. Preguntas despues de investigar

```text
1. La respuesta sobre originalidad cambio?
Respuesta: no mucho. No es terreno virgen amplio, pero la medicion exacta parece una extension fina no encontrada.

2. La probabilidad de relevancia subio, bajo o quedo igual?
Respuesta: subio un poco. El efecto exit_v2 >= 5 persistio al escalar a 5M.

3. Se encontro una senal robusta o solo ruido?
Respuesta: senal moderada para exit_v2 >= 4/5 y exacto 5; ruido/muestra insuficiente para umbrales mas altos.

4. Que aprendimos que no sabiamos antes?
Respuesta: la variable "expansivo previo" no sirve, pero `exit_v2 = 5` podria ser una clase especial.

5. Conviene seguir, escalar, formalizar o abandonar?
Respuesta: seguir una iteracion mas, pero hacia congruencias, no hacia fuerza bruta.

6. Cual es la siguiente pregunta minima?
Respuesta: que congruencia deja `exit_v2 = 5` y como afecta la distribucion de la siguiente cola?
```

## 8. Veredicto

No se encontro una prueba ni una teoria nueva. Se encontro una senal especifica, medible y algo estable:

```text
Despues de exit_v2 = 5, el siguiente bloque real es menos expansivo que el modelo independiente.
```

Eso podria ser relevante si se transforma en una afirmacion modular exacta.
