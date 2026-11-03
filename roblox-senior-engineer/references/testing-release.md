# Verificación, playtests y lanzamiento

## Índice

1. Estrategia proporcional
2. Matriz mínima
3. MCP y Studio
4. Rendimiento y dispositivos
5. Publicación y rollback
6. Evidencia de cierre

## 1. Estrategia proporcional

Adaptar el coste de prueba al riesgo. Un texto local no requiere la misma batería que economía, comercio, compras o migración de datos.

Priorizar:

- Pruebas pequeñas para reglas puras y cálculos.
- Integración para remotes, ciclo de ronda, datos y permisos.
- Playtests para experiencia real, replicación, UI y dispositivos.
- Métricas antes/después para rendimiento y cambios de producto.

No sustituir un playtest por lint. Lint, tipos y auditorías estáticas no detectan por sí solos errores de diseño, red o runtime.

## 2. Matriz mínima

Seleccionar las filas relevantes y registrar resultado:

| Área | Casos |
|---|---|
| Camino feliz | Entrar, entender objetivo, completar acción, recibir resultado y repetir |
| Red | Dos clientes, latencia razonable, desconexión, reingreso y mensajes duplicados |
| Abuso | Argumentos incorrectos, NaN/infinito, valores extremos, spam y permisos falsos |
| Estado | Inicio/fin de ronda, salida a mitad, reaparición, limpieza y doble recompensa |
| Datos | Primera visita, esquema anterior, fallo de carga/guardado y migración |
| Compras | Recibo repetido, fallo de entrega, reintento y ausencia de doble cargo/concesión |
| UI/entrada | Ratón/teclado, táctil y gamepad cuando correspondan; escalas y safe areas |
| Rendimiento | Escena cargada, muchos jugadores/efectos, memoria, red y frame time |
| Compatibilidad | Streaming, dispositivos modestos y funciones beta si aplican |

Para bugs, conservar un caso que falle antes del arreglo cuando sea posible y demostrar que pasa después.

## 3. MCP y Studio

Antes de probar, confirmar lugar, `studio_id` y modo de ejecución. Después:

1. Releer scripts o instancias modificados.
2. Ejecutar comprobaciones estáticas configuradas.
3. Iniciar playtest y seguir un guion observable.
4. Capturar salida de consola y capturas solo cuando ayuden a verificar.
5. Probar dos jugadores para sistemas compartidos; no afirmar cobertura multicliente con un solo jugador.
6. Detener el playtest y comprobar que no quedan procesos o cambios accidentales.

No usar `execute_luau` en modo Edit como sustituto de una prueba Server/Client. No afirmar que compras, teletransportes u otros servicios funcionan en producción si Studio no permite probarlos completamente.

## 4. Rendimiento y dispositivos

Definir una escena y recorrido reproducibles. Capturar frame time, memoria, red o carga según el problema. Usar MicroProfiler para localizar el cuello de botella antes de cambiar código.

Comparar antes/después con la misma escena y condiciones. Reportar entorno, duración y limitaciones. No resumir una captura como “+40 % de rendimiento” sin cálculo y datos suficientes.

Probar en hardware representativo cuando sea posible, especialmente móvil. Si solo se probó Studio, indicarlo. Revisar también legibilidad, tamaño de controles, orientación, cámara y recuperación de errores.

Fuentes: [MicroProfiler](https://create.roblox.com/docs/performance-optimization/microprofiler), [Test on hardware](https://create.roblox.com/docs/performance-optimization/test-on-hardware) y [Beta test games](https://create.roblox.com/docs/education/developer/beta-testing-experiences).

## 5. Publicación y rollback

Publicar únicamente con autorización explícita. Antes:

- Confirmar universo/lugar, rama y versión.
- Revisar diff, secretos, assets, permisos, configuración y pruebas.
- Guardar una versión anterior recuperable.
- Preparar métricas de salud y criterios de reversión.
- Comprobar compatibilidad de datos entre versión anterior y nueva.

Después, verificar el comportamiento observable permitido y vigilar errores, adquisición, retención y monetización según el cambio. No correlacionar automáticamente una variación con el lanzamiento sin controlar cohortes y periodo.

Si aparece un fallo grave, priorizar contención y rollback conocido. No improvisar migraciones destructivas sobre producción.

## 6. Evidencia de cierre

Entregar una lista honesta:

```text
Criterios cumplidos: [...]
Comprobaciones ejecutadas: [...]
Resultados observados: [...]
No probado / limitaciones: [...]
Riesgo restante: [...]
```

Si faltan herramientas o acceso, proporcionar pasos manuales concretos y marcar el criterio como pendiente. Nunca completar esta lista con resultados imaginados.
