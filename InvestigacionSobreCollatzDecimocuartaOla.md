# Investigacion sobre Collatz - Decimocuarta Ola

Fecha: 2026-04-29 09:57:15 -03:00
Tema: Rewriting, certificacion y puente low-bit/descent

## Preguntas guia antes de la ola

- Estamos avanzando? Si, pero ya no por encontrar correlaciones estadisticas: avanzamos construyendo una via certificable alrededor de sistemas de reescritura.
- Estamos en terreno virgen? No en el marco general. Yolcu, Aaronson y Heule ya redujeron Collatz a terminacion de sistemas de reescritura de strings. Angeltveit y Barina ya empujan la verificacion computacional low-bit/descent. Lo parcialmente virgen esta en combinar esos dos mundos de forma reproducible.
- Ya alguien vio esto? Si para las piezas: rewriting, pruebas automaticas, verificacion computacional, residuos low-bit. No encontramos todavia una campana publica que use certificados low-bit como preprocesador de familias residuales para herramientas de terminacion sobre los sistemas S1/S2.
- Que tan lejos estamos de algo publicable? Todavia lejos de una prueba de Collatz. Mas cerca de un resultado publicable pequeno si logramos un benchmark nuevo, reproducible, con certificado externo o con reduccion residual clara.
- Posibilidad cientifica fuerte alta? Media-alta solo para el puente M22; baja para seguir acumulando estadistica odd-to-odd; media para reconstruir herramientas historicas si aparece un binario Matchbox/AProVE certificable.

## Contexto actualizado a fines de abril de 2026

La referencia central para el cambio de marco es el trabajo de Emre Yolcu, Scott Aaronson y Marijn Heule, publicado en Journal of Automated Reasoning el 25 de abril de 2023: [An Automated Approach to the Collatz Conjecture](https://link.springer.com/article/10.1007/s10817-022-09658-8). El articulo construye sistemas de reescritura que simulan Collatz y prueba que la terminacion de un sistema mixto binario-ternario es equivalente a la conjetura. Tambien reporta pruebas automaticas de debilitamientos no triviales, pero no una prueba de Collatz.

La version arXiv del mismo trabajo, [arXiv:2105.14697](https://arxiv.org/abs/2105.14697), deja claro que el enfoque es prometedor pero incompleto. El repositorio publico asociado, `emreyolcu/rewriting-collatz`, contiene reglas, pruebas y conversores TPDB. Por lo tanto, nuestro terreno no es virgen en rewriting: estamos sobre una ruta ya abierta por especialistas fuertes.

El frente computacional mas reciente viene de Vigleik Angeltveit, [arXiv:2602.10466](https://arxiv.org/abs/2602.10466), enviado el 11 de febrero de 2026. Su algoritmo verifica Collatz para todos los `n < 2^N` y promete que pasar de `N` a `N+1` cuesta menos del doble. David Barina habia publicado el 2 de mayo de 2025 una verificacion hasta `2^71` en [The Journal of Supercomputing](https://link.springer.com/article/10.1007/s11227-025-07337-0). Esto vuelve fuerte la idea de usar filtros low-bit/descent como componente de una ruta certificable.

Tambien aparece en marzo de 2026 el paper de Edward Chang, [arXiv:2603.25753](https://arxiv.org/abs/2603.25753), que reduce Collatz a un problema de mezcla orbital de un bit. No lo tomamos como prueba, pero es relevante porque vuelve a poner el foco en informacion low-bit, balance orbital y residuos modulo potencias de 2.

En herramientas de terminacion, el estado del arte no puede tratarse como caja negra. El panorama FSCD/TermComp recuerda que AProVE, TTT2, Matchbox, NaTT y CeTA/CPF existen precisamente porque un `YES` no certificado no alcanza. La referencia de Akihisa Yamada, [Termination of Term Rewriting: Foundation, Formalization, Implementation, and Competition](https://drops.dagstuhl.de/opus/volltexte/2023/17988/pdf/LIPIcs-FSCD-2023-4.pdf), resume la importancia de verificadores como CeTA/IsaFoR.

## Lo que se hizo en el repo durante M19-M22

1. Se reabrio el proyecto despues del cierre estadistico M12-M18, pero solo bajo una condicion: reproducir primero resultados existentes antes de buscar extensiones.
2. Se audito la via Yolcu-Aaronson-Heule: reglas, pruebas publicas, posibilidad de convertir S1/S2 a formatos TPDB/ARI y uso de herramientas externas.
3. Se intento recuperar Matchbox/AProVE como herramientas de certificacion. Los runs de GitHub Actions muestran que no basta con ver un workflow verde: varios "success" eran fallos de build ocultos por `continue-on-error`.
4. Se agregaron gates estrictos: `scripts/m19_matchbox_artifact_gate.py` para exigir binario real, `sha256`, `ldd` y `--help`; `scripts/m19_certificate_gate.py` para exigir `YES` top-level, CPF separado y CeTA `CERTIFIED`.
5. Se probo la ruta Boolector/Matchbox. El paquete Ubuntu no traia `boolector.h/libboolector`; compilar Boolector C resolvio una capa, pero el ecosistema Haskell historico abrio fallos sucesivos: `boolector`, `wl-pprint-extras`, `satchmo`, y `atto-lisp/base`.
6. Se implemento M21: un probe independiente low-bit/descent inspirado en Angeltveit, sin copiar codigo GPL, con auditoria estratificada y cero falsos positivos observados en los rangos probados.
7. Se implemento M22: puente entre low-bit/descent y rewriting. Para S2 con `k=16`, el filtro low-bit descarga `7814/8192` clases y deja un complemento congelado de `378` residuos. El hash del complemento queda fijado como `bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210`.

## Lectura cientifica

La reconstruccion de Matchbox historico tiene valor instrumental, no conceptual. Si conseguimos un binario reproducible y un `YES` certificado sobre una familia no trivial, sirve. Si requiere una cadena larga de parches de Haskell, deja de ser investigacion sobre Collatz y pasa a ser arqueologia de dependencias.

La via con mas ceiling ahora es M22: no intentar "probar Collatz" directamente, sino convertir certificados low-bit en una reduccion formal de familias residuales que las herramientas de rewriting puedan atacar. La pregunta concreta es:

```text
Puede un filtro low-bit/descent certificado reducir una familia S2-k a un complemento pequeno
que despues sea cerrado por herramientas de terminacion con prueba verificable?
```

Si la respuesta es si, el aporte podria ser publicable aunque no pruebe Collatz completo: seria un benchmark nuevo, un puente entre dos literaturas y un metodo reproducible. Si la respuesta es no, el descarte tambien sera valioso porque muestra que la reduccion low-bit no ayuda al marco de rewriting.

## Que destruiria la via

- Que el complemento de 378 residuos no tenga estructura explotable y crezca sin control al subir `k`.
- Que los residuos restantes sean exactamente los casos dificiles del sistema original, sin simplificacion real.
- Que ninguna herramienta de terminacion cierre subfamilias residuales mejor que sobre S2 completo.
- Que el probe low-bit tenga un falso positivo o una discrepancia contra verificacion ingenua.
- Que la unica forma de obtener `YES` dependa de binarios no reproducibles o certificados no verificables.

## Siguiente iteracion abierta

Se abrieron cinco trabajos paralelos con worktrees separados:

- `codex-hijo/m19-run-25109605130-gate`: auditar el run Matchbox restante.
- `codex-hijo/m22-residual-stats`: medir estructura del complemento S2-k16.
- `codex-investigador/m23-frontera-web-2026`: confirmar frontera web/papers a fines de abril de 2026.
- `codex-hijo/m19-build-decision-matrix`: decidir si vale uno o dos parches mas de Matchbox o pivot.
- `codex-hijo/m22-kill-criteria`: definir criterios de exito/abandono de M22.

## Preguntas guia despues de la ola

- Estamos avanzando? Si: el proyecto salio de correlaciones debiles y entro en certificacion/reduccion formal.
- Estamos en terreno virgen? Parcialmente. No por rewriting ni low-bit por separado; si potencialmente por el puente reproducible entre ambos.
- Ya alguien lo vio? Las piezas si. La combinacion exacta no fue encontrada todavia como campana publica.
- Que tan lejos estamos? Lejos de demostrar Collatz; a distancia moderada de un resultado computacional publicable si M22 produce reduccion estable y certificable.
- Cual es la proxima decision real? Si Matchbox sigue fallando por dependencias, congelar esa via como instrumental y empujar M22 como linea principal.
