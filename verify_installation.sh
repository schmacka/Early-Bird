#!/bin/bash
# Early Bird Installation Verification Script
# Run this to verify all required files are present

echo "========================================"
echo "Early Bird Installation Verification"
echo "========================================"
echo ""

ERRORS=0
WARNINGS=0

check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "✗ MISSING: $1"
        ((ERRORS++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
    else
        echo "✗ MISSING: $1/"
        ((ERRORS++))
    fi
}

echo "Checking core addon files..."
check_file "early_bird/config.json"
check_file "early_bird/Dockerfile"
check_file "early_bird/build.json"
check_file "early_bird/requirements.txt"
check_file "early_bird/run.py"
check_file "early_bird/sensor.py"
check_file "early_bird/apparmor.txt"

echo ""
echo "Checking documentation..."
check_file "early_bird/README.md"
check_file "early_bird/DOCS.md"
check_file "README.md"
check_file "CHANGELOG.md"

echo ""
echo "Checking directories..."
check_dir "early_bird/templates"
check_dir "early_bird/translations"
check_dir "early_bird/data"
check_dir "early_bird/www"

echo ""
echo "Checking templates..."
check_file "early_bird/templates/index.html"
check_file "early_bird/templates/setup.html"

echo ""
echo "Checking translations..."
check_file "early_bird/translations/de.json"
check_file "early_bird/translations/en.json"

echo ""
echo "Checking Python syntax..."
python3 -m py_compile early_bird/sensor.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ sensor.py syntax OK"
else
    echo "✗ sensor.py has syntax errors"
    ((ERRORS++))
fi

python3 -m py_compile early_bird/run.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ run.py syntax OK"
else
    echo "✗ run.py has syntax errors"
    ((ERRORS++))
fi

echo ""
echo "Checking JSON validity..."
python3 -c "import json; json.load(open('early_bird/config.json'))" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ config.json valid"
else
    echo "✗ config.json invalid"
    ((ERRORS++))
fi

python3 -c "import json; json.load(open('early_bird/translations/de.json'))" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ de.json valid"
else
    echo "✗ de.json invalid"
    ((ERRORS++))
fi

python3 -c "import json; json.load(open('early_bird/translations/en.json'))" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ en.json valid"
else
    echo "✗ en.json invalid"
    ((ERRORS++))
fi

echo ""
echo "========================================"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✓ All checks passed!"
    echo "Installation is complete and valid."
elif [ $ERRORS -eq 0 ]; then
    echo "⚠ Installation complete with $WARNINGS warning(s)"
else
    echo "✗ Installation incomplete: $ERRORS error(s), $WARNINGS warning(s)"
    exit 1
fi
echo "========================================"
