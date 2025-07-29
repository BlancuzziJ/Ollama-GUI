"""
GPU Information and Recommendations for ShamaOllama
Helps users understand their hardware capabilities for local AI
"""

import platform
import subprocess
import json
import logging
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

# Optional dependencies for enhanced GPU detection
# These imports are wrapped in try/except to prevent errors when packages aren't installed
GPU_UTIL_AVAILABLE = False
PSUTIL_AVAILABLE = False

if TYPE_CHECKING:
    # Type hints only - won't cause runtime import errors
    import GPUtil  # type: ignore
    import psutil  # type: ignore

try:
    import GPUtil  # type: ignore  # Optional dependency

    GPU_UTIL_AVAILABLE = True
except ImportError:
    # GPUtil not installed - enhanced NVIDIA GPU detection not available
    GPUtil = None  # type: ignore

try:
    import psutil  # type: ignore  # Optional dependency

    PSUTIL_AVAILABLE = True
except ImportError:
    # psutil not installed - enhanced system info detection not available
    psutil = None  # type: ignore


class GPUInfo:
    """GPU information and AI suitability analysis"""

    def __init__(self):
        self.gpu_data = []
        self.system_ram = 0
        self.cpu_info = ""
        self._detect_hardware()

    def _detect_hardware(self):
        """Detect system hardware"""
        if not GPU_UTIL_AVAILABLE and not PSUTIL_AVAILABLE:
            logging.info(
                "GPU detection libraries not installed. Using basic detection."
            )
        self._detect_gpus()
        self._detect_system_info()

    def _detect_gpus(self):
        """Detect available GPUs"""
        self.gpu_data = []

        # Try GPUtil first (NVIDIA GPUs)
        if GPU_UTIL_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    gpu_info = {
                        "name": gpu.name,
                        "memory_total": gpu.memoryTotal,
                        "memory_used": gpu.memoryUsed,
                        "memory_free": gpu.memoryFree,
                        "driver": gpu.driver,
                        "uuid": gpu.uuid,
                        "vendor": "NVIDIA",
                        "temperature": getattr(gpu, "temperature", None),
                        "load": getattr(gpu, "load", None),
                    }
                    self.gpu_data.append(gpu_info)
            except Exception as e:
                logging.debug(f"GPUtil detection failed: {e}")
                # Falling back to platform detection

        # Try platform-specific detection for other GPUs
        self._detect_platform_gpus()

        # If no GPUs detected, note integrated graphics
        if not self.gpu_data:
            fallback_note = "Basic detection mode"
            if not GPU_UTIL_AVAILABLE:
                fallback_note += (
                    " - Install requirements-gpu.txt for enhanced detection"
                )

            self.gpu_data.append(
                {
                    "name": "Integrated/Unknown Graphics",
                    "memory_total": 0,
                    "memory_used": 0,
                    "memory_free": 0,
                    "driver": "Unknown",
                    "vendor": "Integrated",
                    "note": fallback_note,
                }
            )

    def _detect_platform_gpus(self):
        """Platform-specific GPU detection"""
        system = platform.system()

        if system == "Windows":
            self._detect_windows_gpus()
        elif system == "Darwin":  # macOS
            self._detect_macos_gpus()
        elif system == "Linux":
            self._detect_linux_gpus()

    def _detect_windows_gpus(self):
        """Detect GPUs on Windows using WMI"""
        try:
            result = subprocess.run(
                [
                    "wmic",
                    "path",
                    "win32_VideoController",
                    "get",
                    "Name,AdapterRAM,DriverVersion",
                    "/format:csv",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        parts = line.split(",")
                        if len(parts) >= 4:
                            try:
                                ram_bytes = int(parts[1]) if parts[1].isdigit() else 0
                                ram_mb = (
                                    ram_bytes / (1024 * 1024) if ram_bytes > 0 else 0
                                )

                                # Skip if already detected by GPUtil
                                gpu_name = parts[3].strip()
                                if not any(
                                    gpu["name"] == gpu_name for gpu in self.gpu_data
                                ):
                                    self.gpu_data.append(
                                        {
                                            "name": gpu_name,
                                            "memory_total": ram_mb,
                                            "memory_used": 0,
                                            "memory_free": ram_mb,
                                            "driver": parts[2].strip(),
                                            "vendor": self._guess_vendor(gpu_name),
                                        }
                                    )
                            except (ValueError, IndexError):
                                continue
        except Exception as e:
            logging.debug(f"Windows GPU detection failed: {e}")
            # Silently fall back to basic detection

    def _detect_macos_gpus(self):
        """Detect GPUs on macOS"""
        try:
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType", "-json"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                displays = data.get("SPDisplaysDataType", [])

                for display in displays:
                    name = display.get("sppci_model", "Unknown GPU")
                    vram = display.get("spdisplays_vram", "0 MB")

                    # Parse VRAM
                    vram_mb = 0
                    if "MB" in vram:
                        vram_mb = int(vram.replace(" MB", "").replace(",", ""))
                    elif "GB" in vram:
                        vram_mb = int(
                            float(vram.replace(" GB", "").replace(",", "")) * 1024
                        )

                    self.gpu_data.append(
                        {
                            "name": name,
                            "memory_total": vram_mb,
                            "memory_used": 0,
                            "memory_free": vram_mb,
                            "driver": "macOS Built-in",
                            "vendor": self._guess_vendor(name),
                        }
                    )
        except Exception as e:
            logging.debug(f"macOS GPU detection failed: {e}")
            # Silently fall back to basic detection

    def _detect_linux_gpus(self):
        """Detect GPUs on Linux"""
        # Try nvidia-smi for NVIDIA GPUs
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=name,memory.total,driver_version",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 3:
                        self.gpu_data.append(
                            {
                                "name": parts[0],
                                "memory_total": int(parts[1]),
                                "memory_used": 0,
                                "memory_free": int(parts[1]),
                                "driver": parts[2],
                                "vendor": "NVIDIA",
                            }
                        )
        except Exception:
            pass

        # Try lspci for other GPUs
        try:
            result = subprocess.run(
                ["lspci", "-v"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                lines = result.stdout.split("\n")
                for line in lines:
                    if (
                        "VGA compatible controller" in line
                        or "Display controller" in line
                    ):
                        name = (
                            line.split(": ", 1)[-1] if ": " in line else "Unknown GPU"
                        )
                        if not any(gpu["name"] == name for gpu in self.gpu_data):
                            self.gpu_data.append(
                                {
                                    "name": name,
                                    "memory_total": 0,
                                    "memory_used": 0,
                                    "memory_free": 0,
                                    "driver": "Unknown",
                                    "vendor": self._guess_vendor(name),
                                }
                            )
        except Exception:
            pass

    def _detect_system_info(self):
        """Detect system RAM and CPU info"""
        if PSUTIL_AVAILABLE:
            try:
                # System RAM in GB
                self.system_ram = psutil.virtual_memory().total / (1024**3)

                # CPU info
                self.cpu_info = f"{psutil.cpu_count()} cores"
                if hasattr(psutil, "cpu_freq"):
                    freq = psutil.cpu_freq()
                    if freq:
                        self.cpu_info += f" @ {freq.current:.1f}GHz"
            except Exception as e:
                logging.debug(f"System info detection failed: {e}")
                self.system_ram = 0
                self.cpu_info = "Unknown"
        else:
            # Basic fallback detection without psutil
            try:
                # Try to get basic RAM info on Windows
                if platform.system() == "Windows":
                    result = subprocess.run(
                        [
                            "wmic",
                            "computersystem",
                            "get",
                            "TotalPhysicalMemory",
                            "/format:csv",
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )

                    if result.returncode == 0:
                        lines = result.stdout.strip().split("\n")[1:]  # Skip header
                        for line in lines:
                            if line.strip():
                                parts = line.split(",")
                                if len(parts) >= 2 and parts[1].isdigit():
                                    self.system_ram = int(parts[1]) / (1024**3)
                                    break

                # Basic CPU count
                import os

                self.cpu_info = f"{os.cpu_count()} cores (detected)"

            except Exception as e:
                logging.debug(f"Fallback system detection failed: {e}")
                self.system_ram = 0
                self.cpu_info = (
                    "Unknown - Install requirements-gpu.txt for detailed info"
                )

    def _guess_vendor(self, gpu_name: str) -> str:
        """Guess GPU vendor from name"""
        name_lower = gpu_name.lower()
        if (
            "nvidia" in name_lower
            or "geforce" in name_lower
            or "quadro" in name_lower
            or "tesla" in name_lower
        ):
            return "NVIDIA"
        elif "amd" in name_lower or "radeon" in name_lower or "rx " in name_lower:
            return "AMD"
        elif "intel" in name_lower or "iris" in name_lower or "uhd" in name_lower:
            return "Intel"
        elif (
            "apple" in name_lower
            or "m1" in name_lower
            or "m2" in name_lower
            or "m3" in name_lower
        ):
            return "Apple"
        else:
            return "Unknown"

    def get_ai_recommendations(self) -> Dict:
        """Get AI model recommendations based on hardware"""
        recommendations = {
            "suitable_models": [],
            "performance_tier": "Unknown",
            "limitations": [],
            "upgrades": [],
        }

        # Determine best GPU
        best_gpu = None
        max_vram = 0

        for gpu in self.gpu_data:
            vram = gpu.get("memory_total", 0)
            if vram > max_vram:
                max_vram = vram
                best_gpu = gpu

        # Performance tiers based on VRAM
        if max_vram >= 16000:  # 16GB+
            recommendations["performance_tier"] = "High-End (16GB+ VRAM)"
            recommendations["suitable_models"] = [
                "Large models (13B-70B parameters)",
                "llama2:13b, llama2:70b",
                "codellama:13b, codellama:34b",
                "mistral:7b with room for multiple models",
            ]
        elif max_vram >= 8000:  # 8GB+
            recommendations["performance_tier"] = "Mid-Range (8GB+ VRAM)"
            recommendations["suitable_models"] = [
                "Medium models (7B-13B parameters)",
                "llama2:7b, llama2:13b",
                "codellama:7b, codellama:13b",
                "mistral:7b",
            ]
        elif max_vram >= 4000:  # 4GB+
            recommendations["performance_tier"] = "Entry-Level (4GB+ VRAM)"
            recommendations["suitable_models"] = [
                "Small models (3B-7B parameters)",
                "llama2:7b (may be slow)",
                "mistral:7b (may be slow)",
                "phi-2, tinyllama",
            ]
            recommendations["limitations"] = [
                "Large models may run slowly or not at all",
                "Consider using quantized models",
            ]
        elif max_vram >= 2000:  # 2GB+
            recommendations["performance_tier"] = "Limited (2GB+ VRAM)"
            recommendations["suitable_models"] = [
                "Very small models only",
                "tinyllama",
                "phi-2 (may be slow)",
            ]
            recommendations["limitations"] = [
                "Very limited model selection",
                "Slow performance expected",
                "Consider CPU-only mode",
            ]
        else:
            recommendations["performance_tier"] = "CPU-Only / Integrated Graphics"
            recommendations["suitable_models"] = [
                "Small models in CPU mode",
                "tinyllama (CPU)",
                "Consider remote Ollama server",
            ]
            recommendations["limitations"] = [
                "GPU acceleration not available",
                "Very slow performance",
                "Large models not recommended",
            ]
            recommendations["upgrades"] = [
                "Add dedicated GPU with 8GB+ VRAM",
                "Consider RTX 3070, RTX 4060 Ti, or better",
                "AMD RX 6800 XT or better",
            ]

        # RAM recommendations
        if self.system_ram < 16:
            recommendations["limitations"].append(
                f"System RAM: {self.system_ram:.1f}GB (16GB+ recommended)"
            )
            if self.system_ram < 8:
                recommendations["upgrades"].append("Upgrade to 16GB+ system RAM")

        return recommendations

    def get_summary(self) -> str:
        """Get a human-readable summary"""
        if not self.gpu_data:
            return "No GPU information available"

        summary = []

        # Primary GPU
        if self.gpu_data:
            primary = self.gpu_data[0]
            vram = primary.get("memory_total", 0)
            if vram > 0:
                summary.append(f"Primary GPU: {primary['name']} ({vram:.0f}MB VRAM)")
            else:
                summary.append(f"Primary GPU: {primary['name']}")

        # System info
        if self.system_ram > 0:
            summary.append(f"System RAM: {self.system_ram:.1f}GB")

        if self.cpu_info:
            summary.append(f"CPU: {self.cpu_info}")

        return " | ".join(summary)


def get_gpu_info() -> GPUInfo:
    """Get GPU information for the current system"""
    return GPUInfo()


def check_gpu_dependencies() -> Dict[str, bool]:
    """Check which GPU detection dependencies are available"""
    return {
        "GPUtil": GPU_UTIL_AVAILABLE,
        "psutil": PSUTIL_AVAILABLE,
        "basic_detection": True,
    }


def get_dependency_install_message() -> str:
    """Get message about installing GPU dependencies"""
    missing = []
    if not GPU_UTIL_AVAILABLE:
        missing.append("GPUtil")
    if not PSUTIL_AVAILABLE:
        missing.append("psutil")

    if missing:
        return (
            f"Enhanced GPU detection not available. Missing: {', '.join(missing)}\n\n"
            "For detailed hardware analysis, install with:\n"
            "pip install -r requirements-gpu.txt\n\n"
            "This provides:\n"
            "• Detailed GPU memory information\n"
            "• Accurate system RAM detection\n"
            "• CPU frequency information\n"
            "• Enhanced AI model recommendations"
        )
    else:
        return "All GPU detection dependencies are available!"


def format_gpu_info_for_display(gpu_info: GPUInfo) -> str:
    """Format GPU info for display in the GUI"""
    lines = []

    lines.append("🖥️ SYSTEM HARDWARE INFORMATION")
    lines.append("=" * 50)

    # Show dependency status
    deps = check_gpu_dependencies()
    if not all([deps["GPUtil"], deps["psutil"]]):
        lines.append("⚠️ Enhanced detection requires optional dependencies")
        lines.append("   Run: pip install -r requirements-gpu.txt")
        lines.append("")

    # GPU Information
    if gpu_info.gpu_data:
        lines.append("🎮 Graphics Cards:")
        for i, gpu in enumerate(gpu_info.gpu_data, 1):
            name = gpu["name"]
            vram = gpu.get("memory_total", 0)
            vendor = gpu.get("vendor", "Unknown")

            lines.append(f"  {i}. {name}")
            lines.append(f"     Vendor: {vendor}")
            if vram > 0:
                lines.append(f"     VRAM: {vram:.0f} MB ({vram/1024:.1f} GB)")
            else:
                lines.append(f"     VRAM: Unknown")

            driver = gpu.get("driver", "Unknown")
            if driver != "Unknown":
                lines.append(f"     Driver: {driver}")
            lines.append("")

    # System Info
    lines.append("💾 System Information:")
    if gpu_info.system_ram > 0:
        lines.append(f"  RAM: {gpu_info.system_ram:.1f} GB")
    if gpu_info.cpu_info:
        lines.append(f"  CPU: {gpu_info.cpu_info}")

    lines.append("")

    # AI Recommendations
    recommendations = gpu_info.get_ai_recommendations()
    lines.append("🤖 AI MODEL RECOMMENDATIONS")
    lines.append("=" * 50)
    lines.append(f"Performance Tier: {recommendations['performance_tier']}")
    lines.append("")

    if recommendations["suitable_models"]:
        lines.append("✅ Recommended Models:")
        for model in recommendations["suitable_models"]:
            lines.append(f"  • {model}")
        lines.append("")

    if recommendations["limitations"]:
        lines.append("⚠️ Limitations:")
        for limitation in recommendations["limitations"]:
            lines.append(f"  • {limitation}")
        lines.append("")

    if recommendations["upgrades"]:
        lines.append("🚀 Suggested Upgrades:")
        for upgrade in recommendations["upgrades"]:
            lines.append(f"  • {upgrade}")
        lines.append("")

    lines.append("💡 Tips:")
    lines.append("  • For remote Ollama, hardware requirements are minimal")
    lines.append("  • Quantized models use less VRAM but may reduce quality")
    lines.append("  • CPU-only mode works but is much slower")

    return "\n".join(lines)
