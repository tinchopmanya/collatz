# Conlusion dinamica

Ultima actualizacion: 2026-04-25 02:32:13 -03:00
Tema activo: Collatz - Septima Ola cerrada

## Conlusion ejecutiva

La septima ola paso de bloques aislados a cadenas odd-to-odd. Para cada impar:

```text
n_i = 2^s q - 1
n_{i+1} = (3^s q - 1) / 2^r
r = v2(3^s q - 1)
```

se itero hasta llegar a `1`, bajar por debajo del impar inicial o agotar `256` bloques.

En todos los impares `3 <= n <= 1000000`, no hubo casos que agotaran el limite. El maximo observado fue:

```text
41 bloques odd-to-odd hasta bajar
```

## Hallazgo principal

La cola siguiente parece resetearse. Condicionado por la cola actual `v2(n_i + 1)`, el promedio de `v2(n_{i+1} + 1)` queda cerca de:

```text
2
```

Esto refuerza la lectura central:

- una cola larga de unos genera expansion local;
- la salida de ese bloque suele mezclar la informacion 2-adica;
- no aparece, en esta escala, una fabricacion automatica de colas largas consecutivas.

## Veredicto

No se probo Collatz. Pero ya tenemos una estructura de trabajo mas fina:

- bloque alternante exacto;
- salida 2-adica casi geometrica;
- cadena odd-to-odd con evidencia de reseteo;
- separacion entre records de duracion y records de altura.

La pregunta publicable posible no es "encontramos una prueba", sino:

> Se puede describir cuantitativamente la dinamica Collatz por bloques y demostrar que las colas largas se mezclan rapido?

## Siguiente paso

Abrir una octava ola para comparar cadenas reales contra un modelo estocastico:

- trazar records como `626331`, `159487`, `270271`;
- medir productos logaritmicos de factores locales;
- comparar contra colas geometricas independientes;
- buscar correlaciones persistentes entre `s_i` y `s_{i+1}`;
- decidir si hay un reporte tecnico formalizable.
