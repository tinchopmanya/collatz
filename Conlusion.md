# Conlusion dinamica

Ultima actualizacion: 2026-04-25 02:24:36 -03:00
Tema activo: Collatz - Sexta Ola cerrada

## Conlusion ejecutiva

La sexta ola avanzo desde el prefijo alternante hacia su salida. Si `n` es impar y:

```text
n = 2^s q - 1
s = v2(n + 1)
q impar
```

entonces la quinta ola habia mostrado que el bloque alternante termina en:

```text
C^(2s)(n) = 3^s q - 1
```

Ahora medimos y formalizamos el paso siguiente:

```text
r = v2(3^s q - 1)
m = (3^s q - 1) / 2^r
```

donde `m` es el siguiente impar despues del bloque.

## Hallazgo principal

Hasta `n <= 1000000`, la distribucion de `r` fue casi exactamente geometrica:

```text
P(r = k) ~= 2^-k
E[r] ~= 2
```

Esto tiene explicacion 2-adica: para `s` fijo, `3^s` es invertible modulo potencias de `2`, asi que la condicion `3^s q == 1 mod 2^k` selecciona una clase residual entre los `q` impares.

La consecuencia dinamica es:

```text
E[m/n | s] ~= (3/2)^s / 3
```

Es decir: una cola larga de unos genera expansion local fuerte, y la division de salida normalmente no alcanza para cancelarla.

## Veredicto

No se probo Collatz. El avance es mecanico y local:

- sabemos por que las colas largas expanden;
- sabemos como se distribuye la division de salida;
- observamos que la siguiente cola `v2(m + 1)` vuelve a promedio cercano a `2`;
- el sistema parece mezclar despues de cada expansion local, pero eso todavia debe medirse por cadenas.

## Siguiente paso

Abrir una septima ola sobre la dinamica odd-to-odd:

```text
n_i -> n_{i+1}
```

y medir correlaciones entre colas consecutivas, productos locales, bloques expansivos encadenados y diferencias contra un modelo geometrico independiente.
