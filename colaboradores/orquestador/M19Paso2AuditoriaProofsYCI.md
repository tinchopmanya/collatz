# M19 paso 2 - auditoria de proofs y puerta CI

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: avance reproducible preparado

## Preguntas antes

- Estamos en terreno virgen?
  - No. La linea rewriting/SAT ya esta publicada por Yolcu-Aaronson-Heule.
- Podemos descubrir algo con esto?
  - No por reproducir el baseline. Si hay aporte, vendra despues: auditoria reproducible, compatibilidad moderna, certificacion o extension pequena no cubierta por los logs.
- Ya alguien estuvo buscando esto?
  - Si. El repo oficial trae scripts, sistemas `.srs` y logs de pruebas.
- Que tan lejos estamos de algo publicable?
  - Lejos de una contribucion matematica. Mas cerca de una nota tecnica reproducible si logramos CI estable, fixes pequenos y comparacion completa contra logs.

## Auditoria del repo externo

Repo:

- URL: https://github.com/emreyolcu/rewriting-collatz
- Commit auditado: `8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340`

Inventario:

- `proofs.sh` declara 24 corridas.
- `proofs/` contiene 24 logs.
- No hay logs faltantes ni extras respecto de `proofs.sh`.
- Los 24 logs contienen `SAT` y `QED`.

Rangos de CNF observados en logs:

- minimo: `collatz-T-02.log` y `collatz-T-05.log`, 77 variables y 267 clausulas;
- prueba base `zantema.log`: 1446 variables y 8537 clausulas;
- pruebas grandes: `farkas.log`, 61145 variables y 401782 clausulas; `collatz-T-3mod8.log`, 21004 variables y 220377 clausulas.

Conclusion:

```text
La evidencia incluida en el repo externo es consistente como inventario, pero todavia no es reproduccion local desde cero.
```

## Intento local sin solver nativo

Se intento crear un wrapper temporal `cadical.bat` + `cadical.py` usando `python-sat` dentro del clon temporal.

Hallazgos:

- `python-sat` se instalo correctamente en el venv temporal;
- `zantema_tmp.cnf` pudo resolverse manualmente con el wrapper PySAT;
- el ejemplo `rules/z086.srs` no termino en 120 segundos con PySAT;
- el prover externo falla en Windows/Python 3.12 por detalles de portabilidad antes de poder usar bien el wrapper.

Problemas concretos detectados:

- `random.randint(0, 1e9)` falla en Python 3.12 porque `1e9` es `float`;
- `subprocess.Popen('./cadical')` no resuelve `cadical.bat` en Windows;
- `shlex.split(f'{cat} {self.cnffile}')` destruye backslashes de paths Windows.

Conclusion:

```text
PySAT puede servir para experimentos pequenos, pero no reemplaza a CaDiCaL para reproducir seriamente el paper.
```

## Accion versionada

Se agrego un workflow manual:

```text
.github/workflows/m19-rewriting-reproduce.yml
```

Objetivo:

- correr en Ubuntu;
- clonar `rewriting-collatz` en el commit auditado;
- instalar Python/NumPy;
- construir CaDiCaL con commit pinneado `7b99c07f0bcab5824a5a3ce62c7066554017f641`;
- reproducir `relative/zantema.srs`;
- verificar que el log contiene `QED`;
- subir el log como artifact.

Este workflow no corre automaticamente en cada push. Solo corre con `workflow_dispatch`.

## Preguntas despues

- Avanzamos?
  - Si, pero como infraestructura de reproduccion. No hay matematica nueva.
- Es terreno virgen?
  - No. Seguimos en una linea publicada.
- La posibilidad cientifica fuerte subio?
  - Subio un poco como proyecto serio, porque ahora hay una puerta para reproducir estado del arte. No subio como probabilidad de probar Collatz.
- Que destruye esta ruta?
  - Que el workflow falle por incompatibilidades del repo externo o que solo reproduzcamos resultados existentes sin extension ni auditoria adicional.
- Que seria el siguiente avance real?
  - Ejecutar el workflow, guardar el log reproducido, y despues comparar automaticamente el log generado contra `proofs/zantema.log`.

## Decision

Continuar M19 solo si la reproduccion CI funciona.

No avanzar a extensiones SAT hasta tener:

- una prueba base regenerada desde cero;
- log versionado o artifact;
- comparacion contra el log oficial;
- lista de parametros ya cubiertos por el paper.
