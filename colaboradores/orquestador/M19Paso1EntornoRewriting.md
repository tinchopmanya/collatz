# M19 paso 1 - entorno para mixed-base rewriting

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: bloqueo tecnico identificado

## Objetivo

Reproducir una prueba base del repo externo `rewriting-collatz` sin tocar el repo principal.

Fuente:

- Paper: https://www.cs.cmu.edu/~mheule/publications/WST21.pdf
- Codigo: https://github.com/emreyolcu/rewriting-collatz

## Acciones realizadas

1. Se clono el repo externo en una carpeta temporal:

```powershell
$env:TEMP\rewriting-collatz
```

2. Se inspecciono el README y los scripts `proofs.sh`, `prover/main.py`, `prover/sat.py`.

3. Se intento ejecutar una prueba base:

```powershell
python $env:TEMP\rewriting-collatz\prover\main.py `
  $env:TEMP\rewriting-collatz\relative\zantema.srs `
  -i natural -d 2 -rw 4 --printascii
```

Primer bloqueo:

```text
ModuleNotFoundError: No module named 'numpy'
```

4. Se creo un entorno virtual temporal fuera del repo principal:

```powershell
$env:TEMP\rewriting-collatz\.venv
```

5. Se instalo `numpy` en ese entorno temporal:

```text
numpy 2.4.4
```

6. Se intento instalar CaDiCaL con el script externo:

```powershell
C:\msys64\usr\bin\bash.exe -lc "cd /c/Users/tinch/AppData/Local/Temp/rewriting-collatz && ./install-cadical.sh"
```

Bloqueos:

```text
git: orden no encontrada
./configure: No such file or directory
ln: fallo al crear el enlace simbolico .../cadical
```

## Estado local de herramientas

Disponible:

- `bash`: `C:\msys64\usr\bin\bash.exe`
- `make`: `C:\msys64\usr\bin\make.exe`
- `git` Windows: `C:\Program Files\Git\cmd\git.exe`
- Python venv temporal con `numpy`

No disponible:

- `lean`
- `lake`
- `cadical`
- `kissat`
- `minisat`
- `gcc`
- `g++`

## Diagnostico

La linea M19 sigue siendo la mejor candidata de alto ceiling, pero esta bloqueada por entorno, no por matematica.

El prover externo requiere:

- Python + NumPy;
- un solver SAT ejecutable como `./cadical`, `./kissat` o `./minisat`;
- comandos Unix como `cat` o `shuf`;
- toolchain C/C++ si se construye CaDiCaL localmente.

En Windows local, el camino mas limpio no es parchear a ciegas el repo externo, sino usar uno de estos entornos:

1. WSL/Linux;
2. GitHub Actions Linux;
3. MSYS2 completo con `git`, `gcc`, `g++` y CaDiCaL;
4. adaptar el prover a un backend SAT Python, si se decide hacer trabajo propio.

## Decision tecnica

No avanzar a busqueda SAT ni claims M19 hasta reproducir una prueba base.

No versionar:

- clon externo;
- venv temporal;
- binarios de solver;
- logs generados por herramientas externas.

## Proximo paso recomendado

Crear una rama dedicada:

```text
claude-socio/m19-rewriting-setup
```

Y elegir una de dos rutas:

1. **Ruta CI/Linux:** agregar un workflow o script documentado que clone `rewriting-collatz`, instale dependencias y reproduzca `relative/zantema.srs`.
2. **Ruta local MSYS2:** instalar toolchain MSYS2 faltante y construir CaDiCaL localmente.

Recomendacion del orquestador:

```text
Ruta CI/Linux primero.
```

Razon: es reproducible, no contamina la maquina local y evita depender de configuracion Windows.

## Preguntas despues

- Avanzamos?
  - Si. Identificamos una direccion con ceiling mas alto y el bloqueo exacto de entorno.
- Es terreno virgen?
  - No aun. Primero hay que reproducir el estado del arte.
- Posibilidad cientifica fuerte?
  - Ceiling alto relativo: si. Probabilidad de breakthrough: baja. Probabilidad de aporte reproducible serio: media si el entorno se estabiliza.
- Que destruye M19?
  - No poder reproducir pruebas base, o no encontrar extension pequena despues de reproducir.
- Que toca?
  - Preparar reproduccion Linux/CI de una prueba base.
