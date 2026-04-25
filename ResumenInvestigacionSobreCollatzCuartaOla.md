# Resumen de la investigacion sobre Collatz - Cuarta Ola

Fecha de cierre de esta ola: 2026-04-25 01:57:35 -03:00
Investigacion completa: [InvestigacionSobreCollatzCuartaOla.md](InvestigacionSobreCollatzCuartaOla.md)
Conclusion dinamica: [Conlusion.md](Conlusion.md)

## Resumen fuerte corto

La cuarta ola cambio el proyecto de Collatz de investigacion bibliografica a laboratorio computacional reproducible. Se implemento un motor minimo en Python, con tests, para calcular pasos totales, stopping time, altura maxima, prefijos de paridad y clases residuales.

El primer resultado fue reproducir records hasta `n <= 1000000`: `837799` tiene el mayor tiempo total con 524 pasos; `626331` tiene el mayor stopping time con 287 pasos antes de bajar de su valor inicial; `704511` alcanza la mayor altura, `56991483520`. Estos records muestran que duracion, primer descenso y altura maxima son metricas distintas.

Luego se analizaron residuos modulo `128`, `256` y `512`. La familia `-1 mod 2^k` quedo primera por promedio de pasos totales y stopping time: `127`, `255`, `511`. Pero esto no es un descubrimiento nuevo; ya esta relacionado con literatura clasica sobre stopping/dropping time, Terras, Klee-Wagon y OEIS A324248. El aporte fue reproducirlo, cuantificarlo y compararlo contra controles.

El analisis de prefijos de paridad mostro que las clases `2^k - 1` tienen arranque alternante `1,0,1,0...`. Para `511 mod 512`, la longitud alternante promedio fue casi 20 pasos y el pico temprano promedio fue `347x`. La clase par vecina `510` tambien alterna mucho, pero tiene stopping time 1, lo que separa crecimiento temprano de primer descenso.

Conclusion: no se probo Collatz ni se descubrio una familia nueva. Si se construyo una base experimental seria y se identifico un lemma candidato: formalizar por que `n == -1 mod 2^k` induce prefijos alternantes y crecimiento temprano.

## Resumen fuerte ampliado

La cuarta ola fue el primer cierre experimental del proyecto. Hasta este punto, las investigaciones sobre Collatz habian sido principalmente panoramicas: estado del problema, resultados parciales, competencia actual, preprints recientes y posibles rutas de trabajo. En esta ola se tomo una decision metodologica importante: dejar de solo leer y empezar a medir con codigo propio.

Se construyo un laboratorio computacional minimo en Python. El nucleo vive en `src/collatz/core.py` y expone funciones para el paso clasico, el paso acelerado, la orbita completa y el calculo de metricas. Las metricas incluyen pasos totales hasta llegar a 1, stopping time o primer descenso por debajo del valor inicial, altura maxima, cantidad de pasos pares/impares y prefijo de paridad. Tambien se agregaron tests unitarios sobre casos conocidos como `1`, `3` y `27`. La verificacion paso correctamente con `python -m unittest discover -s tests`.

El primer experimento reprodujo records hasta `n <= 1000000`. El resultado confirmo que `837799` es el caso con mayor tiempo total dentro del primer millon, con 524 pasos. Pero el mayor stopping time aparecio en `626331`, con 287 pasos hasta bajar de su valor inicial, y la mayor altura maxima aparecio en `704511`, que sube hasta `56991483520`. Este resultado ya fue util porque separa tres fenomenos que suelen mezclarse: duracion total, resistencia a bajar y crecimiento maximo.

Luego se analizaron clases residuales modulo potencias de 2. Para modulo `128`, `256` y `512`, la familia `-1 mod 2^k` quedo primera por promedio de pasos totales y por promedio de stopping time: `127`, `255` y `511`. La tentacion inicial habria sido tratar esto como un hallazgo nuevo, pero se hizo una pausa de auditoria. Al revisar la literatura reciente y clasica, se encontro que esta familia ya esta conectada con resultados sobre dropping/stopping time, clases residuales modulo potencias de 2, Terras, Klee-Wagon y OEIS A324248. Por lo tanto, el patron no es original como objeto matematico.

Eso no vuelve inutil el trabajo. Cambia su valor: el laboratorio redetecta un fenomeno conocido, lo cuantifica con scripts propios, lo compara contra controles y lo deja reproducible. Ese es un avance metodologico sano. En vez de afirmar novedad, la cuarta ola lo reencuadra como benchmark estructural.

El siguiente paso fue medir prefijos de paridad. Para modulo `512`, se compararon clases como `511`, `510`, `255`, `254`, `127`, `126`, `447`, `283`, `167`, `155`, `1` y `0`. El resultado mostro que las clases `2^k - 1` tienen un arranque alternante de paridad `1,0,1,0...`. En `511 mod 512`, la tasa de impares en los primeros 32 pasos fue mayor que en controles cercanos. Esto ofrece una explicacion computacional inicial del promedio alto.

Finalmente se midio la longitud efectiva del prefijo alternante y la excursion temprana dentro de los primeros 64 pasos. `511 mod 512` tuvo casi 20 pasos alternantes promedio y un pico temprano promedio de `347x`, el mayor de las clases comparadas. `510 mod 512` tambien tuvo alternancia larga, casi 19 pasos, pero su stopping time promedio fue 1 porque al ser par baja inmediatamente por debajo de si misma. Esa comparacion es muy instructiva: alternar mucho no significa necesariamente tener alto stopping time; importa desde donde se empieza y como se define el descenso.

La conclusion de la cuarta ola es sobria. No se probo Collatz. No se encontro una familia nueva. No hay que sobrerreclamar. Pero si se logro algo importante para el proyecto: ahora existe una infraestructura reproducible que permite transformar intuiciones en mediciones, y esas mediciones ya conectan residuo, paridad, crecimiento temprano y stopping time.

La proxima ola deberia intentar formalizar un lemma pequeno: si `n == -1 mod 2^k`, entonces los primeros pasos bajo el mapa clasico tienen un prefijo alternante de longitud controlada, y ese prefijo induce una cota inferior para la excursion temprana. Ese lemma no resolveria Collatz, pero seria una pieza matematica clara, verificable y alineada con literatura existente.
