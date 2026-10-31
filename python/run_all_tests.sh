#!/bin/bash
# Run the tests of all Python packages in this folder.
#
# Every package with a pyproject.toml and a tests/ directory is tested. All
# packages are run even if one fails, and the exit code is non-zero if any did.

cd "$(dirname "$0")"

echo "Running tests for all Python packages..."
echo "=========================================="

output_file="$(mktemp)"
trap 'rm -f "$output_file"' EXIT

total_passed=0
failed_packages=""

for pyproject in */pyproject.toml; do
    package="$(dirname "$pyproject")"
    [ -d "$package/tests" ] || continue

    echo ""
    echo "Testing $package..."
    echo "-------------------"

    (cd "$package" && pytest tests/ --tb=short) 2>&1 | tee "$output_file"
    if [ "${PIPESTATUS[0]}" -ne 0 ]; then
        echo "FAILED: Tests in $package failed"
        failed_packages="$failed_packages $package"
    else
        passed=$(grep -Eo "[0-9]+ passed" "$output_file" | tail -1 | awk '{print $1}')
        total_passed=$((total_passed + ${passed:-0}))
    fi
done

echo ""
echo "=========================================="
if [ -n "$failed_packages" ]; then
    echo "Tests failed in:$failed_packages"
    exit 1
fi
echo "All tests passed! Total: $total_passed tests"
