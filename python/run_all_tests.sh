#!/bin/bash
# Run all tests across Python packages

set -e  # Exit on error

cd "$(dirname "$0")"

echo "Running tests for all Python packages..."
echo "=========================================="

total_passed=0
total_failed=0

for package in pyplexil-core pyplexil-plexilv plexilv-cli plexilv-run plexilv-diff; do
    if [ -d "$package/tests" ]; then
        echo ""
        echo "Testing $package..."
        echo "-------------------"

        # Run tests and capture results
        if pytest "$package/tests/" --tb=short; then
            passed=$(pytest "$package/tests/" -q 2>&1 | grep -E "^[0-9]+ passed" | awk '{print $1}' || echo "0")
            total_passed=$((total_passed + passed))
        else
            echo "FAILED: Tests in $package failed"
            exit 1
        fi
    fi
done

echo ""
echo "=========================================="
echo "All tests passed! Total: $total_passed tests"
