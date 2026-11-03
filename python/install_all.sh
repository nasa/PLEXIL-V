#!/bin/bash
# Force a (re)installation for development of all Python packages in this folder.
#
# Package versions are not bumped between changes, so pip would otherwise treat
# the already-installed packages (or cached wheels) as up to date. Run this from
# the Python environment (e.g. an activated virtualenv) you want to install into.

set -e  # Exit on error

cd "$(dirname "$0")"

# Packages in dependency order: a package must come after the local packages it
# depends on. Any other package found in this folder is appended at the end.
ordered_packages="pyplexil-core pyplexil-plexilv plexilv-log plexilv-run plexilv-diff plexilv-cli"

packages=""
for package in $ordered_packages; do
    if [ -f "$package/pyproject.toml" ]; then
        packages="$packages $package"
    fi
done

for pyproject in */pyproject.toml; do
    package="$(dirname "$pyproject")"
    case " $ordered_packages " in
        *" $package "*) ;;
        *) packages="$packages $package" ;;
    esac
done

echo "Installing Python packages in development mode..."
echo "=================================================="

# Upgrade pip first so that editable installs behave the same on every machine.
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Pass 1: install the local packages themselves in editable mode, ignoring
# caches. --no-deps means pip never resolves the sibling packages by name, so
# they cannot be fetched from PyPI by mistake.
for package in $packages; do
    echo ""
    echo "Installing $package..."
    echo "----------------------"
    (cd "$package" && pip install --no-cache-dir --force-reinstall --no-deps -e .)
done

# Pass 2: install the third-party dependencies and the dev extras of all
# packages in a single command, so pip resolves them together instead of
# reporting the dependencies of the packages that are not processed yet. Every
# local sibling is already installed, so its requirement is satisfied and PyPI
# is only queried for third-party packages.
echo ""
echo "Installing third-party dependencies..."
echo "--------------------------------------"
editable_args=()
for package in $packages; do
    editable_args+=(-e "./$package[dev]")
done
pip install --no-cache-dir "${editable_args[@]}"

# Verify: requirements are consistent and each local package is an editable
# install, not a copy from PyPI or a cached wheel.
echo ""
echo "Verifying installation..."
echo "-------------------------"
pip check
python -I - $packages <<'PY'
import json
import sys
from importlib.metadata import distribution

bad = []
for name in sys.argv[1:]:
    direct_url = json.loads(distribution(name).read_text("direct_url.json") or "{}")
    if not direct_url.get("dir_info", {}).get("editable"):
        bad.append(name)
if bad:
    sys.exit("Not installed in editable mode: " + ", ".join(bad))
PY

echo ""
echo "=================================================="
echo "Installed:$packages"
