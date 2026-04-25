# Protocolo de autonomia

Fecha: 2026-04-25

## Que puedo hacer sin pedir permiso

- Leer y auditar los archivos del repo.
- Buscar fuentes publicas y recientes.
- Crear documentos de investigacion.
- Crear scripts, tests y reportes.
- Generar datasets chicos en carpetas ignoradas por git.
- Hacer commits pequenos y descriptivos.
- Pushear avances a `main` si el working tree esta limpio y el cambio es incremental.
- Abrir issues de GitHub como backlog de trabajo.

## Que deberia preguntarte antes

- Reescribir historia de git o hacer `force push`.
- Borrar archivos no generados por mi.
- Cambiar el foco principal del proyecto.
- Instalar dependencias pesadas o herramientas de sistema.
- Usar servicios externos con costo.
- Publicar claims fuertes fuera del repo.
- Convertir una hipotesis en afirmacion matematica fuerte.

## Como voy a trabajar varias horas

1. Elegir el milestone activo.
2. Crear una rama mental de trabajo chica: auditar, implementar, medir o reportar.
3. Dejar cada avance en archivos concretos.
4. Verificar con tests o scripts.
5. Commit y push cuando haya un punto estable.
6. Actualizar `Conlusion.md` solo cuando cambie la decision operativa.

## Primer milestone activo

M0 - Higiene y auditoria.

Razon: antes de buscar patrones nuevos, necesitamos saber que partes de las olas anteriores son base firme y que partes son especulativas.
