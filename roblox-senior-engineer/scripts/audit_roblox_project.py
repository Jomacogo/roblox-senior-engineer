#!/usr/bin/env python3
"""Auditoría estática heurística para proyectos Roblox/Luau, sin dependencias.

No compila Luau, no ejecuta el juego y no demuestra que un proyecto sea seguro.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

SKIPPED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "Packages",
    "DevPackages",
    "dist",
    "build",
}

PATTERNS = (
    (
        "high",
        "dynamic-code",
        re.compile(r"\bloadstring\s*\("),
        "Carga dinámica de código: revisar necesidad, origen y alternativas seguras.",
    ),
    (
        "high",
        "remote-code",
        re.compile(r"\b(?:game\s*:\s*HttpGet|HttpGetAsync)\s*\("),
        "Descarga HTTP: comprobar que no se ejecute contenido remoto ni se expongan datos.",
    ),
    (
        "high",
        "remote-require",
        re.compile(r"\brequire\s*\(\s*\d+\s*\)"),
        "Require por ID: inspeccionar procedencia, permisos, mantenimiento y código del módulo.",
    ),
    (
        "high",
        "possible-secret",
        re.compile(
            r"(?i)\b(?:api[_-]?key|secret|(?:access[_-]?)?token|password)\b\s*=\s*[\"'][^\"']{8,}[\"']"
        ),
        "Posible secreto incrustado: retirarlo del código y rotarlo si era real.",
    ),
    (
        "medium",
        "http-service",
        re.compile(r"\bHttpService\b"),
        "Uso de red: revisar URLs, permisos, datos enviados, errores y límites.",
    ),
    (
        "low",
        "global-state",
        re.compile(r"(?<![\w])_G(?![\w])"),
        "Estado global: revisar acoplamiento, colisiones y ciclo de vida.",
    ),
)


def finding(
    severity: str,
    rule: str,
    message: str,
    path: Path,
    root: Path,
    line: int | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "severity": severity,
        "rule": rule,
        "message": message,
        "file": str(path.relative_to(root)),
    }
    if line is not None:
        item["line"] = line
    return item


def source_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".lua", ".luau"}:
            continue
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in SKIPPED_DIRS for part in relative.parts[:-1]):
            continue
        yield path


def check_rojo_project(path: Path, root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [
            finding(
                "high",
                "rojo-invalid-json",
                f"No se pudo leer el proyecto Rojo: {exc}",
                path,
                root,
            )
        ]

    def visit(node: Any, location: str) -> None:
        if isinstance(node, dict):
            if "$path" in node:
                raw_path = node["$path"]
                if isinstance(raw_path, str):
                    target = (path.parent / raw_path).resolve()
                    try:
                        target.relative_to(root.resolve())
                    except ValueError:
                        results.append(
                            finding(
                                "medium",
                                "rojo-external-path",
                                f"La ruta Rojo sale del directorio auditado: {raw_path}",
                                path,
                                root,
                            )
                        )
                    if not target.exists():
                        results.append(
                            finding(
                                "high",
                                "rojo-missing-path",
                                f"La ruta Rojo no existe ({location}): {raw_path}",
                                path,
                                root,
                            )
                        )
                else:
                    results.append(
                        finding(
                            "high",
                            "rojo-invalid-path",
                            f"El valor de $path no es texto ({location}).",
                            path,
                            root,
                        )
                    )
            for key, value in node.items():
                visit(value, f"{location}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                visit(value, f"{location}[{index}]")

    visit(data, "$")
    return results


def audit(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    files = list(source_files(root))

    for path in files:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            findings.append(
                finding(
                    "medium",
                    "unreadable-source",
                    f"No se pudo leer como UTF-8: {exc}",
                    path,
                    root,
                )
            )
            continue

        for number, line in enumerate(lines, start=1):
            if line.lstrip().startswith("--"):
                continue
            for severity, rule, pattern, message in PATTERNS:
                if pattern.search(line):
                    findings.append(finding(severity, rule, message, path, root, number))

    rojo_projects = sorted(root.glob("*.project.json"))
    for project in rojo_projects:
        findings.extend(check_rojo_project(project, root))

    if not files:
        findings.append(
            {
                "severity": "info",
                "rule": "no-source",
                "message": "No se encontraron archivos .lua o .luau en el alcance auditado.",
                "file": ".",
            }
        )
    if not rojo_projects:
        findings.append(
            {
                "severity": "info",
                "rule": "no-rojo-project",
                "message": "No se encontró un archivo *.project.json en la raíz; no se validó Rojo.",
                "file": ".",
            }
        )

    counts = Counter(item["severity"] for item in findings)
    return {
        "root": str(root.resolve()),
        "files_scanned": len(files),
        "rojo_projects": len(rojo_projects),
        "summary": {
            severity: counts.get(severity, 0)
            for severity in ("high", "medium", "low", "info")
        },
        "findings": findings,
        "limitations": [
            "Heurística estática: puede producir falsos positivos y omitir vulnerabilidades.",
            "Se omiten dependencias y directorios de salida habituales.",
            "No compila Luau, no ejecuta Studio y no sustituye playtests ni revisión manual.",
        ],
    }


def print_human(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(
        f"Archivos Luau: {report['files_scanned']} | "
        f"Proyectos Rojo: {report['rojo_projects']} | "
        f"Altos: {summary['high']} | Medios: {summary['medium']} | "
        f"Bajos: {summary['low']} | Info: {summary['info']}"
    )
    for item in report["findings"]:
        location = item["file"]
        if "line" in item:
            location += f":{item['line']}"
        print(f"[{item['severity'].upper()}] {location} ({item['rule']})")
        print(f"  {item['message']}")
    print("Limitación: auditoría heurística; no demuestra compilación, seguridad ni ejecución correcta.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Directorio raíz del proyecto Roblox")
    parser.add_argument("--json", action="store_true", help="Emitir el informe como JSON")
    parser.add_argument(
        "--fail-on-high",
        action="store_true",
        help="Salir con código 1 si hay hallazgos de severidad alta",
    )
    args = parser.parse_args()

    root = args.root.expanduser()
    if not root.is_dir():
        parser.error(f"no es un directorio válido: {root}")

    report = audit(root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)

    if args.fail_on_high and report["summary"]["high"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
