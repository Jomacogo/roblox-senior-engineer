# Arquitectura, Luau, seguridad y rendimiento

## Índice

1. Diseño del proyecto
2. Contratos cliente-servidor
3. Persistencia y compras
4. Rendimiento
5. Revisión de assets y dependencias
6. Fuentes oficiales

## 1. Diseño del proyecto

Mantener una separación visible por contexto de ejecución:

```text
src/
  client/     LocalScripts, controladores, UI y efectos
  server/     Scripts, servicios, reglas y persistencia
  shared/     Tipos, constantes y datos replicables no secretos
```

En Studio, usar ubicaciones equivalentes (`StarterPlayerScripts`, `ServerScriptService`, `ReplicatedStorage`). No imponer esta estructura si el proyecto ya tiene una convención coherente.

Escribir Luau claro y tipado donde aporte valor:

- Usar `--!strict` en módulos nuevos cuando sea viable; no romper un proyecto legacy para imponerlo globalmente.
- Exportar tipos de contratos compartidos y anotar límites de módulos, remotes y datos guardados.
- Evitar ciclos de `require`, variables globales, `_G`, módulos con múltiples responsabilidades y largas cadenas de `WaitForChild` como sustituto de una arquitectura.
- Inicializar dependencias en un orden explícito. Hacer que el arranque falle de forma visible y controlada, no con esperas infinitas silenciosas.
- Desconectar eventos y limpiar estado en `PlayerRemoving`, al destruir objetos o al terminar una ronda.
- Configurar valores en módulos o configuraciones mantenibles; no dispersar números mágicos.

Elegir composición y módulos pequeños antes que clases profundas. No crear una capa genérica para una sola operación sin expectativa real de reutilización.

## 2. Contratos cliente-servidor

Asumir que un explotador controla su cliente y puede invocar remotes con argumentos arbitrarios. Para cada operación definir:

- Nombre y dirección del remote.
- Esquema, tipos, tamaño y rangos permitidos.
- Permisos y estado requeridos.
- Cooldown o límite de frecuencia en servidor.
- Resultado y comportamiento ante errores.
- Pruebas válidas, inválidas y de spam.

El servidor debe validar tipo, estructura, valores finitos, longitud de strings, claves de tablas, distancia, estado del personaje, propiedad del objeto, recursos y permisos según corresponda. Rechazar entradas no válidas antes de mutar estado.

```luau
if type(quantity) ~= "number" or not math.isfinite(quantity) then
	return false, "Cantidad no válida"
end
if quantity <= 0 or quantity % 1 ~= 0 or quantity > MAX_QUANTITY then
	return false, "Cantidad fuera de rango"
end
```

Este fragmento solo ilustra validación numérica; no sustituye las demás comprobaciones ni demuestra que una compra sea segura.

Usar el cliente para respuesta inmediata y presentación, nunca como autoridad de economía o resultado. Evitar invocar al cliente desde el servidor para decisiones críticas: puede desconectarse, no responder o devolver datos manipulados.

Aplicar la misma revisión a interacciones iniciadas por `ProximityPrompt`, `ClickDetector`, `Touched` u otros eventos que un cliente pueda manipular. No asumir que propiedades visuales o distancias configuradas solo en cliente constituyen seguridad.

No enviar tablas enormes ni estado cada frame. Replicar únicamente datos necesarios, al cambiar o con una frecuencia justificada. Mantener efectos puramente visuales en cliente.

## 3. Persistencia y compras

Antes de alterar datos guardados, inventariar esquema, claves, versiones y consumidores. Preparar migración compatible y backup; nunca borrar o reiniciar datos de jugadores sin autorización explícita.

Para persistencia:

- Guardar solo datos serializables, validados y acotados.
- Versionar el esquema y aplicar migraciones idempotentes.
- Manejar errores y límites de presupuesto de las APIs; consultar la documentación vigente para elegir lectura, escritura y reintentos.
- Evitar escrituras por cada cambio menor; agrupar sin perder garantías importantes.
- Probar reingreso, datos ausentes, datos antiguos, fallo de guardado, salida durante una transacción y duplicación.
- Limpiar estado en memoria al salir el jugador.

Para productos y pases:

- Verificar y entregar en servidor.
- Consultar la documentación vigente de `MarketplaceService` y `ProcessReceipt` antes de implementar recibos.
- Hacer la concesión idempotente y registrar el identificador de recibo para no entregar dos veces.
- No confirmar una compra basándose en un evento del cliente.
- Probar recibo repetido, fallo antes/después de conceder y reingreso.

No guardar secretos ni lógica confidencial en módulos replicados. Separar reglas sensibles del código compartido.

## 4. Rendimiento

Medir primero. Capturar un caso reproducible y comparar el mismo recorrido antes y después.

Revisar según el síntoma:

- **CPU de scripts:** operaciones por frame, bucles grandes, serialización, escaneos repetidos del DataModel y trabajo síncrono.
- **Red:** payloads grandes, ráfagas de remotes, replicación innecesaria y cambios frecuentes de instancias.
- **Memoria/carga:** contenido en `ReplicatedStorage` y `ReplicatedFirst`, assets únicos, texturas, audio y streaming.
- **Física:** assemblies, colisiones precisas, constraints, propiedad de red y objetos sin necesidad de colisión.
- **Escena:** partes y meshes únicos, nivel de detalle, modelos innecesariamente complejos y efectos.
- **Fugas:** conexiones, caches por jugador, instancias huérfanas y tareas que sobreviven a su propietario.

Usar MicroProfiler, Developer Console, estadísticas y pruebas en hardware cuando estén disponibles. No activar streaming, paralelismo, pooling o native code generation de forma automática: comprobar compatibilidad y beneficio medido.

Probar especialmente móvil si pertenece a la audiencia. Un playtest fluido en un PC potente no demuestra buen rendimiento en teléfonos.

## 5. Revisión de assets y dependencias

Antes de adoptar un modelo, plugin, paquete o módulo:

1. Comprobar autor, licencia, mantenimiento y procedencia.
2. Inspeccionar scripts, llamadas HTTP, `require` por ID, carga dinámica y permisos.
3. Medir impacto y eliminar contenido innecesario.
4. Fijar versiones cuando el gestor lo permita.
5. Mantener una alternativa de reversión.

## 6. Fuentes oficiales

- [Securing the client-server boundary](https://create.roblox.com/docs/scripting/security/client-server-boundary)
- [Security and cheat mitigation tactics](https://create.roblox.com/docs/scripting/security/security-tactics)
- [Access control and confidentiality](https://create.roblox.com/docs/scripting/security/access-control)
- [Remote events and callbacks](https://create.roblox.com/docs/scripting/events/remote)
- [Improve performance](https://create.roblox.com/docs/performance-optimization/improve)
- [MicroProfiler](https://create.roblox.com/docs/performance-optimization/microprofiler)
- [Test on hardware](https://create.roblox.com/docs/performance-optimization/test-on-hardware)
