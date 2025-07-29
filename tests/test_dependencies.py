#!/usr/bin/env python3
"""
Simple test for GPU dependencies
"""

import sys
from pathlib import Path

# Add parent directory to path to find main modules
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Testing GPU Dependencies...")
print("=" * 40)

# Test psutil
try:
    import psutil

    print("✅ psutil: OK")
    print(f"   RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    print(f"   CPU cores: {psutil.cpu_count()}")
    if hasattr(psutil, "cpu_freq"):
        freq = psutil.cpu_freq()
        if freq:
            print(f"   CPU frequency: {freq.current:.0f} MHz")
except Exception as e:
    print(f"❌ psutil: {e}")

print()

# Test GPUtil
try:
    import GPUtil

    print("✅ GPUtil: OK")
    gpus = GPUtil.getGPUs()
    if gpus:
        for i, gpu in enumerate(gpus):
            print(f"   GPU {i+1}: {gpu.name}")
            print(f"   VRAM: {gpu.memoryTotal:.0f} MB")
            print(f"   Driver: {gpu.driver}")
    else:
        print("   No NVIDIA GPUs detected")
except Exception as e:
    print(f"❌ GPUtil: {e}")

print()
print("Testing our GPU detection module...")
try:
    from gpu_info import get_gpu_info, check_gpu_dependencies

    deps = check_gpu_dependencies()
    print(f"Dependencies: {deps}")

    gpu_info = get_gpu_info()
    print(f"Summary: {gpu_info.get_summary()}")

    recommendations = gpu_info.get_ai_recommendations()
    print(f"Performance Tier: {recommendations['performance_tier']}")

except Exception as e:
    print(f"❌ GPU module error: {e}")
    import traceback

    traceback.print_exc()
