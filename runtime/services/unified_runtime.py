#!/usr/bin/env python3
"""Unified KEDDEH runtime service layer.

This module formalizes the service architecture:
- HTTPS static web service
- HTTP redirect service
- UDP DNS service
- custom runtime orchestration
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[1]


class UnifiedServiceManifest:
    def __init__(self, root: Path = ROOT):
        self.root = root
        self.manifest_path = root / "runtime" / "manifest.json"

    def load(self) -> Dict[str, Any]:
        if not self.manifest_path.exists():
            return {
                "service": "keddeh_unified_runtime",
                "status": "uninitialized",
                "custom_runtime": True,
                "github_dependencies": False,
                "ports": {"https": 443, "http": 80, "dns": 5300},
            }
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    manifest = UnifiedServiceManifest()
    print(json.dumps(manifest.load(), indent=2))
