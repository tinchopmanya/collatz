# Investigacion sobre Collatz - Undecima Ola: seleccion de muestra en `exit_v2 = 5`

Fecha de cierre de esta ola: 2026-04-25 09:45:21 -03:00
Estado: undecima ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzUndecimaOla.md](ResumenInvestigacionSobreCollatzUndecimaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Decima](InvestigacionSobreCollatzDecimaOla.md)
Reporte tecnico: [reports/exit_v2_selection_limit_5000000.md](reports/exit_v2_selection_limit_5000000.md)

## 1. Preguntas antes de investigar

```text
1. Estoy en algo virgen?
Respuesta: no en el marco general. Bloques de Mersenne, salida r(x), mezcla y clases modulo 2^m ya aparecen en Campbell 2025.

2. Alguien busco esto antes?
Respuesta: si a nivel de marco. No habia que presumir originalidad; habia que verificar si nuestra senal `exit_v2 = 5` era local o producto de muestreo.

3. Que parte exacta podria ser nueva?
Respuesta: comparar la transicion local de todos los bloques contra los pares de cadenas sobrevivientes antes del primer descenso.

4. Puedo descubrir algo con esto?
Respuesta: si, pero probablemente negativo: descubrir que una pista no es local tambien es avance porque evita formalizar una falsa causa.

5. Que tan lejos estoy de algo relevante?
Respuesta: lejos de probar Collatz. Cerca de entender una diferencia entre modelo geometrico independiente y orbitas reales condicionadas.

6. Que haria que sigamos?
Respuesta: que `exit_v2 = 5` sesgue tambien la muestra local de todos los bloques.

7. Que haria que abandonemos?
Respuesta: que la muestra local coincida con el modelo geometrico y la desviacion solo aparezca en cadenas sobrevivientes.
```

## 2. Objetivo

La decima ola encontro que, dentro de cadenas odd-to-odd antes del primer descenso, los bloques posteriores a:

```text
exit_v2 = 5
```

eran menos expansivos que el modelo geometrico independiente.

Esta ola pregunta:

```text
Ese efecto es una ley local de la clase exit_v2 = 5, o aparece por el condicionamiento de estar mirando cadenas que aun no descendieron?
```

## 3. Congruencia exacta

Para un impar:

```text
n = 2^s q - 1
s = v2(n + 1)
q impar
```

la salida del bloque es:

```text
B(n) = (3^s q - 1) / 2^r
r = v2(3^s q - 1)
```

La condicion exacta:

```text
r = 5
```

equivale a:

```text
3^s q = 33 mod 64
q = 3^(-s) + 32 mod 64
```

Si escribimos:

```text
3^s q = 33 + 64h
```

entonces:

```text
B(n) = 1 + 2h
B(n) + 1 = 2(h + 1)
v2(B(n) + 1) = 1 + v2(h + 1)
```

Esto muestra que `exit_v2 = 5` no deberia romper por si solo la ley geometrica de la cola siguiente, salvo que el parametro `h` no este mezclado uniformemente.

## 4. Metodo

Se agrego:

```text
experiments/analyze_exit_v2_selection.py
```

Comando:

```powershell
python experiments\analyze_exit_v2_selection.py --limit 5000000 --max-blocks 256 --targets 1,2,3,4,5,6,7,8 --out-dir reports --prefix exit_v2_selection_limit_5000000
```

El script compara dos fuentes:

```text
local_all_starts
```

Todos los impares `n <= 5000000`, tomando una transicion local despues de un bloque con cierto `exit_v2`.

```text
chain_before_descent
```

Pares consecutivos dentro de cadenas odd-to-odd que aun no descendieron por debajo del valor inicial. Esta es la muestra usada por las olas de rachas/duracion.

## 5. Resultado principal

Para `prev_exit_v2 = 5`:

| Fuente | Pares | P siguiente expansion | Diff vs geometrico | Avg next_tail | Avg next_exit_v2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| local_all_starts | 78124 | 0.28628846 | 0.00001396 | 2.00011520 | 1.99953919 |
| chain_before_descent | 5385 | 0.25979573 | -0.02647877 | 1.92423398 | 1.96620241 |

La muestra local coincide practicamente perfecto con el modelo geometrico.

La desviacion aparece solo cuando miramos cadenas sobrevivientes antes del primer descenso.

## 6. Mecanismo del sesgo

En la muestra local:

```text
P(next_tail = 1 | prev_exit_v2 = 5) = 0.50000000
```

En cadenas sobrevivientes:

```text
P(next_tail = 1 | prev_exit_v2 = 5) = 0.54447539
```

Como `next_tail = 1` no puede generar un bloque expansivo, esta sobre-representacion explica casi toda la caida de expansion.

Descomposicion:

| Fuente | Real | Geometrico | Cola observada + exit geometrico | Cola geometrica + exit observado |
| --- | ---: | ---: | ---: | ---: |
| local_all_starts | 0.28628846 | 0.28627450 | 0.28627991 | 0.28628648 |
| chain_before_descent | 0.25979573 | 0.28627450 | 0.26158600 | 0.28958020 |

La cola observada explica la baja. El `exit_v2` siguiente observado no la explica.

## 7. Preguntas despues de investigar

```text
1. La respuesta sobre originalidad cambio?
Respuesta: si, baja para la pista `exit_v2 = 5`. La congruencia local es simple y vuelve a la ley geometrica.

2. La probabilidad de relevancia subio, bajo o quedo igual?
Respuesta: bajo para un lemma local sobre `exit_v2 = 5`; subio para estudiar sesgo de supervivencia orbital.

3. Se encontro una senal robusta o solo ruido?
Respuesta: no es ruido, pero tampoco es una ley local. Es un efecto de seleccion de cadenas antes del primer descenso.

4. Que aprendimos que no sabiamos antes?
Respuesta: el modelo local estatico funciona; lo que falla es el muestreo condicionado por supervivencia.

5. Conviene seguir, escalar, formalizar o abandonar?
Respuesta: abandonar la formalizacion de `exit_v2 = 5` como causa local. Seguir con un modelo de supervivencia si queremos explicar por que el modelo sobreproduce extremos.

6. Cual es la siguiente pregunta minima?
Respuesta: que eventos o filtros orbitales sobre-representan `next_tail = 1` y reducen rachas expansivas reales?
```

## 8. Veredicto

La decima ola habia encontrado una senal real. La undecima ola muestra que la interpretacion correcta no es:

```text
exit_v2 = 5 causa localmente menor expansion.
```

sino:

```text
en cadenas que aun no descendieron, la muestra de transiciones queda sesgada hacia colas siguientes mas cortas.
```

Esto cambia la direccion del roadmap. La pregunta relevante ya no es un lemma local para `exit_v2 = 5`; es el mecanismo de seleccion que filtra las transiciones en orbitas largas.
