# Resumen de la investigacion sobre Collatz - Novena Ola

Fecha de cierre de esta ola: 2026-04-25 02:45:03 -03:00
Investigacion completa: [InvestigacionSobreCollatzNovenaOla.md](InvestigacionSobreCollatzNovenaOla.md)
Conclusion dinamica: [Conlusion.md](Conlusion.md)
Reporte tecnico: [reports/antipersistence_limit_1000000.md](reports/antipersistence_limit_1000000.md)

## Resumen fuerte corto

La novena ola puso a prueba una hipotesis nacida de la octava: quizas Collatz real sobrevive menos a extremos que el modelo independiente porque tiene anti-persistencia entre bloques expansivos. Se midieron factores logaritmicos consecutivos en cadenas odd-to-odd reales hasta `n <= 1000000` y se compararon contra el modelo geometrico independiente.

El resultado fue negativo para la hipotesis simple. La correlacion entre factores consecutivos fue casi cero: `0.003178993200` en real y `-0.002183105526` en modelo. La probabilidad de que el siguiente bloque sea expansivo despues de un bloque expansivo fue tambien casi igual: `0.28551273` real contra `0.28606594` modelo. Las rachas expansivas consecutivas se parecieron mucho.

Esto significa que la diferencia extrema detectada en la octava ola no se explica simplemente por "despues de subir, Collatz tiende a bajar". Esa idea era atractiva, pero los datos no la sostienen.

La senal mas interesante aparecio al condicionar por salidas con `exit_v2 >= 5`. En ese caso, la probabilidad real de siguiente expansion fue `0.23662551`, frente a `0.28140351` en el modelo, y la siguiente cola promedio fue menor. La muestra es chica, asi que no se puede afirmar una ley. Pero ahora el hilo mas prometedor es estudiar congruencias asociadas a `exit_v2` alto.

## Resumen fuerte ampliado

La octava ola habia mostrado algo sutil: el modelo geometrico independiente explica muy bien la distribucion gruesa de bloques hasta descenso, pero parece producir mas extremos que la dinamica real. La primera explicacion tentativa fue anti-persistencia: tal vez despues de un bloque expansivo, la dinamica real hace menos probable otra expansion.

La novena ola midio exactamente eso. Para cada cadena real y modelada se registraron los factores logaritmicos locales, si cada bloque era expansivo, las rachas expansivas y varios condicionamientos sobre el bloque anterior. El resultado fue claro: no hay anti-persistencia simple. La correlacion de factores consecutivos es casi nula, la probabilidad de expansion despues de expansion es casi identica a la del modelo, y la distribucion de rachas expansivas coincide muy bien.

Este resultado negativo es util. Evita construir una teoria sobre una intuicion falsa o demasiado gruesa. Si hay una diferencia real entre Collatz y el modelo independiente, no parece estar en la variable "expansivo/no expansivo" por si sola.

El unico desvio interesante aparecio al condicionar por `exit_v2` alto. Cuando el bloque anterior sale con muchas divisiones por dos (`exit_v2 >= 5`), la cadena real muestra menor probabilidad de expansion siguiente y menor cola promedio que el modelo. Esto podria deberse a congruencias aritmeticas dejadas por una salida muy divisible. Pero el conteo es bajo, por lo que la proxima etapa debe medir varios umbrales `exit_v2 >= k`, escalar muestra y calcular si el efecto persiste.

La conclusion es prudente: no encontramos anti-persistencia de primer orden, pero encontramos una pregunta mas precisa y matematizable.
