#!/bin/bash
# Setup script for GPU brute force

echo "=================================="
echo "GSMG Puzzle GPU Brute Force Setup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check for GPU
echo ""
echo "Checking for NVIDIA GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
    HAS_GPU=1
else
    echo "⚠️  No NVIDIA GPU detected - will run in CPU-only mode"
    HAS_GPU=0
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
if [ $HAS_GPU -eq 1 ]; then
    echo "Installing numba for GPU acceleration..."
    pip3 install --user numba numpy 2>&1 | tail -5
else
    echo "Installing basic dependencies..."
    pip3 install --user numpy 2>&1 | tail -5
fi

echo ""
echo "=================================="
echo "✓ Setup Complete!"
echo "=================================="
echo ""
echo "To run the brute force:"
echo "  python3 optimized_gpu_brute_force_new.py"
echo ""
