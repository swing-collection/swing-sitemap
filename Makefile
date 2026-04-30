# =============================================================================
# Makefile - Development Automation
# =============================================================================
#
# Common development tasks for Python/Django + Node.js projects.
# Documentation: https://www.gnu.org/software/make/manual/make.html
#
# This file is portable - copy to other repos without modification.
#
# -----------------------------------------------------------------------------
# Usage
# -----------------------------------------------------------------------------
#
#   Show available targets:
#     make help
#
#   Run a target:
#     make install
#     make test
#     make lint
#
#   Run multiple targets:
#     make lint test
#
# -----------------------------------------------------------------------------
# Why Make?
# -----------------------------------------------------------------------------
#
# Make provides:
#   - Tab-completion for targets
#   - Self-documenting help via ## comments
#   - Cross-platform (works on macOS, Linux, WSL)
#   - No runtime dependencies
#   - Familiar to most developers
#
# =============================================================================


# =============================================================================
# Configuration
# =============================================================================

# Include port configuration (single source of truth)
-include ports.mk

# Export port variables for Procfile/honcho
export DJANGO_PORT
export MKDOCS_PORT


# Prevent make from treating targets as files
.PHONY: help install install-dev start stop clean test lint format typecheck \
        docs docs-build build migrate makemigrations shell collectstatic \
        runserver pre-commit translate-make translate-compile \
        translate-validate translate-clean clean-ports test-fast test-verbose \
        lint-py lint-js lint-yaml lint-md lint-shell lint-docker lint-all

# Default target when running `make` with no arguments
.DEFAULT_GOAL := help


# -----------------------------------------------------------------------------
# Executables
# -----------------------------------------------------------------------------
# Use poetry run to ensure correct virtual environment

PYTHON := poetry run python
PYTEST := poetry run pytest
NPM := npm


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
# Portable paths - no project-specific names

SRC_DIR := src
TST_DIR := tst
EXE_DIR := exe


# -----------------------------------------------------------------------------
# Development Server Ports
# -----------------------------------------------------------------------------
# Ports to clean when stopping development servers

PORTS := $(DJANGO_PORT) $(MKDOCS_PORT) 3000 8000 8001 8002 8081 9000


# =============================================================================
# Help
# =============================================================================

help: ## Show this help message
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""


# =============================================================================
# Installation
# =============================================================================

install: ## Install all dependencies (Python + Node.js)
	poetry install
	$(NPM) install

install-dev: install ## Install with dev dependencies and pre-commit hooks
	poetry install --with dev
	pre-commit install
	pre-commit install --hook-type commit-msg


# =============================================================================
# Development Servers
# =============================================================================

start: clean-ports ## Start all development servers (Django, Vite, MkDocs)
	$(PYTHON) -m honcho start

stop: clean-ports ## Stop all processes on development ports
	@echo "Development ports cleaned"

clean-ports: ## Kill processes on development ports
	@for port in $(PORTS); do \
		pid=$$(lsof -ti tcp:$$port 2>/dev/null); \
		if [ -n "$$pid" ]; then \
			echo "Killing process on port $$port (PID: $$pid)"; \
			kill -9 $$pid 2>/dev/null || true; \
		fi \
	done


# =============================================================================
# Testing
# =============================================================================

test: ## Run tests with coverage
	$(PYTEST) $(TST_DIR)/

test-fast: ## Run tests without coverage (faster)
	$(PYTEST) $(TST_DIR)/ --no-cov -x

test-verbose: ## Run tests with verbose output
	$(PYTEST) $(TST_DIR)/ -v --no-cov


# =============================================================================
# Code Quality
# =============================================================================

lint: ## Run all linters (Python + JavaScript/CSS)
	$(PYTHON) -m flake8 $(SRC_DIR)/
	$(PYTHON) -m pylint $(SRC_DIR)/ || true
	$(NPM) run lint || true

lint-py: ## Run Python linters only
	$(PYTHON) -m flake8 $(SRC_DIR)/
	$(PYTHON) -m pylint $(SRC_DIR)/ || true

lint-js: ## Run JavaScript/CSS linters only
	$(NPM) run lint

lint-yaml: ## Lint YAML files
	yamllint -c .yamllint.yaml . || true

lint-md: ## Lint Markdown files
	markdownlint '**/*.md' --ignore node_modules --ignore .venv || true

lint-shell: ## Lint shell scripts
	find . -name "*.sh" -not -path "./node_modules/*" -not -path "./.venv/*" -exec shellcheck {} + || true

lint-docker: ## Lint Dockerfiles
	find . -name "Dockerfile*" -not -path "./node_modules/*" -exec hadolint {} + || true

lint-all: lint lint-yaml lint-md lint-shell lint-docker ## Run all linters

format: ## Format all code (Python + JavaScript/CSS)
	$(PYTHON) -m black $(SRC_DIR)/ $(TST_DIR)/ $(EXE_DIR)/
	$(PYTHON) -m isort $(SRC_DIR)/ $(TST_DIR)/ $(EXE_DIR)/
	$(NPM) run format || true

typecheck: ## Run Python type checking (mypy)
	$(PYTHON) -m mypy $(SRC_DIR)/

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files


# =============================================================================
# Documentation
# =============================================================================

docs: ## Serve documentation locally with live reload
	$(PYTHON) -m mkdocs serve

docs-build: ## Build documentation for deployment
	$(PYTHON) -m mkdocs build


# =============================================================================
# Build & Release
# =============================================================================

build: ## Build Python package and frontend assets
	$(NPM) run build
	poetry build

clean: ## Clean all build artifacts and caches
	rm -rf dist/ build/ *.egg-info
	rm -rf htmlcov/ .coverage .coverage.* coverage.xml coverage.json
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf node_modules/.cache/
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Build artifacts cleaned"


# =============================================================================
# Django Management
# =============================================================================

migrate: ## Run Django database migrations
	PYTHONPATH=$(EXE_DIR) $(PYTHON) $(EXE_DIR)/manage.py migrate

makemigrations: ## Create new Django migrations
	PYTHONPATH=$(EXE_DIR) $(PYTHON) $(EXE_DIR)/manage.py makemigrations

shell: ## Open Django interactive shell
	PYTHONPATH=$(EXE_DIR) $(PYTHON) $(EXE_DIR)/manage.py shell

collectstatic: ## Collect static files for deployment
	PYTHONPATH=$(EXE_DIR) $(PYTHON) $(EXE_DIR)/manage.py collectstatic --noinput

runserver: ## Run Django development server only (no Vite/MkDocs)
	PYTHONPATH=$(EXE_DIR) $(PYTHON) $(EXE_DIR)/manage.py runserver


# =============================================================================
# Translations (i18n)
# =============================================================================

translate-make: ## Extract translatable strings from source code
	PYTHONPATH=$(EXE_DIR) $(PYTHON) $(EXE_DIR)/manage.py makemessages -a \
		--ignore=htmlcov \
		--ignore=tst/reports \
		--ignore=node_modules \
		--ignore=.venv \
		--ignore=dist \
		--ignore=build

translate-compile: ## Compile .po files to .mo binary files
	PYTHONPATH=$(EXE_DIR) $(PYTHON) $(EXE_DIR)/manage.py compilemessages

translate-validate: ## Validate translation files for syntax errors
	PYTHONPATH=$(EXE_DIR) $(PYTHON) $(EXE_DIR)/manage.py compilemessages --check

translate-clean: ## Remove compiled translation files (.mo)
	find . -type f -name "*.mo" -delete
	@echo "Compiled translation files removed"
