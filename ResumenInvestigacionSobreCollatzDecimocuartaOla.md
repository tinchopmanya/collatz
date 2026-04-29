# Resumen - Collatz Decimocuarta Ola

Fecha: 2026-04-29 09:57:15 -03:00

La decimocuarta ola cambia el centro del proyecto. Despues de cerrar el arco estadistico M12-M18 como descarte disciplinado, la via con mas posibilidad cientifica ya no es seguir midiendo cadenas odd-to-odd, sino movernos hacia sistemas de reescritura, certificacion y filtros low-bit/descent.

El terreno no es virgen en sentido global. Yolcu, Aaronson y Heule ya publicaron en 2023 un enfoque que reduce Collatz a terminacion de sistemas de reescritura mixtos binario-ternarios. Angeltveit propuso en febrero de 2026 un algoritmo low-bit/descent para verificar Collatz hasta cotas grandes, y Barina publico en 2025 la verificacion hasta `2^71`. Por lo tanto, las piezas principales ya existen. La posible novedad esta en combinarlas: usar filtros low-bit/descent como preprocesadores o certificados parciales para familias residuales de rewriting.

Durante M19 se intento recuperar herramientas externas como Matchbox/AProVE. La leccion principal fue operativa: no alcanza con que GitHub Actions diga `success`. Varios runs verdes contenian fallos reales de build. Por eso se agregaron gates estrictos: uno exige binario Matchbox real, `sha256`, `ldd` y `--help`; otro exige `YES` top-level, CPF separado y CeTA `CERTIFIED`. La reconstruccion de Matchbox historico encontro una cadena de fallos Haskell: primero Boolector, despues `wl-pprint-extras`, despues `satchmo`, y luego `atto-lisp/base`. Esto sugiere que seguir parcheando indefinidamente puede volverse arqueologia de dependencias, no avance sobre Collatz.

La via mas prometedora ahora es M22. Se implemento un puente low-bit/rewrite: para S2 con `k=16`, el filtro descarga `7814/8192` clases y deja `378` residuos congelados, con hash reproducible. Esto no prueba Collatz, pero crea un objeto concreto para estudiar. Si esos 378 residuos tienen estructura y pueden convertirse en subfamilias que herramientas de terminacion cierren con certificado, tendriamos un aporte real: benchmark nuevo, reduccion verificable y puente entre dos literaturas que parecen no estar integradas publicamente.

La hipotesis fuerte queda asi: un filtro low-bit/descent certificado podria reducir una familia S2-k a un complemento pequeno, y ese complemento podria cerrarse por rewriting certificado. Esta via se destruye si el complemento crece sin estructura, si las herramientas no mejoran respecto de S2 completo, si aparece un falso positivo low-bit, o si los `YES` dependen de binarios no reproducibles.

La respuesta actual a las preguntas guia es: si estamos avanzando; no estamos en terreno virgen para las piezas; estamos en terreno parcialmente abierto para la combinacion; estamos lejos de una prueba de Collatz, pero a distancia moderada de un resultado computacional publicable si M22 produce reduccion estable y certificable.
