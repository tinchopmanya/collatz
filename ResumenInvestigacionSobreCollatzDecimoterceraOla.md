# Resumen fuerte - Decimotercera Ola

La decimotercera ola hizo la prueba de destruccion que Claude recomendo para M14. La pista era el residuo `prev_exit_v2 = 5` + `interior_block`, donde en el primer rango `n <= 5000000` el real tenia `next_tail = 1` en `0.45271454` contra `0.40614137` del modelo.

El resultado fue mixto al principio y negativo al final. En el rango original, la diferencia sobrevive bootstrap y permutacion por cadena, pero no pasa el umbral estricto de Bonferroni `p ajustado < 0.01`: `0.01390268` contando solo M13 y `0.06519232` contando tambien la exploracion del Codex hijo.

La prueba decisiva fue el holdout independiente `5000001 <= n <= 10000000`: real `0.41553749`, modelo `0.40614137`, diferencia `0.00939612`, `p = 0.43201832`, bootstrap CI95 `[-0.01423070, 0.03272495]`. La senal no se reproduce.

El chequeo algebraico local tambien da `P(next_tail = 1 | prev_exit_v2 = 5) = 0.5`, por lo que la congruencia local no explica una anomalia real-modelo.

Conclusion: M14 queda cerrado como descarte limpio. La rama del Codex hijo queda preservada como exploracion, pero no se integra como hallazgo. La leccion importante es metodologica: separar descubrimiento y confirmacion con holdout desde el inicio.
