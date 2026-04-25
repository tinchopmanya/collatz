# Investigacion sobre Collatz - Duodecima Ola: sesgo de supervivencia orbital

Fecha de cierre de esta ola: 2026-04-25 10:00:03 -03:00
Estado: duodecima ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzDuodecimaOla.md](ResumenInvestigacionSobreCollatzDuodecimaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Undecima](InvestigacionSobreCollatzUndecimaOla.md)
Reporte tecnico: [reports/survival_bias_limit_5000000.md](reports/survival_bias_limit_5000000.md)

## 1. Preguntas antes de investigar

```text
1. Estoy en algo virgen?
Respuesta: no en el marco general. Stopping times, vectores de paridad, modelos aleatorios, bloques Mersenne y heterogeneidad modular ya existen en la literatura.

2. Alguien busco esto antes?
Respuesta: si a nivel amplio. No encontramos aun nuestra medicion exacta por posicion final/interior, profundidad, margen y `prev_exit_v2`.

3. Que parte exacta podria ser nueva?
Respuesta: distinguir que parte de la senal `next_tail = 1` es seleccion inevitable de supervivencia y que parte queda como dependencia real residual.

4. Puedo descubrir algo con esto?
Respuesta: probablemente una explicacion experimental de la sobreproduccion de extremos del modelo, no una prueba de Collatz.

5. Que tan lejos estoy de algo relevante?
Respuesta: lejos de una demostracion, pero cerca de una formulacion mas honesta del fallo del modelo independiente.

6. Que haria que sigamos?
Respuesta: que quede una diferencia real-modelo despues de separar bloque final e interior.

7. Que haria que abandonemos?
Respuesta: que todas las diferencias desaparezcan al hacer esa separacion.
```

## 2. Objetivo

La ola anterior mostro que `exit_v2 = 5` no era una ley local estatica: en todos los bloques locales, la cola siguiente vuelve a distribucion geometrica.

Esta ola pregunta:

```text
El sesgo observado se explica completamente por el hecho de mirar cadenas que sobreviven hasta cierto punto, o queda una dependencia real residual?
```

## 3. Metodo

Se agrego:

```text
experiments/analyze_survival_bias.py
```

Comando principal:

```powershell
python experiments\analyze_survival_bias.py --limit 5000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix survival_bias_limit_5000000
```

El script compara:

```text
real: impares 3 <= n <= 5000000
modelo: 2499999 cadenas independientes con tail, exit_v2 ~ Geom(1/2)
```

Cada cadena se corta al primer bloque que baja por debajo del valor inicial.

Se agrupo por:

- posicion: `only_block`, `first_block`, `interior_block`, `final_block`;
- profundidad de bloque;
- margen logaritmico antes del bloque;
- duracion total hasta primer descenso;
- `prev_exit_v2`;
- combinacion `prev_exit_v2` + posicion.

## 4. Resultado global

Por posicion, el modelo explica casi perfectamente la seleccion de supervivencia:

| Posicion | tail=1 real | tail=1 modelo | Diff | IC95 |
| --- | ---: | ---: | ---: | --- |
| only_block | 0.70054800 | 0.70110213 | -0.00055413 | [-0.00150428, 0.00039602] |
| interior_block | 0.38646876 | 0.38606060 | 0.00040816 | [-0.00085247, 0.00166879] |
| final_block | 0.68311110 | 0.68213098 | 0.00098012 | [-0.00054502, 0.00250526] |

Esto muestra que:

```text
la mayor parte del sesgo de supervivencia no es una anomalia aritmetica; es lo que tambien produce el modelo independiente al condicionar por seguir vivo o terminar.
```

## 5. Resultado por profundidad y margen

La profundidad y el margen logaritmico tampoco rompen globalmente el modelo.

Senales pequenas:

- `depth_21_plus`: `tail=1` real `0.51596573` vs modelo `0.49637910`, diff `0.01958663`, IC95 `[0.00766010, 0.03151316]`.
- `margin_2_4`: `tail=1` real `0.50406429` vs modelo `0.50019887`, diff `0.00386542`, IC95 `[0.00080908, 0.00692175]`.

Estas senales son menores y mezclan condiciones distintas. No son todavia una teoria.

## 6. Resultado condicionado por `prev_exit_v2 = 5`

Aqui aparece el residuo mas interesante:

| Condicion | tail=1 real | tail=1 modelo | Diff tail=1 | IC95 tail=1 | Exp real | Exp modelo | Diff exp | IC95 exp |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| prev_exit_v2_05 | 0.54447539 | 0.50345455 | 0.04102085 | [0.02227129, 0.05977041] | 0.25979573 | 0.28127273 | -0.02147700 | [-0.03816197, -0.00479203] |
| prev_exit_v2_05__final_block | 0.70495151 | 0.66748047 | 0.03747104 | [0.00876201, 0.06618006] | 0.00000000 | 0.00000000 | 0.00000000 | [0.00000000, 0.00000000] |
| prev_exit_v2_05__interior_block | 0.45271454 | 0.40614137 | 0.04657317 | [0.02320157, 0.06994477] | 0.40834793 | 0.44814600 | -0.03979807 | [-0.06316752, -0.01642863] |

Lo importante es la fila `interior_block`.

Aunque se quiten los bloques finales, despues de `prev_exit_v2 = 5` el real sigue teniendo:

```text
mas next_tail = 1
menos expansion siguiente
```

que el modelo.

## 7. Interpretacion

La lectura anterior:

```text
exit_v2 = 5 es una clase local especial
```

sigue descartada.

La lectura nueva:

```text
exit_v2 = 5 + supervivencia orbital + bloque interior produce una dependencia fina no capturada por el modelo independiente.
```

Esta es una afirmacion mas pequena, pero mas precisa.

## 8. Preguntas despues de investigar

```text
1. La respuesta sobre originalidad cambio?
Respuesta: si. El sesgo global de supervivencia no es terreno virgen ni sorprendente. El residuo condicionado por `prev_exit_v2 = 5` en bloques interiores es la parte que merece revision.

2. La probabilidad de relevancia subio, bajo o quedo igual?
Respuesta: subio un poco respecto de la ola anterior, porque no todo quedo explicado por final/interior.

3. Se encontro una senal robusta o solo seleccion?
Respuesta: ambas. La seleccion global queda explicada por el modelo; queda una senal residual localizada.

4. Que aprendimos que no sabiamos antes?
Respuesta: el modelo independiente captura muy bien la forma gruesa de la supervivencia, pero falla en una condicion fina.

5. Conviene seguir, escalar, formalizar o abandonar?
Respuesta: seguir, pero sin escalar ciegamente. Hay que aislar residuos y margenes dentro de `prev_exit_v2 = 5` + interior.

6. Cual es la siguiente pregunta minima?
Respuesta: que variable explica el exceso de `next_tail = 1`: profundidad, margen, residuo de `q`, residuo del siguiente impar o combinacion?
```

## 9. Veredicto

No hay prueba, ni lemma global, ni terreno virgen amplio.

Pero si hay un resultado util:

```text
El modelo independiente explica la supervivencia global, pero no explica completamente la dependencia posterior a `prev_exit_v2 = 5` entre bloques interiores.
```

La siguiente ola debe ser quirurgica: descomponer esa fila, no ampliar todo el universo.
