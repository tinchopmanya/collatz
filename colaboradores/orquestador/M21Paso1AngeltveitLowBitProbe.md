# M21 paso 1 - Angeltveit low-bit probe

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: prototipo independiente pequeno ejecutado

## Preguntas antes

- Estamos avanzando?
  - Si, abriendo una via 2026 seria en paralelo a M19.
- Estamos en terreno virgen?
  - No globalmente. Angeltveit ya propuso el algoritmo y publico codigo. El aporte posible del repo es auditoria independiente, no autoria del metodo.
- Podemos descubrir algo fuerte?
  - Fuerte como reproduccion/auditoria computacional, no como prueba teorica de Collatz. Una reproduccion robusta de cotas grandes o una deteccion de bug seria relevante.
- Ya alguien estuvo buscando esto?
  - Si: Angeltveit 2026, Barina y la linea de verificacion computacional de Collatz.
- Que tan lejos estamos?
  - Cerca de un prototipo verificable chico; lejos de competir con `2^71+`.

## Implementacion

Archivo: `scripts/m21_angeltveit_lowbit_probe.py`

Este script implementa una version pequena y limpia del certificado low-bit/descent:

```text
T(n) = n/2       si n es par
T(n) = (3n+1)/2 si n es impar
```

Para cada modulo `2^k`, calcula los primeros `k` pasos de `T` sobre cada residuo. Si el prefijo contrae y el residuo desciende, marca ese residuo como certificado. Luego valida cada `n < 2^N` contra una iteracion ingenua de `T` para detectar falsos positivos.

El script no copia codigo GPL del repositorio externo. Es una prueba independiente y deliberadamente chica.

## Comando

```powershell
python -m py_compile scripts\m21_angeltveit_lowbit_probe.py
python scripts\m21_angeltveit_lowbit_probe.py --max-power 20 --ks 8,10,12,14,16 --naive-steps 256 --out-dir reports --prefix m21_angeltveit_lowbit_probe
```

Artefactos:

- `reports/m21_angeltveit_lowbit_probe.csv`
- `reports/m21_angeltveit_lowbit_probe.md`

## Resultado

Resultado central:

```text
rows = 95
max_false_positives = 0
```

Muestras:

| N | k | cobertura low-bit | falsos positivos | cobertura preimagen mod 3 |
| ---: | ---: | ---: | ---: | ---: |
| 12 | 8 | 0.828083028083 | 0 | 0.333333333333 |
| 12 | 16 | 0.892796092796 | 0 | 0.333333333333 |
| 16 | 8 | 0.828122377356 | 0 | 0.333333333333 |
| 16 | 16 | 0.894911116197 | 0 | 0.333333333333 |
| 20 | 8 | 0.828124836087 | 0 | 0.333333333333 |
| 20 | 16 | 0.894912619507 | 0 | 0.333333333333 |

## Interpretacion

Esto no prueba Collatz y no reproduce todavia el algoritmo completo de Angeltveit. Pero si valida tres cosas utiles:

- La propiedad low-bit produce certificados de descenso sin falsos positivos en el rango chico probado.
- La cobertura crece con `k`; para `N=20, k=16` certifica aproximadamente 89.49% de los enteros positivos menores que `2^20`.
- M21a tiene sentido como linea de auditoria: se puede construir una escalera de reproducibilidad antes de tocar GPU o cotas grandes.

## Preguntas despues

- Estamos avanzando?
  - Si. M21a ya tiene primer script y primer artefacto reproducible.
- Estamos en algo virgen?
  - No como metodo; si como auditoria propia independiente dentro del repo.
- Podemos descubrir algo?
  - Si, pero el descubrimiento probable seria tecnico: bug, mejora de auditoria, comparacion clara con Angeltveit/Barina, o reproduccion independiente.
- Que tan lejos estamos?
  - Lejos de records; cerca de validar el pipeline chico. El siguiente salto razonable es implementar los filtros restantes y comparar contra `cases_tiny`.

## Proximo paso

1. Extender el probe con el filtro mod 9 exacto de Angeltveit, no solo la preimagen mod 3 segura.
2. Descargar o clonar el repo externo a `tmp/` y comparar hashes/estructura de `cases_tiny`.
3. Subir `N` solo despues de que el conjunto chico tenga cero discrepancias contra verificacion ingenua.
4. Mantener M21 separado de M19: M21 es verificacion computacional; M19 es terminacion/certificacion de SRS.

## Fuentes

- Angeltveit, "An improved algorithm for checking the Collatz conjecture for all n < 2^N", arXiv:2602.10466, 2026-02-11: https://arxiv.org/abs/2602.10466
- Codigo publico asociado: https://github.com/vigleik0/collatz
