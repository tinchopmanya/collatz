# Investigacion

Archivo central y log maestro de investigaciones.

## Archivos fijos

- [Investigacion.md](Investigacion.md): indice central y log maestro.
- [InvestigacionMapa.md](InvestigacionMapa.md): mapa cronologico con fecha, hora y enlaces.
- [Conlusion.md](Conlusion.md): conclusion dinamica de la ultima ola activa.

## Convencion de nombres

Cada investigacion nueva genera dos archivos:

- `InvestigacionSobreTema.md`
- `ResumenInvestigacionSobreTema.md`

Cada alta nueva tambien debe:

- agregar una entrada en este archivo;
- agregar una entrada en [InvestigacionMapa.md](InvestigacionMapa.md) con fecha y hora;
- actualizar [Conlusion.md](Conlusion.md).

## Log de investigaciones

| Fecha y hora | Tema | Investigacion | Resumen | Estado |
| --- | --- | --- | --- | --- |
| 2026-04-23 03:06:27 -03:00 | Problema de Collatz | [InvestigacionSobreElProblemaDeCollatz.md](InvestigacionSobreElProblemaDeCollatz.md) | [ResumenInvestigacionSobreElProblemaDeCollatz.md](ResumenInvestigacionSobreElProblemaDeCollatz.md) | Primera ola cerrada |
| 2026-04-23 06:20:00 -03:00 | Collatz - Segunda Ola (8 subfrentes) | [InvestigacionSobreCollatzSegundaOla.md](InvestigacionSobreCollatzSegundaOla.md) | [ResumenInvestigacionSobreCollatzSegundaOla.md](ResumenInvestigacionSobreCollatzSegundaOla.md) | Segunda ola cerrada |
| 2026-04-23 06:45:00 -03:00 | Collatz - Tercera Ola (mapa de competencia y propuesta) | [InvestigacionSobreCollatzTerceraOla.md](InvestigacionSobreCollatzTerceraOla.md) | [ResumenInvestigacionSobreCollatzTerceraOla.md](ResumenInvestigacionSobreCollatzTerceraOla.md) | Tercera ola cerrada |
| 2026-04-25 01:57:35 -03:00 | Collatz - Cuarta Ola (laboratorio computacional y familias residuales) | [InvestigacionSobreCollatzCuartaOla.md](InvestigacionSobreCollatzCuartaOla.md) | [ResumenInvestigacionSobreCollatzCuartaOla.md](ResumenInvestigacionSobreCollatzCuartaOla.md) | Cuarta ola cerrada |
| 2026-04-25 02:12:23 -03:00 | Collatz - Quinta Ola (formalizacion del prefijo alternante) | [InvestigacionSobreCollatzQuintaOla.md](InvestigacionSobreCollatzQuintaOla.md) | [ResumenInvestigacionSobreCollatzQuintaOla.md](ResumenInvestigacionSobreCollatzQuintaOla.md) | Quinta ola cerrada |
| 2026-04-25 02:24:36 -03:00 | Collatz - Sexta Ola (mapa de salida del bloque alternante) | [InvestigacionSobreCollatzSextaOla.md](InvestigacionSobreCollatzSextaOla.md) | [ResumenInvestigacionSobreCollatzSextaOla.md](ResumenInvestigacionSobreCollatzSextaOla.md) | Sexta ola cerrada |
| 2026-04-25 02:32:13 -03:00 | Collatz - Septima Ola (cadenas odd-to-odd y reseteo de cola) | [InvestigacionSobreCollatzSeptimaOla.md](InvestigacionSobreCollatzSeptimaOla.md) | [ResumenInvestigacionSobreCollatzSeptimaOla.md](ResumenInvestigacionSobreCollatzSeptimaOla.md) | Septima ola cerrada |

## Estado actual del repositorio de investigacion

- Hay 7 investigaciones registradas.
- La conclusion dinamica vigente es [Conlusion.md](Conlusion.md).
- La primera ola cubrio un panorama amplio del problema de Collatz.
- La segunda ola profundizo en 8 subfrentes tecnicos.
- La tercera ola mapeo el ecosistema reciente y posibles rutas, pero varios claims de IA/startups deben tratarse como exploratorios hasta verificacion fuerte.
- La cuarta ola construyo el primer laboratorio computacional reproducible, reprodujo records hasta `n <= 1000000`, redetecto la familia `-1 mod 2^k` como benchmark conocido y midio paridad/excursion temprana contra controles.
- La quinta ola formalizo el lemma local: para impar `n`, la longitud exacta del prefijo alternante inicial es `2 * v2(n + 1)`.
- La sexta ola midio la salida `3^s q - 1`, verifico una distribucion geometrica para `v2(3^s q - 1)` y propuso estudiar cadenas odd-to-odd.
- La septima ola encadeno bloques odd-to-odd, midio primer descenso hasta `n <= 1000000` y encontro evidencia fuerte de reseteo de cola.

## Siguiente uso esperado

Cuando se abra una nueva ola, conviene:

- conservar este archivo como indice;
- sumar la nueva entrada al final del log;
- mantener [InvestigacionMapa.md](InvestigacionMapa.md) como cronologia detallada;
- reemplazar o reescribir [Conlusion.md](Conlusion.md) con la nueva conclusion vigente.
