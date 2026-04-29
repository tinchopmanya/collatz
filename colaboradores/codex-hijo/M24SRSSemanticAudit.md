# M24 SRS semantic audit

Fecha: 2026-04-29
Agente: CodexHijo-M24-SRS-SemanticAudit
Worktree: `C:\dev\vert\collatz-m24-srs-semantic-audit`
Rama: `codex-hijo/m24-srs-semantic-audit`

## Veredicto

La equivalencia local queda **probada para la rama operacional dinamica** de `S`: en la semantica funcional del paper, la regla paper `tf* -> *` representa exactamente el caso `n = 8x + 5`, es decir `n % 8 == 5`. Con el mapa ASCII local, `tf* -> *` es `bad -> d`.

El matiz importante es que M22-C2 no contenia esta derivacion: la tenia como etiqueta y por eso marco `gap_unproven`. M24 cierra ese gap estrecho de etiqueta/rama, pero no implementa C3 ni prueba todavia que un SRS guardado concreto por residuos `mod 2^16` conserve exactamente el subproblema operacional.

## Fuentes y reglas leidas

Fuente primaria paper YA-Heule: el PDF `An Automated Approach to the Collatz Conjecture` (`https://www.cs.cmu.edu/~mheule/publications/collatz.pdf`, version JAR en `https://doi.org/10.1007/s10817-022-09658-8`) define la funcion acelerada `S` sobre impares con tres casos:

```text
n == 1 mod 8 -> (3n + 1) / 4
n == 5 mod 8 -> (n - 1) / 4
n == 3 mod 4 -> (3n + 1) / 2
```

El mismo paper traduce esos casos a:

```text
S = {ff* -> 0*, tf* -> *, t* -> 2*} union X
S2 = S \ {tf* -> *}
```

Repo oficial `emreyolcu/rewriting-collatz` (`https://github.com/emreyolcu/rewriting-collatz`), consultado temporalmente dentro del worktree, HEAD `8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340`. En `rules/collatz-S.srs` aparecen exactamente:

```text
aad -> ed
bad -> d
bd -> gd
ae -> ea
af -> eb
ag -> fa
be -> fb
bf -> ga
bg -> gb
ce -> cb
cf -> caa
cg -> cab
```

Artefactos locales M19:

```text
reports/m19_rewriting_challenges/m19_collatz_S_full.srs
reports/m19_rewriting_challenges/m19_collatz_S2_without_tf_end_to_end.srs
reports/m19_rewriting_challenges/README.md
scripts/m19_generate_rewriting_challenges.py
```

El `README` y el script M19 etiquetan:

```text
aad -> ed  = ff* -> 0* = dynamic S, residue 1 mod 8
bad -> d   = tf* -> *  = dynamic S, residue 5 mod 8
bd -> gd   = t* -> 2*  = dynamic S, residue 3 mod 4
```

El archivo S2 local elimina solo `bad -> d`; `m19_collatz_S2_without_tf_end_to_end.srs` conserva las otras 11 reglas.

Artefactos locales M22/M23 relevantes:

```text
colaboradores/codex-hijo/M22C2SemanticBridge.md
reports/m22_c2_semantic_bridge_summary.csv
colaboradores/codex-investigador/M23FronteraWeb2026.md
colaboradores/orquestador/DecisionM22TrasC1C2M23.md
```

M22-C2 reporta `PASS` para la guarda finita S2-k16, con `8192` residuos `r mod 8 = 5`, `7814` certificados, `378` no cubiertos, `0` fuera de S2 aceptados y estado `semantic_translation_status = gap_unproven`. M23 y la decision del orquestador bloquean C3 hasta cerrar esta auditoria.

## Derivacion local

La semantica funcional del paper para los simbolos relevantes es:

```text
f(x) = 2x
t(x) = 2x + 1
*(x) = 2x + 1
```

La palabra se lee por composicion hacia el marcador final. Por tanto:

```text
ff* = *(f(f(x))) = 8x + 1
tf* = *(f(t(x))) = 8x + 5
t*  = *(t(x))    = 4x + 3
```

Y las partes derechas coinciden con los tres casos de `S`:

```text
ff* -> 0*:  0*(x) = 6x + 1 = (3(8x + 1) + 1) / 4
tf* -> *:   *(x)  = 2x + 1 = ((8x + 5) - 1) / 4
t* -> 2*:   2*(x) = 6x + 5 = (3(4x + 3) + 1) / 2
```

Con el mapa ASCII local `a=f`, `b=t`, `d=*`, `e=0`, `f=1`, `g=2`, la regla `bad -> d` es exactamente `tf* -> *`. Asi, en una palabra normalizada donde se aplica la regla dinamica de `S`, activar `bad -> d` equivale a estar en el caso operacional `residue % 8 == 5`.

## Estado de la equivalencia

| Reclamo | Estado M24 | Alcance |
| --- | --- | --- |
| `bad -> d` es la regla ASCII de `tf* -> *` | `probado` | Por mapa M19 y `rules/collatz-S.srs` oficial |
| `tf*` selecciona `n % 8 == 5` | `probado` | Por composicion `*(f(t(x))) = 8x + 5` |
| M22 ya contenia una derivacion local | `refutado` | M22-C2 marcaba `tag_only_not_operational_equivalence` y `gap_unproven` |
| La guarda S2-k16 finita acepta solo complemento dentro de `r % 8 == 5` | `probado computacionalmente por M22-C2` | Counts/hashes y `0` violaciones locales |
| C3 guarded SRS exacto | `no decidido / no implementado` | Falta especificacion y checker de implicacion del SRS guardado |

## Minimo que falta para C3

Antes de construir o reclamar un C3 guarded SRS hace falta:

1. Especificar donde se inserta la guarda respecto de las reglas auxiliares `X` y la regla dinamica `bad -> d`.
2. Fijar orientacion de bits y lectura de residuos `mod 2^16` en el alfabeto mixto, incluyendo si la guarda lee LSB-first o MSB-first.
3. Probar con un checker que toda aplicacion permitida por la guarda corresponde a una palabra dinamica `tf*` con residuo congelado no certificado, y que toda clase certificada queda descargada fuera del SRS guardado.
4. Probar que el SRS guardado implica un subproblema de S2, no una propiedad artificial producida por la codificacion de la guarda.
5. Solo despues, generar `S2_guarded_k16_uncovered.srs`/TPDB y correr la comparacion preregistrada contra S2 base. Si aparece `YES`, exigir CPF/CeTA antes de cualquier reclamo fuerte.

## Script de auditoria

Se agrego `scripts/m24_srs_semantic_audit.py` para dejar ejecutable la derivacion de residuos y verificar que el S2 local elimina solo `bad -> d`. Su salida principal es:

```text
ff* -> 0* | aad -> ed | n = 8*x + 1 | (3n+1)/4 if n == 1 mod 8
tf* -> * | bad -> d | n = 8*x + 5 | (n-1)/4 if n == 5 mod 8
t* -> 2* | bd -> gd | n = 4*x + 3 | (3n+1)/2 if n == 3 mod 4
S2 removed rules: ['bad -> d']
S2 removes only bad -> d: True
```

Tests agregados:

```text
python -m unittest tests.test_m24_srs_semantic_audit
```

Resultado: `Ran 5 tests ... OK`.
