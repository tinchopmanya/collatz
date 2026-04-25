# Investigacion sobre Collatz - Novena Ola: anti-persistencia entre bloques

Fecha de cierre de esta ola: 2026-04-25 02:45:03 -03:00
Estado: novena ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzNovenaOla.md](ResumenInvestigacionSobreCollatzNovenaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Octava](InvestigacionSobreCollatzOctavaOla.md)
Reporte tecnico: [reports/antipersistence_limit_1000000.md](reports/antipersistence_limit_1000000.md)

## 1. Objetivo

La octava ola mostro que el modelo geometrico independiente explica muy bien el cuerpo de la distribucion, pero sobreproduce algunos extremos. La hipotesis natural fue:

> despues de un bloque expansivo real, el siguiente bloque podria tener menor probabilidad de ser expansivo que en el modelo.

La novena ola mide esa anti-persistencia directamente.

## 2. Metodo

Se agrego:

```text
experiments/analyze_antipersistence.py
```

El script compara cadenas reales y modeladas midiendo:

- correlacion entre factores logaritmicos consecutivos;
- probabilidad de expansion despues de expansion;
- probabilidad de expansion despues de cola larga;
- probabilidad de expansion despues de `exit_v2` alto;
- distribucion de rachas expansivas consecutivas.

La corrida principal fue:

```powershell
python experiments\analyze_antipersistence.py --limit 1000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix antipersistence_limit_1000000
```

## 3. Resultado principal

| Fuente | Corr log_i, log_{i+1} | P exp despues de exp | Max racha expansiva |
| --- | ---: | ---: | ---: |
| Real | 0.003178993200 | 0.28551273 | 10 |
| Modelo | -0.002183105526 | 0.28606594 | 11 |

La anti-persistencia simple no aparece.

En particular, la expansion despues de expansion es practicamente igual en real y modelo.

## 4. Rachas expansivas

Las rachas de bloques expansivos tambien son muy similares:

| Max racha | Real | Modelo |
| ---: | ---: | ---: |
| 0 | 0.71373143 | 0.71377743 |
| 1 | 0.19620439 | 0.19620639 |
| 2 | 0.06236812 | 0.06245412 |
| 3 | 0.01961404 | 0.01959804 |
| 4 | 0.00571201 | 0.00556801 |
| 5 | 0.00172400 | 0.00169800 |

Esto debilita la idea de que el modelo sobreproduce extremos simplemente porque permite demasiadas expansiones consecutivas.

## 5. Senal secundaria

El condicionamiento mas interesante no fue "bloque expansivo", sino:

```text
exit_v2 previo >= 5
```

| Fuente | Conteo | P siguiente expansivo | Promedio siguiente cola |
| --- | ---: | ---: | ---: |
| Real | 1458 | 0.23662551 | 1.89574760 |
| Modelo | 1425 | 0.28140351 | 2.00491228 |

Esto podria indicar que despues de una salida muy divisible por `2`, la cadena real queda en una clase que reduce la cola o la expansion siguiente. Pero la muestra es chica y necesita escalado.

## 6. Que se logro

- Se testeo una hipotesis concreta de anti-persistencia.
- Se encontro resultado negativo para la forma simple de la hipotesis.
- Se confirmo que rachas expansivas reales y modeladas son casi iguales.
- Se detecto un posible sesgo condicionado por `exit_v2` alto.

## 7. Que no se logro

- No se probo Collatz.
- No se explico todavia por que el modelo geometrico sobreproduce extremos.
- No se demostro una dependencia aritmetica.
- No se puede afirmar que el sesgo de `exit_v2 >= 5` sea estable sin mas datos.

## 8. Veredicto

La anti-persistencia simple no es el fenomeno correcto. Eso ayuda: elimina una explicacion demasiado facil.

La nueva direccion es mas aritmetica:

> estudiar que congruencias quedan despues de salidas con `exit_v2` alto y si esas congruencias sesgan la siguiente cola.

Si ese efecto persiste, seria una pieza mucho mas formalizable que mirar "expansion" de manera generica.
