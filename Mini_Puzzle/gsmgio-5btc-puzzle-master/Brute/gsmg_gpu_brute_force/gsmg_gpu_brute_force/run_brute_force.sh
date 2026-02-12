#!/bin/bash
# Run script for GPU brute force

echo ""
echo "=================================="
echo "GSMG Puzzle GPU Brute Force"
echo "=================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 not found"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if script exists
if [ ! -f "optimized_gpu_brute_force_new.py" ]; then
    echo "❌ Error: optimized_gpu_brute_force_new.py not found"
    echo "Make sure you're in the correct directory"
    exit 1
fi

# Check for dependencies
echo "Checking dependencies..."
python3 -c "import numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  numpy not found - installing..."
    pip3 install --user numpy
fi

python3 -c "import numba" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ numba found - GPU acceleration enabled"
else
    echo "⚠️  numba not found - running in CPU-only mode"
    echo "   For GPU acceleration: pip3 install numba"
fi

echo ""
echo "Starting brute force..."
echo "This will test ~25 million permutations"
echo "Press Ctrl+C to stop"
echo ""

# Run the script
python3 optimized_gpu_brute_force_new.py

echo ""
echo "=================================="
echo "Brute force complete"
echo "=================================="
