# M22 Bridge Angeltveit low-bit/descent hacia rewriting/termination

Fecha: 2026-04-29
Rama: `codex-hijo/m22-angeltveit-rewriting-bridge`
Agente: CodexHijo

## Resumen ejecutivo

Veredicto honesto: el puente es viable como preprocesador/benchmark, no como prueba nueva de Collatz. La conexion util es estrecha:

```text
certificados low-bit de descenso modulo 2^k
    -> descargan subconjuntos finitos de ramas residuales
    -> dejan complementos mas pequenos para SRS/TRS guardados
    -> posible reduccion de S1/S2 como benchmarks, no como demostracion inflada
```

El primer prototipo confirma una senal cuantitativa: para `k = 16`, el certificado low-bit M21 descarga `7098/8192` clases de la rama S1 (`1 mod 8`, regla `aad -> ed`) y `7814/8192` clases de la rama S2 (`5 mod 8`, regla `bad -> d`). Eso sugiere que un benchmark guardado podria atacar solo `13.35%` de S1 y `4.61%` de S2. La advertencia fuerte: al subir a `k = 20` la fraccion cubierta baja para estas ramas, asi que no hay monotonia automatica.

## 1. Terreno recorrido

Rewriting/termination no es terreno virgen. Yolcu, Aaronson y Heule ya construyeron sistemas de reescritura mixtos binario-ternarios para Collatz, probaron equivalencia de terminacion con Collatz para el sistema central, implementaron un prover con interpretaciones natural/arctic/tropical, y publicaron pruebas automaticas de debilitamientos no triviales. Fuente primaria: <https://arxiv.org/abs/2105.14697>. Repo publico observado: <https://github.com/emreyolcu/rewriting-collatz>, HEAD `8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340`.

M19 ya materializo los objetos exactos:

```text
S1 = S sin aad -> ed   # paper: ff* -> 0*
S2 = S sin bad -> d    # paper: tf* -> *
```

El inventario local confirma que el repo oficial contiene 24 pruebas relativas reproducibles, pero no pruebas para S1/S2. La grilla M19 local sobre S1/S2 con `rewriting-collatz` dio `0 QED` para natural/arctic con `d <= 3`, `rw <= 5`.

Angeltveit tampoco es terreno virgen como verificacion computacional. Su paper 2026 propone un algoritmo de verificacion exhaustiva por bits bajos, sieves de descenso, preimagenes y merging. Fuente primaria: <https://arxiv.org/abs/2602.10466>. M21 ya implemento en este repo un probe independiente pequeno del certificado:

```text
T(n) = n/2       si n es par
T(n) = (3n+1)/2 si n es impar
T^k(r + a 2^k) = T^k(r) + 3^f a
```

Ese probe no reproduce GPU ni cota grande, pero audita que ciertos residuos modulo `2^k` fuerzan descenso para todos sus lifts positivos.

## 2. Que podria ser novedoso

Lo novedoso no seria "Collatz por rewriting" ni "Collatz por low bits". Eso ya existe. La novedad plausible esta en el acoplamiento:

1. Convertir certificados Angeltveit low-bit en invariantes externos de seguridad para descargar ramas residuales antes de llamar al prover de terminacion.
2. Generar benchmarks SRS/TRS guardados por residuos, donde el prover solo ve el complemento no certificado de una rama como S1/S2.
3. Medir si la dificultad SAT/matrix-interpretation baja al reemplazar una regla global abierta por una familia finita de guardas no descargadas.
4. Separar "reduccion real" de "inflar el sistema": si el guardado agrega mas estados/reglas que la eliminacion que produce, el puente no sirve.

La forma sana de reclamarlo seria:

```text
Un preprocesador certificado de descenso reduce una frontera rewriting publicada a benchmarks complementarios mas pequenos.
```

No se debe reclamar:

```text
Una prueba nueva de Collatz.
```

## 3. Prototipo M22 ejecutado

Archivo nuevo:

```text
scripts/m22_bridge_lowbit_rewriting.py
```

Tests:

```text
tests/test_m22_bridge_lowbit_rewriting.py
```

Comando ejecutado:

```powershell
python -m py_compile scripts\m22_bridge_lowbit_rewriting.py tests\test_m22_bridge_lowbit_rewriting.py
python -m unittest tests.test_m22_bridge_lowbit_rewriting
python scripts\m22_bridge_lowbit_rewriting.py --ks 8,10,12,14,16,18,20 --sample-k 16 --sample-size 16
```

Artefactos:

```text
reports/m22_bridge_lowbit_rewriting.csv
reports/m22_bridge_lowbit_rewriting.md
reports/m22_bridge_lowbit_rewriting_uncovered_samples.csv
```

Lectura del prototipo:

| k | Rama | Regla M19 | Cobertura low-bit | Complemento |
| ---: | --- | --- | ---: | ---: |
| 16 | S1 | `aad -> ed` / `ff* -> 0*` | `7098/8192 = 0.866455078125` | `1094` residuos |
| 16 | S2 | `bad -> d` / `tf* -> *` | `7814/8192 = 0.953857421875` | `378` residuos |
| 16 | S3 | `bd -> gd` / `t* -> 2*` | `12911/16384 = 0.788024902344` | `3473` residuos |
| 20 | S1 | `aad -> ed` / `ff* -> 0*` | `109293/131072 = 0.833839416504` | `21779` residuos |
| 20 | S2 | `bad -> d` / `tf* -> *` | `121670/131072 = 0.928268432617` | `9402` residuos |
| 20 | S3 | `bd -> gd` / `t* -> 2*` | `199140/262144 = 0.759658813477` | `63004` residuos |

Conclusion del prototipo: hay una reduccion cuantitativa fuerte, especialmente para S2, pero el mejor `k` probado para esta lectura es `16`, no `20`. Esto ya es informacion accionable para no disenar un experimento inflado.

## 4. Especificacion concreta del primer experimento reproducible

Experimento M22a: benchmark guardado S2-k16 con certificado externo.

Objetivo: comprobar si descargar por low-bit la rama `5 mod 8` reduce de manera medible el problema S2 sin romper la semantica de Yolcu-Aaronson-Heule.

Entradas fijas:

```text
rewriting-collatz HEAD: 8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340
S base: reports/m19_rewriting_challenges/m19_collatz_S_full.srs
S2 base: reports/m19_rewriting_challenges/m19_collatz_S2_without_tf_end_to_end.srs
k: 16
certificado externo: residues C_16 de scripts/m21_angeltveit_lowbit_probe.py
rama objetivo: residues r mod 2^16 con r mod 8 = 5
complemento a guardar: U_16 = {r mod 2^16 : r mod 8 = 5 and r notin C_16}
tamano esperado: |U_16| = 378
```

Procedimiento propuesto:

1. Congelar `C_16` y `U_16` con SHA-256 en `reports/m22_*`.
2. Construir un DFA minimo o trie determinista que reconoce los 16 bits bajos de `U_16`.
3. Insertar el DFA como fase de guardia antes de permitir la rama dinamica equivalente a `bad -> d`; las clases en `C_16` se descargan por el lema affine/descent de M21 y no entran al SRS guardado.
4. Generar dos archivos: `S2_guarded_k16_uncovered.srs` y `S2_guarded_k16_uncovered.tpdb`.
5. Correr la misma grilla M19: natural/arctic, `d = 1..3`, `rw = 2..5`, mismo timeout.
6. Comparar contra M19 S2 base por `QED`, CNF vars/clauses, tiempo, timeouts y estabilidad de resultados.

Criterio de exito minimo:

```text
El SRS guardado es menor o comparable en CNF que S2 base y obtiene QED/YES en algun punto donde S2 base no lo obtuvo.
```

Criterio de exito debil pero util:

```text
No obtiene QED, pero reduce CNF/tiempo de forma robusta y deja claro que el cuello esta en los 378 residuos no certificados.
```

Criterio de no-exito:

```text
El guardado explota el tamano del SRS/TRS, los CNF crecen, o el resultado no se puede interpretar como subproblema de S2.
```

## 5. Que lo destruiria

Destruiria la via cualquiera de estas condiciones:

1. Un fallo en la correspondencia semantica entre los residuos `mod 2^k` y las ramas del alfabeto mixto (`aad`, `bad`, `bd`). Si el guardado no expresa lo que creemos, todo resultado de termination seria irrelevante.
2. Un solo falso positivo en el certificado M21: una clase descargada por low-bit que no desciende para algun lift positivo.
3. Que el DFA/trie guardado infle el SRS tanto que los CNF sean mayores o mas dificiles que S1/S2 base.
4. Que el benchmark guardado pruebe solo una propiedad artificial sin implicar nada sobre el complemento operacional de S1/S2.
5. Que al comparar con el repo oficial se descubra que la misma familia de guardas ya fue probada bajo otro nombre.
6. Que la cobertura siga siendo no monotona y fragil al cambiar `k`, sin una razon estructural para elegir una ventana estable.

## Recomendacion

Seguir una iteracion mas, pero solo con M22a/S2-k16. S2 tiene el mejor ratio: `95.39%` de la rama queda descargada y solo `378` residuos quedan como complemento. No recomiendo generar todavia una familia grande de SRS para S1/S2/S3 y varios `k`; eso seria exactamente la prueba inflada que queremos evitar.

Si M22a no reduce CNF ni produce una lectura semantica clara, cerrar el puente como "diagnostico util pero no ruta fuerte".
