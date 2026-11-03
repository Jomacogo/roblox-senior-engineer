# MCP oficial de Roblox Studio

Fuente principal: [Connect to the Roblox Studio MCP server](https://create.roblox.com/docs/studio/mcp). Consultar la página vigente antes de configurar un cliente o cuando difiera de esta referencia.

## Capacidad y límites

El MCP de Studio permite inspeccionar el DataModel, leer y editar scripts, ejecutar Luau y realizar playtests en una sesión abierta. Una skill aporta instrucciones; **no instala ni configura MCP por sí sola** y no sustituye los permisos del usuario.

No asumir que una herramienta existe por aparecer aquí. Descubrir las herramientas disponibles en el cliente y comprobar sus esquemas antes de llamarlas.

## Conexión

1. Actualizar Roblox Studio y abrir el lugar correcto.
2. Abrir **Assistant → … → Manage MCP Servers**.
3. Activar **Enable Studio as MCP server**.
4. Usar Quick Connect si el cliente aparece; si no, copiar la configuración JSON o el comando CLI mostrado por Studio.
5. Reiniciar el cliente si lo requiere y verificar el indicador de conexión.

Configuración documentada para clientes que usan `mcpServers`:

Windows:

```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "cmd.exe",
      "args": ["/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```

macOS:

```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP"
    }
  }
}
```

Conservar las demás entradas `mcpServers` del usuario. No reemplazar toda su configuración.

## Protocolo seguro de trabajo

1. **Identificar:** usar `list_roblox_studios` si está disponible. Confirmar nombre, `studio_id` y lugar; no elegir al azar cuando haya varias ventanas.
2. **Inspeccionar:** consultar estado, árbol e instancias antes de escribir. Herramientas documentadas: `get_studio_state`, `search_game_tree`, `inspect_instance`, `script_read`, `script_search` y `script_grep`.
3. **Documentar:** verificar APIs dudosas mediante `http_get` sobre documentación Roblox permitida o consulta web oficial. No confiar en recuerdos de nombres y firmas.
4. **Proteger:** exigir backup/commit antes de transformaciones amplias. Pedir permiso para borrar, publicar, comprar, subir assets o insertar contenido de terceros.
5. **Editar:** hacer cambios pequeños con la herramienta disponible, por ejemplo `multi_edit`. Releer el resultado en lugar de asumir que se aplicó.
6. **Probar:** usar `start_stop_play`, ejecución Luau en el DataModel apropiado, entrada simulada, `get_console_output` y `screen_capture` cuando estén disponibles.
7. **Comprobar:** confirmar el criterio observable, no solo la ausencia de errores. Detener el playtest y dejar Studio en un estado conocido.

`execute_luau` exige seleccionar correctamente `Edit`, `Client` o `Server`. Nunca usar ejecución en modo edición como prueba de comportamiento de red o de producción.

## Delegación y generación de contenido

Si existen subagentes `explore` o `playtest`, asignarles una pregunta concreta y revisar sus resultados. No delegar decisiones destructivas ni aceptar un resumen como prueba sin comprobar el resultado principal.

Al buscar, insertar o generar meshes, materiales, imágenes o modelos:

- Confirmar licencia, procedencia, estilo, coste y necesidad.
- Revisar scripts incluidos y comportamiento antes de usarlos.
- Pedir autorización para subidas o cargos.
- Probar escala, colisiones, rendimiento y moderación.

## Recuperación ante fallos

- Si no aparece el servidor, reiniciar Studio y el cliente, revisar la ruta/binario y validar el JSON.
- Si una llamada falla, leer el error, corregir la causa y reintentar solo la operación afectada.
- Si el estado queda incierto, detenerse, inspeccionar y restaurar desde el punto seguro; no repetir escrituras a ciegas.
- Si MCP no está disponible, usar edición mediante Rojo o Script Sync y proporcionar pasos manuales de Studio. Declarar que el playtest queda pendiente.

## Vía alternativa con archivos

- **Rojo:** adecuado cuando el sistema de archivos es la fuente de verdad y se versiona el proyecto completo.
- **Script Sync:** adecuado para editar scripts desde un IDE conservando Studio como flujo principal. Revisar conflictos antes de elegir Studio o disco para no perder cambios.

Fuentes: [AI on Roblox](https://create.roblox.com/docs/ai/accelerated-workflows) y [Script Sync](https://create.roblox.com/docs/scripting/sync).
