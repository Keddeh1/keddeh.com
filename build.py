#!/usr/bin/env python3
"""
KEDDEH.COM Build and Packaging System

Formalizes the engineering lifecycle:
- Source code organization
- Dependency management
- Runtime packaging
- Deployment configuration
"""

from pathlib import Path
from typing import Dict, List
import json
import sys

ROOT = Path(__file__).resolve().parent

# Package version and metadata
PACKAGE_METADATA = {
    "name": "keddeh.com",
    "version": "1.0.0-alpha.1",
    "author": "Keddeh Systems",
    "license": "Proprietary Sovereign Triad",
    "description": "Wire-based autonomous computing platform with KEX/BRAINK/IL-LLM runtime",
    "runtime": {
        "type": "custom",
        "layers": ["KEX", "BRAINK", "IL-LLM", "FROST", "Mesh"],
        "no_github_dependencies": True,
    },
}

# Core runtime components
RUNTIME_COMPONENTS = {
    "kex": {
        "module": "runtime.local-runtime.kex_geometry",
        "class": "KEXStateGeometry",
        "purpose": "State geometry, identity anchors, physical partition layout",
        "planes": 5,
        "coordinates": ["root", "runtime_active", "runtime_staging", "dns_primary", "dns_secondary", "web_index", "web_assets"],
    },
    "braink": {
        "module": "runtime.local-runtime.braink_fabric",
        "class": "BRAINKExecutionFabric",
        "purpose": "Governed execution, evidence logging, independent verification",
        "features": ["permitted_transitions", "coherence_tracking", "audit_trail", "external_verification"],
    },
    "il_llm": {
        "module": "runtime.local-runtime.il_llm_semantic",
        "class": "ILLMSemanticSubstrate",
        "purpose": "Local-first semantic substrate, knowledge graphs, persistent indexes",
        "features": ["entity_registration", "relation_tracking", "graph_traversal", "persistent_knowledge"],
    },
    "frost": {
        "module": "runtime.local-runtime.frost_signatures",
        "class": "FROSTThresholdSignature",
        "purpose": "Distributed multiparty threshold signatures over Ed25519",
        "scheme": "FROST_Round_2",
        "finite_field": "Ed25519_F_q",
    },
    "mesh": {
        "module": "runtime.local-runtime.mesh_topology",
        "class": "MeshTopologyCoordinator",
        "purpose": "Hierarchical overlay mesh, phase-lock governance, autogenetic forks",
        "features": ["intra_domain_coupling", "inter_domain_coupling", "flywheel_mode", "soft_phase_capture"],
    },
}

# Application services
SERVICES = {
    "https_server": {
        "module": "runtime.keddeh_venv_runtime",
        "handler": "StaticHTTPSHandler",
        "port": 443,
        "protocol": "TLS 1.3",
        "document_root": "apps/www",
        "features": ["HSTS", "self_signed_cert_generation", "static_content_serving"],
    },
    "http_redirect": {
        "module": "runtime.keddeh_venv_runtime",
        "handler": "RedirectHTTPHandler",
        "port": 80,
        "protocol": "HTTP/1.1",
        "features": ["301_redirect_to_https", "header_forwarding"],
    },
    "dns_udp": {
        "module": "runtime.keddeh_venv_runtime",
        "handler": "DNSUDPServer",
        "port": 5300,
        "protocol": "UDP",
        "features": ["domain_resolution", "a_record_lookup", "standard_library_sockets"],
    },
}

class Build:
    """Formalized build system for KEDDEH.COM."""

    def __init__(self, root: Path = ROOT):
        self.root = root
        self.dist_dir = root / "dist"
        self.build_dir = root / "build"
        self.venv_dir = root / "venv"

    def ensure_directories(self):
        """Ensure all build directories exist."""
        self.dist_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)
        print(f"[BUILD] directories: {self.dist_dir}, {self.build_dir}")

    def package_info(self) -> Dict:
        """Return packaging information."""
        return {
            "metadata": PACKAGE_METADATA,
            "components": {k: {vk: vv for vk, vv in v.items() if vk != "class"} for k, v in RUNTIME_COMPONENTS.items()},
            "services": {k: {vk: vv for vk, vv in v.items() if vk != "handler"} for k, v in SERVICES.items()},
        }

    def validate(self) -> bool:
        """Validate all runtime components are present."""
        errors = []
        for name, component in RUNTIME_COMPONENTS.items():
            module_path = self.root / component["module"].replace(".", "/") + ".py"
            if not module_path.exists():
                errors.append(f"Missing {name}: {module_path}")
        if errors:
            print("[BUILD] Validation errors:")
            for err in errors:
                print(f"  - {err}")
            return False
        print("[BUILD] Validation passed")
        return True

    def generate_manifest(self) -> str:
        """Generate runtime manifest."""
        manifest = {
            "package": PACKAGE_METADATA,
            "components": RUNTIME_COMPONENTS,
            "services": SERVICES,
            "build_timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        }
        manifest_json = json.dumps(manifest, indent=2)
        manifest_path = self.build_dir / "MANIFEST.json"
        manifest_path.write_text(manifest_json)
        print(f"[BUILD] manifest: {manifest_path}")
        return manifest_json

    def list_runtime_modules(self) -> List[str]:
        """List all runtime modules to be packaged."""
        modules = []
        runtime_dir = self.root / "runtime"
        for py_file in runtime_dir.glob("local-runtime/*.py"):
            modules.append(str(py_file.relative_to(self.root)))
        for py_file in runtime_dir.glob("*.py"):
            if py_file.name != "__pycache__":
                modules.append(str(py_file.relative_to(self.root)))
        return sorted(modules)


def main():
    build = Build()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "validate":
            if build.validate():
                sys.exit(0)
            sys.exit(1)
        elif cmd == "manifest":
            print(build.generate_manifest())
        elif cmd == "info":
            print(json.dumps(build.package_info(), indent=2))
        elif cmd == "modules":
            for mod in build.list_runtime_modules():
                print(mod)
        elif cmd == "prepare":
            build.ensure_directories()
            build.validate()
            build.generate_manifest()
            print("[BUILD] prepared")
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)
    else:
        build.ensure_directories()
        build.validate()
        build.generate_manifest()
        print("\n[BUILD] available commands:")
        print("  validate     - check all runtime components")
        print("  manifest     - generate runtime manifest")
        print("  info         - show package information")
        print("  modules      - list runtime modules")
        print("  prepare      - full build preparation")


if __name__ == "__main__":
    main()
