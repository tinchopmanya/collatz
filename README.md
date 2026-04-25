# Collatz

Repositorio de investigacion y experimentacion computacional sobre la conjetura de Collatz.

## Estructura

- [Investigacion.md](Investigacion.md): indice central y log maestro.
- [InvestigacionMapa.md](InvestigacionMapa.md): mapa cronologico con fecha, hora y enlaces.
- [Conlusion.md](Conlusion.md): conclusion dinamica vigente.
- `InvestigacionSobre*.md`: investigaciones largas por ola.
- `ResumenInvestigacionSobre*.md`: resumen fuerte de cada investigacion.
- [RoadmapCollatz.md](RoadmapCollatz.md): plan de trabajo para convertir la investigacion en un laboratorio computacional.
- [MILESTONES.md](MILESTONES.md): milestones cerrables para avanzar por etapas.
- [AUTONOMIA.md](AUTONOMIA.md): reglas de trabajo autonomo y decisiones que requieren confirmacion.
- [AuditoriaFuentesCollatz.md](AuditoriaFuentesCollatz.md): primera auditoria de claims y fuentes.
- [EstadoActualidadYOriginalidadCollatz.md](EstadoActualidadYOriginalidadCollatz.md): verificacion de actualidad y originalidad del patron `-1 mod 2^k`.

## Flujo recomendado

1. Abrir una nueva ola con `scripts/nueva-ola.ps1`.
2. Completar el archivo largo de investigacion.
3. Completar el resumen fuerte.
4. Actualizar o reescribir [Conlusion.md](Conlusion.md).
5. Hacer commit por ola cerrada.

## Laboratorio computacional

Ejecutar tests:

```powershell
python -m unittest discover -s tests
```

Generar records para un rango:

```powershell
python experiments\generate_records.py --limit 100000 --out reports\records_limit_100000.csv
```

Analizar residuos modulo `2^k`:

```powershell
python experiments\analyze_residues.py --limit 1000000 --power 9 --out reports\residue_mod_512_limit_1000000.csv
```

Primer patron candidato:

- [records_limit_1000000.md](reports/records_limit_1000000.md)
- [residue_mod_512_limit_1000000.md](reports/residue_mod_512_limit_1000000.md)
- [parity_prefix_mod_512_limit_1000000.md](reports/parity_prefix_mod_512_limit_1000000.md)
- [alternating_prefix_mod_512_limit_1000000.md](reports/alternating_prefix_mod_512_limit_1000000.md)

## Crear una nueva ola

```powershell
.\scripts\nueva-ola.ps1 -Tema "Collatz ciclos no triviales" -Estado "Ola abierta"
```

El script crea los dos archivos base, registra la entrada en el indice y el mapa, y deja [Conlusion.md](Conlusion.md) lista para actualizar.

## Variables locales

Copiar el formato de [.env.example](.env.example) en `.env` para configuracion local. El archivo `.env` queda ignorado por git.
