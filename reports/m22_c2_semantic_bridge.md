# M22-C2 semantic bridge validator

Fecha: 2026-04-29
Agente: CodexHijo-M22-C2-SemanticBridge
Rama: `codex-hijo/m22-c2-semantic-bridge`

## Veredicto

- Guardia low-bit S2-k16: `PASS`.
- Estado del puente semantico SRS mixto: `gap_unproven`.
- No se reclama equivalencia operacional entre el SRS mixto y `r mod 8 = 5`.

La enumeracion exhaustiva confirma que la guarda congelada acepta exactamente
los `378` residuos no certificados dentro de la rama etiquetada como S2 por
`r mod 8 = 5`. Tambien confirma que no acepta residuos fuera de S2 y que no
reenvia residuos certificados al guardado. Esto valida la aritmetica de la
guarda, pero no cierra la traduccion semantica del alfabeto mixto.

## Checks computacionales

| Check | Valor | Esperado | Estado |
| --- | ---: | ---: | --- |
| Residuos evaluados | `65536` | `65536` | `PASS` |
| Residuos S2 por `r mod 8 = 5` | `8192` | `8192` | `PASS` |
| Complemento aceptado por la guarda | `378` | `378` | `PASS` |
| Residuos fuera de S2 aceptados | `0` | `0` | `PASS` |
| Residuos certificados enviados al guardado | `0` | `0` | `PASS` |
| Huecos en la particion S2 certificado/complemento | `0` | `0` | `PASS` |

## Hashes

| Conjunto | SHA-256 actual | SHA-256 esperado | Match |
| --- | --- | --- | --- |
| Complemento S2-k16 | `bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210` | `bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210` | `True` |
| Certificados S2-k16 | `0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa` | `0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa` | `True` |

## Tabla local de traduccion disponible

| Regla ASCII | Regla paper | Etiqueta local | Estado C2 |
| --- | --- | --- | --- |
| `bad -> d` | `tf* -> *` | `residue % 8 == 5` | `tag_only_not_operational_equivalence` |

Los artefactos locales M19/M22 identifican la rama `bad -> d` / `tf* -> *`
con el residuo `5 mod 8`, pero no incluyen una especificacion que derive esa
condicion desde palabras alcanzables del SRS mixto binario/ternario. Por eso
C2 queda como validador de guarda congelada y como diagnostico de brecha.

## Archivos producidos

- `reports/m22_c2_semantic_bridge_summary.csv`
- `reports/m22_c2_semantic_bridge_residue_audit.csv`
- `reports/m22_c2_semantic_bridge_violations.csv`
- `reports/m22_c2_semantic_bridge.md`
- `colaboradores/codex-hijo/M22C2SemanticBridge.md`

## Conclusion

El criterio computacional de la guarda S2-k16 pasa. El criterio semantico
fuerte no pasa como equivalencia probada: falta una traduccion real, local y
auditada del SRS mixto al predicado `r mod 8 = 5`. Cualquier C3 debe quedar
bloqueado o rotulado como exploratorio hasta cerrar esta brecha.
