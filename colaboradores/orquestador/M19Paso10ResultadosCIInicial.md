# M19 paso 10 - resultados CI iniciales

Fecha: 2026-04-29
Responsable: Codex orquestador
Estado: primera ronda CI auditada; fixes pendientes aplicados

## Preguntas antes

- Estamos avanzando?
  - Si. Pasamos de investigacion web y diseno de rutas a ejecucion real en GitHub Actions.
- Estamos en terreno virgen?
  - No en la idea general. La zona concreta sigue siendo S1/S2 + herramientas modernas + auditoria reproducible.
- Podemos descubrir algo con esto?
  - Si, pero solo si una herramienta produce `YES` top-level y luego certificado/auditoria. Los resultados actuales no son avance matematico.
- Ya alguien estuvo buscando esto?
  - Si. Yolcu-Aaronson-Heule, AProVE/TermComp, Matchbox y comunidad de terminacion. Nuestra contribucion por ahora es integracion/reproduccion ordenada.
- Que tan lejos estamos?
  - Mas cerca de una plataforma seria; todavia lejos de una prueba.

## Runs ejecutados

| Run | Workflow | Resultado operacional | Lectura |
| ---: | --- | --- | --- |
| 25104952224 | M19 rewriting reproduction | failure | falso fallo por exit code `19` usado como `QED` por el prover |
| 25104952228 | M19 rewriting challenge search | success | 48/48 `ERROR` por incompatibilidad Python `random.randint(0, 1e9)` |
| 25104952325 | M19 AProVE challenge search | success | S1/S2 `KILLED`; sin `YES` top-level |
| 25105347516 | M19 AProVE environment probe | success | confirma `ENV_YICES_E_INCOMPATIBLE` con Yices 2.6.4 |
| 25105375622 | M19 Matchbox challenge search | success | runner funciono, pero `matchbox2015` no quedo disponible |
| 25105347569 | M19 rewriting challenge search | success | grilla corregida: 0 `QED`, 46 `UNSAT`, 2 logs imprimen `UNSAT` antes de colgar |
| 25105647983 | M19 rewriting challenge search focalizada | success | las celdas dudosas de S2 tambien dan `UNSAT` |
| 25105756807 | M19 rewriting reproduction | success | reproduccion Zantema validada en CI; `SAT=True`, `QED=True` |
| 25105756825 | M19 AProVE environment probe | success | wrapper `yices2-strip-e` elimina bloqueo `-e`, pero S1/S2 terminan `WST_KILLED` |
| 25105756640 | M19 rewriting challenge search focalizada | success | confirma de nuevo `UNSAT` en las celdas S2 dudosas |

## Hallazgos

### Rewriting-collatz

El prover oficial usa codigos de salida no convencionales:

```text
19 = QED
11 = PARTIAL
29 = UNSAT
```

Por eso el workflow de reproduccion trataba una prueba exitosa como failure. Se corrigio para aceptar `code=19` si el log contiene `QED` y `Relatively top-terminating rules`.

La corrida `25105756807` valida la tuberia base:

```text
relative/zantema.srs
SAT=True
QED=True
CNF: 1446 variables, 8537 clauses
```

### AProVE

El probe separo claramente ambiente de matematica:

```text
yices --version -> Yices 2.6.4
yices -e -> invalid option
S1/S2 -> ENV_YICES_E_INCOMPATIBLE
```

Esto confirma que la corrida AProVE con Yices 2 no debe usarse como evidencia matematica. Para hacer una prueba justa hace falta Yices 1.0.40 o un wrapper compatible con `yices -e`.

El experimento `25105756825` probo un wrapper minimo `yices2-strip-e`:

```text
yices -e probe -> supported
S1 -> WST_KILLED
S2 -> WST_KILLED
```

Lectura prudente: el wrapper permite que AProVE avance, pero no convierte Yices 2 en entorno certificado. Sirve como diagnostico barato; para evidencia fuerte sigue haciendo falta Yices 1 compatible o certificado independiente.

### Matchbox

El workflow y runner funcionaron, pero no hubo binario:

```text
ERROR: cannot execute Matchbox command: matchbox2015
```

El build experimental no produjo `matchbox2015` por conflicto de dependencias Cabal/Haskell contra el repo historico. La via Matchbox no queda descartada; queda bloqueada por packaging. Proximo paso realista: binario reproducible, container, o pin de toolchain Haskell antiguo.

### Grilla S1/S2 corregida

La grilla corregida ya no falla por Python. Resultado:

```text
48 corridas
0 QED
46 UNSAT
2 timeouts externos
```

Los dos timeouts corresponden a:

- S2 natural `d=1`, `rw=3`;
- S2 arctic `d=2`, `rw=3`.

Al inspeccionar logs, ambos habian impreso `UNSAT` antes de que el proceso externo venciera. Esto sugiere problema de salida/cleanup del prover, no una celda prometedora. Se ajusto el clasificador para marcar estos casos como `UNSAT_AFTER_TIMEOUT` en futuras corridas.

La corrida focalizada `25105647983` con mayor presupuesto cerro esas celdas:

```text
S2 natural d=1 rw=3 -> UNSAT
S2 arctic  d=2 rw=3 -> UNSAT
```

Resultado actualizado de la grilla chica:

```text
0 QED
0 candidatos
S1/S2 no ceden con natural/arctic d<=3, rw<=5 bajo este prover
```

### Auditor de artefactos

Clasificacion actual:

```text
uncertified_logs_only
```

No hay CPF, no hay CeTA, no hay `YES` top-level certificado.

## Preguntas despues

- Avanzamos?
  - Si. Identificamos tres bloqueos concretos: exit code `19`, Yices1 vs Yices2, Matchbox packaging.
- Hay resultado matematico?
  - No.
- Estamos mas cerca de algo publicable?
  - Si como infraestructura reproducible; no como teorema.
- Que destruye esta via?
  - Que con entorno correcto Yices1/Matchbox/rewriting-collatz sigan sin producir `YES` o CPF en presupuestos razonables.
- Que toca?
  - Relanzar reproduccion Zantema corregida; esperar la grilla S1/S2 corregida; decidir si perseguir Yices1 o container Matchbox.
