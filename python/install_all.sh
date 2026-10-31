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

# Pass 1: install the third-party dependencies and the dev extras. This also
# replaces the local sibling packages (declared as `file:` dependencies) with
# non-editable copies in site-packages, which pass 2 must undo.
for package in $packages; do
    echo ""
    echo "Installing dependencies of $package..."
    echo "--------------------------------------"
    (cd "$package" && pip install --no-cache-dir -e ".[dev]")
done

# Pass 2: force-reinstall the local packages themselves in editable mode,
# ignoring caches. This must run last so the editable installs win, and
# --no-deps keeps pip from touching the dependencies installed above.
for package in $packages; do
    echo ""
    echo "Reinstalling $package..."
    echo "------------------------"
    (cd "$package" && pip install --no-cache-dir --force-reinstall --no-deps -e .)
done

echo ""
echo "=================================================="
echo "Installed:$packages"
