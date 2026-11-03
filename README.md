# Roblox Senior Engineer

Skill en español para convertir un agente de IA compatible en un copiloto riguroso de desarrollo Roblox. Refuerza análisis, arquitectura Luau, seguridad cliente-servidor, uso del MCP oficial de Roblox Studio, pruebas, rendimiento, investigación de tendencias, prototipado, analítica y lanzamiento.

No garantiza viralidad ni sustituye playtests, revisión humana, dispositivos reales o las políticas vigentes de Roblox.

## Qué incluye

```text
roblox-senior-engineer/
├── SKILL.md                         # Instrucciones y flujo principal
├── references/
│   ├── mcp-studio.md                # Conexión y uso seguro del MCP oficial
│   ├── architecture-security.md     # Luau, remotes, datos, compras y rendimiento
│   ├── game-design-trends.md        # Tendencias, bucle, analítica y monetización
│   └── testing-release.md           # Pruebas, dispositivos, publicación y rollback
├── scripts/
│   └── audit_roblox_project.py      # Auditoría estática heurística sin dependencias
└── assets/
    └── rojo-base/                   # Plantilla mínima para proyectos nuevos con Rojo
```

## Opción 1: instalar con el enlace del repositorio

```text
https://github.com/Jomacogo/roblox-senior-engineer/tree/main/roblox-senior-engineer
```

Pégale a tu agente este mensaje:

```text
Instala la skill roblox-senior-engineer desde esta carpeta de mi repositorio:
https://github.com/Jomacogo/roblox-senior-engineer/tree/main/roblox-senior-engineer

Conserva todos sus archivos y carpetas. Verifica que SKILL.md tenga el nombre
roblox-senior-engineer y que las referencias, scripts y assets estén presentes.
Reinicia o recarga las skills si tu plataforma lo requiere. No conectes MCP ni
modifiques Roblox Studio todavía.
```

Esto funciona cuando tu agente admite instalación de skills desde repositorios. No todos los agentes admiten instalación por URL; en ese caso usa una de las dos opciones siguientes.

## Opción 2: importar el archivo .skill

1. Descarga `dist/roblox-senior-engineer.skill` de este repositorio o de su release.
2. Abre la sección de skills de tu agente.
3. Selecciona **Importar**, **Instalar skill** o la opción equivalente.
4. Sube el archivo `.skill` completo, sin descomprimirlo.
5. Recarga el agente si es necesario y comprueba que aparece `roblox-senior-engineer`.

## Opción 3: instalación manual

1. Clona o descarga el repositorio.
2. Copia la carpeta completa `roblox-senior-engineer` —la que contiene `SKILL.md`— al directorio de skills indicado en la documentación de tu agente.
3. No copies solamente `SKILL.md`: la skill utiliza sus referencias, script y plantilla.
4. Reinicia o recarga el agente.
5. Pregunta: “¿Qué skill usas para desarrollar Roblox y qué archivos incluye?”.

También puedes usarla sin instalación persistente pidiendo al agente que lea y siga el `SKILL.md` del repositorio, siempre que el agente pueda acceder a sus recursos. Esto depende del contexto y no equivale a instalarla.

## Subirlo a GitHub

Crea un repositorio vacío llamado `roblox-senior-engineer` en GitHub. Desde la carpeta que contiene este README:

```bash
git init
git add .
git commit -m "feat: add Roblox senior engineer skill"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/roblox-senior-engineer.git
git push -u origin main
```

## Conectar Roblox Studio por MCP

La skill y MCP son componentes distintos: instalar la skill no abre Roblox Studio ni concede acceso a tu lugar.

1. Actualiza y abre Roblox Studio con una copia de seguridad del lugar.
2. Abre **Assistant → … → Manage MCP Servers**.
3. Activa **Enable Studio as MCP server**.
4. Usa **Quick Connect** si tu cliente aparece. Si no, copia la configuración JSON o el comando CLI que muestra Studio en la configuración MCP de tu agente.
5. Reinicia el cliente si lo solicita y comprueba el indicador de conexión.

Configuración oficial documentada para Windows:

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

Configuración oficial documentada para macOS:

```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP"
    }
  }
}
```

Si ya tienes otros servidores MCP, añade solo la entrada `Roblox_Studio`; no borres tu configuración existente. Consulta la guía vigente: [Roblox Studio MCP](https://create.roblox.com/docs/studio/mcp).

## Primer uso recomendado

Empieza en modo solo lectura:

```text
Usa roblox-senior-engineer. Inspecciona el lugar abierto en Roblox Studio mediante MCP.
No edites, borres, insertes assets ni publiques. Identifica la instancia de Studio,
resume la arquitectura real, encuentra riesgos concretos y propón una prueba para cada
hallazgo. Distingue lo observado de lo inferido.
```

Después, para crear un prototipo:

```text
Usa roblox-senior-engineer para crear una rebanada vertical de un juego Roblox.
Investiga primero tres señales actuales con fuentes y fechas; no inventes métricas.
Propón como máximo tres ideas originales y espera mi elección. Después define criterios
de aceptación, programa el bucle mínimo con Luau y servidor autoritativo, y pruébalo
mediante MCP. No publiques sin mi permiso. Entrega cambios, pruebas ejecutadas y límites.
```

## Auditoría local opcional

Desde la carpeta de la skill, con Python 3 instalado:

```bash
python3 scripts/audit_roblox_project.py /ruta/a/tu/proyecto
python3 scripts/audit_roblox_project.py /ruta/a/tu/proyecto --json
```

El script revisa rutas Rojo y señales como carga dinámica, `require` por ID, posibles secretos, HTTP y estado global. Son avisos heurísticos: no compila Luau, no ejecuta Studio y no demuestra que el juego sea seguro.

## Reglas de seguridad recomendadas

- Trabaja con Git o una copia de seguridad antes de permitir cambios.
- Abre primero un lugar de prueba, no producción.
- Revisa los diffs y los resultados del playtest.
- Autoriza por separado publicación, borrados, compras, subidas e inserción de assets.
- No compartas cookies, tokens, claves API ni credenciales con el agente.
