# Resumen de la investigacion sobre Collatz - Decima Ola

Fecha de cierre de esta ola: 2026-04-25 09:31:26 -03:00
Investigacion completa: [InvestigacionSobreCollatzDecimaOla.md](InvestigacionSobreCollatzDecimaOla.md)
Conclusion dinamica: [Conlusion.md](Conlusion.md)
Reporte tecnico: [reports/high_exit_v2_limit_5000000.md](reports/high_exit_v2_limit_5000000.md)

## Resumen fuerte

La decima ola aplico el nuevo filtro de relevancia antes y despues de investigar. La respuesta inicial fue prudente: no estamos en terreno virgen amplio, porque Campbell 2025 ya trabaja bloques Mersenne, salida `r(x)`, mezcla y modelo geometrico. Lo que podia quedar como aporte propio era una medicion fina: condicionar por `exit_v2 >= k` o `exit_v2 = k` y comparar el siguiente bloque real contra el modelo independiente.

Se agrego `experiments/analyze_high_exit_v2.py` y se midieron dos rangos: `n <= 1000000` y `n <= 5000000`. La senal inicial de la novena ola sobrevivio parcialmente. En cinco millones, despues de `exit_v2 >= 5`, la probabilidad real de que el siguiente bloque sea expansivo fue `0.25968013`, contra `0.28201954` en el modelo. La diferencia fue `-0.02233940`, con intervalo aproximado `[-0.03685220, -0.00782660]`. Para `exit_v2 = 5` exacto, la diferencia fue `-0.02147700`, tambien con intervalo bajo cero.

Esto aumenta un poco la probabilidad de que haya una veta real, pero no prueba que sea una ley. La senal no es monotona: `exit_v2 = 6` no queda concluyente, `exit_v2 = 7` sale fuerte pero con poca muestra, y umbrales mayores son demasiado escasos. Por eso la interpretacion correcta no es "mas exit_v2 implica menos expansion", sino algo mas fino: ciertos valores, especialmente `exit_v2 = 5`, podrian dejar clases modulares que sesgan el siguiente bloque.

La conclusion despues de la iteracion es clara: no conviene escalar por fuerza bruta todavia. Conviene derivar la congruencia exacta asociada a `exit_v2 = 5` y estudiar como esa clase afecta `v2(next_odd + 1)` o el siguiente factor logaritmico. Si esa congruencia explica el sesgo, podria haber una nota experimental-formal pequena. Si no, abandonamos la pista.
