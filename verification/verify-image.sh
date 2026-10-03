#!/usr/bin/env bash

FAILED=0

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo "[PASS] $1"
    else
        echo "[FAIL] $1"
        FAILED=$((FAILED + 1))
    fi
}

check_python_module() {
    if tabbypy3 -c "import $1" >/dev/null 2>&1; then
        echo "[PASS] Python module: $1"
    else
        echo "[FAIL] Python module: $1"
        FAILED=$((FAILED + 1))
    fi
}

check_verilator() {
    if ! command -v verilator >/dev/null 2>&1; then
        echo "[FAIL] Verilator not found"
        FAILED=$((FAILED + 1))
        return
    fi

    local version
    version=$(verilator --version | awk '{print $2}')

    if dpkg --compare-versions "$version" ge "5.036"; then
        echo "[PASS] Verilator $version"
    else
        echo "[FAIL] Verilator $version (requires >= 5.036)"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== Docker Image Verification ==="

# Python
check_command python3

# Python modules
check_python_module cocotb

# Waveform viewers
check_command surfer

# RTL simulation
check_verilator

echo "================================="

if [ "$FAILED" -eq 0 ]; then
    echo "All checks passed!"
    exit 0
else
    echo "$FAILED check(s) failed."
    exit 1
fi
