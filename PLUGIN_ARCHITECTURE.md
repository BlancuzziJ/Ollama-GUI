# GPU Detection Architecture

## Overview

ShamaOllama implements a plugin-like architecture for GPU detection that gracefully handles optional dependencies. This approach keeps the core application lightweight while providing enhanced features when additional packages are available.

## Architecture Design

### Core Principles

1. **Zero Required Dependencies**: Basic GPU detection works without any optional packages
2. **Graceful Degradation**: Enhanced features are available when dependencies are installed
3. **Clear User Guidance**: Users are informed about available enhancements
4. **Easy Installation**: Simple scripts to install optional features

### Dependency Layers

#### Layer 1: Basic Detection (Always Available)

- Uses built-in Python libraries and system commands
- Provides basic GPU identification
- Works on Windows, macOS, and Linux
- Offers fundamental AI model recommendations

#### Layer 2: Enhanced Detection (Optional)

- **GPUtil**: Detailed NVIDIA GPU information (VRAM usage, temperature, load)
- **psutil**: Accurate system RAM, CPU frequency, and process information
- Enhanced AI model recommendations based on precise hardware specs

## Implementation Details

### Import Strategy

```python
# Type hints for IDE support without runtime errors
if TYPE_CHECKING:
    import GPUtil
    import psutil

# Safe runtime imports with fallbacks
try:
    import GPUtil
    GPU_UTIL_AVAILABLE = True
except ImportError:
    GPUtil = None
    GPU_UTIL_AVAILABLE = False
```

### Detection Fallbacks

1. **GPU Detection**:

   - Primary: GPUtil for NVIDIA GPUs
   - Fallback: Platform-specific commands (wmic, system_profiler, lspci)
   - Ultimate: Generic "Integrated Graphics" detection

2. **System Information**:
   - Primary: psutil for detailed system specs
   - Fallback: Basic OS commands for RAM and CPU count
   - Ultimate: "Unknown" with installation guidance

### User Experience

#### Without Optional Dependencies

- Basic GPU detection works
- Provides general AI model recommendations
- Shows installation guidance for enhanced features
- No errors or crashes

#### With Optional Dependencies

- Detailed hardware analysis
- Precise VRAM usage monitoring
- Temperature and load information
- Specific AI model recommendations based on exact specs

## Installation Options

### Core Only (Minimal)

```bash
pip install -r requirements.txt
```

### With GPU Detection

```bash
pip install -r requirements.txt
pip install -r requirements-gpu.txt
```

### Convenience Scripts

- Windows: `install-gpu-support.bat`
- PowerShell: `install-gpu-support.ps1`
- Linux/macOS: `install-gpu-support.sh`

## Benefits

1. **Minimal Bloat**: Users only install what they need
2. **Future Plugin System**: Architecture supports additional optional features
3. **Better Performance**: Fewer dependencies mean faster startup
4. **Wider Compatibility**: Works on systems where enhanced packages might not be available
5. **Clear Upgrade Path**: Users can easily add features as needed

## Future Extensions

This architecture makes it easy to add other optional features:

- **Database Support**: Optional SQLite/PostgreSQL for conversation history
- **Advanced Logging**: Optional structured logging with external services
- **Cloud Integration**: Optional cloud storage for model synchronization
- **Advanced UI**: Optional rich widgets for enhanced interface

Each feature can be implemented as an optional dependency with graceful fallbacks.
