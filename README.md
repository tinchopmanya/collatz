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
- [FormalizacionPrefijoAlternante.md](FormalizacionPrefijoAlternante.md): lemma local sobre la longitud exacta del prefijo alternante.
- [InvestigacionSobreCollatzSextaOla.md](InvestigacionSobreCollatzSextaOla.md): mapa de salida del bloque alternante y siguiente impar.
- [InvestigacionSobreCollatzSeptimaOla.md](InvestigacionSobreCollatzSeptimaOla.md): cadenas odd-to-odd, primer descenso comprimido y reseteo de cola.
- [InvestigacionSobreCollatzOctavaOla.md](InvestigacionSobreCollatzOctavaOla.md): modelo geometrico independiente y comparacion real/modelo.
- [InvestigacionSobreCollatzNovenaOla.md](InvestigacionSobreCollatzNovenaOla.md): anti-persistencia entre bloques y condicionamientos por salida.
- [InvestigacionSobreCollatzDecimaOla.md](InvestigacionSobreCollatzDecimaOla.md): salidas con alta valuacion 2-adica y candidato `exit_v2 = 5`.
- [CriterioDeRelevancia.md](CriterioDeRelevancia.md): preguntas obligatorias antes y despues de cada iteracion.

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
- [exit_map_limit_1000000.md](reports/exit_map_limit_1000000.md)
- [odd_chain_limit_1000000.md](reports/odd_chain_limit_1000000.md)
- [geometric_model_limit_1000000.md](reports/geometric_model_limit_1000000.md)
- [antipersistence_limit_1000000.md](reports/antipersistence_limit_1000000.md)
- [high_exit_v2_limit_5000000.md](reports/high_exit_v2_limit_5000000.md)
- [exit_v2_selection_limit_5000000.md](reports/exit_v2_selection_limit_5000000.md)
- [survival_bias_limit_5000000.md](reports/survival_bias_limit_5000000.md)
- [m14_residual_robustness.md](reports/m14_residual_robustness.md)

Analizar la salida del bloque alternante:

```powershell
python experiments\analyze_exit_map.py --limit 1000000 --out-dir reports --prefix exit_map_limit_1000000
```

Analizar cadenas odd-to-odd:

```powershell
python experiments\analyze_odd_chain.py --limit 1000000 --max-blocks 256 --out-dir reports --prefix odd_chain_limit_1000000
```

Comparar contra modelo geometrico independiente:

```powershell
python experiments\trace_odd_records.py --max-blocks 256 --out-dir reports --prefix odd_record_traces
python experiments\compare_geometric_model.py --limit 1000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix geometric_model_limit_1000000
```

Analizar anti-persistencia entre bloques:

```powershell
python experiments\analyze_antipersistence.py --limit 1000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix antipersistence_limit_1000000
```

Analizar salidas con `exit_v2` alto:

```powershell
python experiments\analyze_high_exit_v2.py --limit 5000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix high_exit_v2_limit_5000000
```

Comparar transiciones locales contra cadenas sobrevivientes:

```powershell
python experiments\analyze_exit_v2_selection.py --limit 5000000 --max-blocks 256 --targets 1,2,3,4,5,6,7,8 --out-dir reports --prefix exit_v2_selection_limit_5000000
```

Analizar sesgo de supervivencia orbital:

```powershell
python experiments\analyze_survival_bias.py --limit 5000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix survival_bias_limit_5000000
```

Probar robustez del residuo M14:

```powershell
python experiments\test_m14_residual_robustness.py --limit 5000000 --max-blocks 256 --permutations 10000 --seed 20260425 --extra-tests 546 --out-dir reports --prefix m14_residual_robustness
python experiments\test_m14_residual_robustness.py --start 5000001 --limit 10000000 --max-blocks 256 --permutations 10000 --seed 20260425 --extra-tests 546 --out-dir reports --prefix m14_residual_robustness_holdout_5000001_10000000
```

## Crear una nueva ola

```powershell
.\scripts\nueva-ola.ps1 -Tema "Collatz ciclos no triviales" -Estado "Ola abierta"
```

El script crea los dos archivos base, registra la entrada en el indice y el mapa, y deja [Conlusion.md](Conlusion.md) lista para actualizar.

## Variables locales

Copiar el formato de [.env.example](.env.example) en `.env` para configuracion local. El archivo `.env` queda ignorado por git.
