# M20 Knight Route

Fecha: 2026-04-29
Agente: CodexHijo-KnightM20
Rama: main
Commit: no commit
Milestone: M20
Tarea: evaluar si Kevin Knight 2026 abre una sublinea util para terminacion/rewrite

## Comando reproducible

```powershell
python scripts\m20_knight_rule_notes.py
python -m py_compile scripts\m20_knight_rule_notes.py
git diff --check -- colaboradores/codex-hijo/M20KnightRoute.md scripts/m20_knight_rule_notes.py
```

## Fuentes primarias y estado de busqueda

Fuente primaria leida: Kevin Knight, "A Small Collatz Rule without the Plus One", Complex Systems 35(1), 2026, DOI `10.25088/ComplexSystems.35.1.1`.

URL primaria: <https://content.wolfram.com/sites/13/2026/04/35-1-1.pdf>

La regla K del paper codifica un termino de Collatz `m` como `2^m` y aplica solo multiplicaciones racionales sobre terminos de la forma `2^x 3^y 5^z`. La tabla impresa es:

| Rama | Residuo mod 30 | Multiplicador | Delta en exponentes `(2,3,5)` |
| --- | --- | --- | --- |
| A | `2, 8` | `375/2` | `(-1,+1,+3)` |
| B | `0` | `125/2` | `(-1,0,+3)` |
| C | `3, 9, 15, 21, 27` | `5/3` | `(0,-1,+1)` |
| D | `5, 10, 20, 25` | `2/5` | `(+1,0,-1)` |
| E | `4, 6, 12, 16, 18, 24` | `3/4` | `(-2,+1,0)` |

No encontre evidencia publica de una traduccion ya hecha de esta regla de Knight a TRS/SRS/AProVE/Matchbox. La busqueda por titulo exacto, multiplicadores exactos y GitHub devolvio esencialmente el PDF/issue de Complex Systems, no repositorios de reescritura. Esto no prueba inexistencia; solo deja la hipotesis "sin traduccion publica visible al 2026-04-29".

Terreno no virgen: Collatz via reescritura ya esta trabajado por Yolcu, Aaronson y Heule en "An Automated Approach to the Collatz Conjecture" (JAR 2023, DOI `10.1007/s10817-022-09658-8`), por Monks via Fractran en "3x + 1 Minus the +" (2002, DOI `10.46298/dmtcs.297`), y por otros modelos citados en Knight. Nuestro M19 ya materializo sistemas SRS de Yolcu-Aaronson-Heule y desafios S1/S2.

Terreno parcialmente virgen: la pieza nueva seria una traduccion especifica de la regla K/K' de Knight a una forma de terminacion que preserve su estructura de tres registros primos, no otra reformulacion general de Collatz.

## Resultado central

Respuesta corta: si vale abrir M20, pero con presupuesto corto y criterio de abandono fuerte. La regla de Knight parece mas amigable que S1/S2 para una formalizacion de contadores o TRS con estados, pero no claramente mas amigable para SRS pura.

La razon positiva es que K expone una maquina de 3 contadores con deltas lineales muy chicos:

```text
A: (x,y,z) -> (x-1, y+1, z+3)
B: (x,y,z) -> (x-1, y,   z+3)
C: (x,y,z) -> (x,   y-1, z+1)
D: (x,y,z) -> (x+1, y,   z-1)
E: (x,y,z) -> (x-2, y+1, z)
```

Esto es conceptualmente mas transparente que la reescritura mixta binario-ternaria de S1/S2: cada paso dice que registro primo sube o baja, y el paper ya separa fases para terminos pares e impares. Para herramientas de terminacion, la promesa real no es "probar Collatz", sino construir benchmarks de subdinamicas y buscar interpretaciones lineales/matriciales mas limpias que las de M19.

La razon negativa es igual de importante: la regla K de 30 condiciones no es una funcion entera total sobre todos los enteros de esos residuos. Knight mismo observa que K no es una verdadera generalized Collatz rule, porque la rama `3/4` no se puede reescribir como `(a n + b)/30`; propone una variante K' de 60 condiciones para arreglar eso. En terminos de rewrite, esto significa que una SRS ingenua sobre una palabra ordenada `2^x 3^y 5^z` necesita guardas de fase, pruebas de cero/ausencia o marcadores de estado. Sin esas guardas, reglas como "consumir 3 y producir 5" se dispararian tambien en estados donde K deberia elegir `3/4` o `125/2`.

## Traduccion posible a TRS/SRS

Opcion con mejor relacion valor/riesgo: TRS/VASS con estados finitos.

Representar una configuracion como `K(state, x, y, z)`, donde `x,y,z` son naturales unary/Peano o contadores abstractos, y los estados codifican la fase: `odd_start`, `odd_drain_2`, `drain_3`, `drain_5`, `even_drain_2`, etc. Esta ruta conserva la simplicidad de Knight y evita que una regla se aplique fuera de su fase alcanzable.

Opcion SRS pura: posible pero menos limpia.

Con alfabeto de tokens `2,3,5` y palabra canonica ordenada, las reglas locales tipo `2 -> 3555`, `3 -> 5`, `5 -> 2`, `22 -> 3` no son correctas sin contexto negativo o marcadores. Se puede introducir control de fase y separadores, pero entonces parte de la complejidad vuelve a parecerse a S1/S2.

Opcion K' de 60 condiciones: util como fallback tecnico.

K' convierte la regla en una generalized Collatz rule con denominador 60. Puede ser mejor para generar automaticamente casos modulo-finito, pero probablemente pierde la elegancia de los tres contadores y duplica el tamano de la tabla. La usaria solo si AProVE/Matchbox exige una regla total modulo fija.

## Posibilidad fuerte

Probabilidad de descubrir algo relevante para la busqueda: media-baja para una prueba global, media para una herramienta de descarte/benchmark.

Senal fuerte para seguir:

- Encontrar una TRS con estados de menos de, digamos, 10 fases y reglas lineales que simule K micro-paso a micro-paso.
- Que AProVE/Matchbox pruebe terminacion de restricciones analogas a S1/S2 con CNF o certificados mas chicos que M19.
- Que la formulacion de contadores revele un ranking local nuevo para una familia no cubierta por los subsistemas ya inventariados.
- Que las ecuaciones de ciclo de Knight (`p=1` y frecuencia fija de ramas) se traduzcan a invariantes automaticos utiles para filtrar ciclos candidatos.

Senal debil o negativa:

- La traduccion SRS necesita tantos marcadores/fases que deja de ser mas simple que S1/S2.
- Cada intento util macro-colapsa a `2^n -> 2^C(n)`, o sea vuelve a meter `3n+1` disfrazado.
- Los provers no prueban ni debilitamientos chicos donde M19 ya tiene pruebas o benchmarks manejables.
- La variante K' de 60 condiciones aumenta el espacio de busqueda sin producir certificados mas chicos.

## Verificacion

Archivo reproducible creado: `scripts/m20_knight_rule_notes.py`.

Resultados del smoke run:

```text
Verified K projection to Collatz C(n) for encoded terms 1..40.
Sample term 3:
- 2^3 reaches 2^10 using 14 K steps
- branch word: ABBCDDDDDDDDDD
```

Tambien paso `python -m py_compile scripts\m20_knight_rule_notes.py`.

## Que destruye este resultado

- Encontrar una traduccion publica previa Knight->TRS/SRS con los mismos objetivos y resultados.
- Confirmar que las guardas de fase necesarias son equivalentes en complejidad practica al sistema S de Yolcu-Aaronson-Heule.
- Ver que K' de 60 condiciones, al expandirse para herramientas, genera instancias mas grandes o menos tratables que M19.
- Detectar que la unica forma correcta de probar terminacion de subcasos usa directamente propiedades Collatz ya conocidas, no la estructura nueva de Knight.

## Que no se debe concluir

- No se debe concluir que Knight simplifica Collatz hasta hacerlo resoluble por terminacion automatica.
- No se debe concluir que la regla K sea una SRS lista para usar: necesita estados/guardas.
- No se debe concluir que el chequeo `1..40` prueba nada matematico; solo valida que la tabla fue transcrita de manera coherente para smoke testing.

## Siguiente paso recomendado

Abrir una micro-iteracion M20a solo si se acepta este objetivo minimo:

```text
Construir una TRS/VASS con estados que simule las cinco ramas A-E sobre
configuraciones alcanzables, generar 2 o 3 restricciones tipo "quitar una rama
dinamica" analogas a S1/S2, y comparar si AProVE/Matchbox obtiene pruebas mas
chicas o mas claras que M19.
```

Criterio de abandono de M20a: si en una iteracion no aparece una codificacion con menos complejidad conceptual que S1/S2, abandonar Knight como ruta de terminacion y conservarlo solo como reformulacion/ciclo-invariante interesante.
