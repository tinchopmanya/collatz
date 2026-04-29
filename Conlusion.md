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

## Estado M22-C1/C2

M22-C1 paso como rechecker independiente:

- `branch_residue_count = 8192`;
- `lowbit_certified_count = 7814`;
- `uncovered_count = 378`;
- hashes de certificados y complemento reproducidos;
- `false_positives = 0`;
- `affine_failures = 0`.

M22-C2 paso como guarda computacional finita:

- `65536` residuos evaluados;
- `378` residuos del complemento aceptados;
- `0` residuos fuera de S2 aceptados;
- `0` residuos certificados reenviados al guardado.

M24 cerro la brecha semantica estrecha para la rama dinamica:

```text
tf* = *(f(t(x))) = 8x + 5
bad -> d = tf* -> *
```

Por lo tanto, `bad -> d` corresponde al caso operacional `n % 8 == 5` dentro de `S`. Esto desbloquea un C3 minimo, pero no prueba todavia que un SRS guardado por residuos `mod 2^16` este correctamente construido.

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

Ejecutar C3 minimo:

- usar microguarda `r mod 2^13 = 8189`;
- generar artefacto/checker antes de correr provers;
- comparar contra S2 base solo con parametros preregistrados;
- exigir CPF/CeTA si aparece un `YES`.
