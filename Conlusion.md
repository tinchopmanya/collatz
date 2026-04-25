# Conlusion dinamica

Ultima actualizacion: 2026-04-25 02:12:23 -03:00
Tema activo: Collatz - Quinta Ola cerrada

## Conlusion ejecutiva

La quinta ola convirtio una medicion experimental en un lemma local exacto. Para todo impar positivo `n`, si `s = v2(n + 1)`, entonces la longitud exacta del prefijo alternante inicial bajo el mapa clasico de Collatz es:

```text
2s = 2 * v2(n + 1)
```

Escribiendo `n = 2^s q - 1`, con `q` impar, se obtiene la forma cerrada:

```text
C^(2j)(n) = 3^j 2^(s-j) q - 1
C^(2j+1)(n) = 3^(j+1) 2^(s-j) q - 2
```

Esto explica por que las clases `127`, `255` y `511` tienen las longitudes alternantes observadas y por que `511 mod 512` promedia casi `20` pasos alternantes. Tambien da el pico temprano exacto del bloque:

```text
C^(2s-1)(n) = 2(3^s q - 1)
```

## Veredicto

No se probo Collatz. Pero se logro algo valioso: una observacion experimental ahora tiene formula, prueba, codigo y tests. La parte ya entendida es el bloque alternante. Lo desconocido empieza en la salida:

```text
C^(2s)(n) = 3^s q - 1
```

## Siguiente paso

Abrir una sexta ola sobre el mapa de salida:

- estudiar `q -> 3^s q - 1`;
- medir `v2(3^s q - 1)` para familias de `q`;
- buscar si hay clases de salida no obvias;
- comparar contra Mersenne tails y literatura reciente;
- decidir si aparece una estructura menos conocida que merezca reporte tecnico.
