# Conlusion dinamica

Ultima actualizacion: 2026-04-29
Tema: Collatz - M19/M22, rewriting certificado y puente low-bit/descent

## Estado actual

El arco estadistico M12-M18 queda cerrado como descarte disciplinado. No hay senal odd-to-odd con ceiling suficiente para seguir invirtiendo ahi.

El proyecto sigue abierto solo por una via de mayor posibilidad cientifica:

```text
M19/M22 - sistemas de reescritura, certificacion externa y puente low-bit/descent.
```

Esto no es una prueba de Collatz. La meta realista es producir una reduccion o benchmark certificable que conecte dos areas ya existentes: rewriting/termination y verificacion low-bit/descent.

## Respuesta corta a las preguntas guia

- Estamos avanzando? Si, porque estamos reemplazando correlaciones debiles por artefactos verificables, gates de certificacion y complementos residuales congelados.
- Estamos en terreno virgen? No para rewriting ni para low-bit por separado. Parcialmente si para la combinacion reproducible de ambos.
- Alguien ya estuvo aca? Si: Yolcu-Aaronson-Heule en rewriting; Barina y Angeltveit en verificacion computacional; TermComp/AProVE/Matchbox/CeTA en terminacion certificada. No encontramos aun una campana publica que use filtros low-bit como preprocesador de familias residuales S1/S2.
- Que tan lejos estamos? Lejos de demostrar Collatz; a distancia moderada de un resultado computacional publicable si M22 estabiliza y alguna subfamilia queda cerrada con certificado.
- Posibilidad cientifica fuerte alta? Media-alta para M22; media para Matchbox/AProVE si se obtiene un binario reproducible; baja para mas estadistica orbital.

## Mejor via vigente

La via principal pasa a ser M22:

```text
Usar certificados low-bit/descent para reducir familias de rewriting,
y luego intentar cerrar los residuos con herramientas de terminacion certificadas.
```

Resultado concreto actual: para S2 con `k=16`, el filtro low-bit descarga `7814/8192` clases y deja un complemento congelado de `378` residuos, con hash:

```text
bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210
```

Ese complemento es ahora el objeto cientifico principal. Si muestra estructura explotable, puede volverse benchmark. Si no la muestra, M22 se enfria limpiamente.

## Estado de Matchbox/AProVE

Matchbox/AProVE siguen siendo herramientas instrumentales, no la hipotesis central. Los intentos de build historico muestran fallos sucesivos de ecosistema:

- paquete Ubuntu de Boolector sin headers/libreria;
- parche Haskell `boolector`;
- parche `wl-pprint-extras`;
- fallo `satchmo`;
- conflicto `atto-lisp/base` con `use_source_deps=true`.

Decision provisoria: permitir como maximo uno o dos parches acotados mas si el run pendiente ofrece una frontera clara. Si la cadena continua, pivotar a binario/container/herramienta alternativa y no gastar la investigacion en arqueologia de dependencias.

## Que destruiria la linea actual

- Un falso positivo en el probe low-bit/descent.
- Un complemento residual que crece sin estructura al subir `k`.
- Herramientas de terminacion que no mejoran sobre subfamilias residuales frente a S2 completo.
- Certificados no reproducibles o `YES` sin CPF/CeTA.
- Que el supuesto puente low-bit/rewrite sea solo una reformulacion sin reduccion efectiva.

## Proxima decision

Esperar los resultados de los cinco hijos en worktrees separados y decidir:

- si M19 se mantiene solo como herramienta o se enfria;
- si M22 pasa a milestone principal;
- que experimento confirmatorio se corre primero sobre el complemento S2-k16.
