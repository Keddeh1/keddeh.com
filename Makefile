PYTHON ?= python3
ROOT := $(CURDIR)

.PHONY: bootstrap validate run dns site manifest clean

bootstrap:
	$(PYTHON) -m venv venv || true
	. venv/bin/activate && $(PYTHON) -m pip install --upgrade pip setuptools wheel || true
	@echo "[KEDDEH] local runtime environment bootstrapped"

validate:
	$(PYTHON) build.py validate

manifest:
	$(PYTHON) build.py manifest

run:
	$(PYTHON) runtime/keddeh_venv_runtime.py

dns:
	$(PYTHON) runtime/keddeh_venv_runtime.py

site:
	$(PYTHON) -m http.server 8080 --directory $(ROOT)/apps/www

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "[KEDDEH] local build artifacts cleaned"
