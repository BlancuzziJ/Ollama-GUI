# 🚀 ShamaOllama - Quick Start Guide

The **easiest way** to get ShamaOllama running on your system!

## For the Impatient (30 seconds)

### Windows Users

1. **Clone/Download** this repository
2. **Double-click** `setup.bat` (installs everything)
3. **Double-click** `run_gui.bat` (starts the app)

### Linux/Mac Users

1. **Clone/Download** this repository
2. **Run** `./run_gui.sh` (handles setup automatically)

That's it! 🎉

---

## What You Need (Prerequisites)

✅ **Ollama installed** - [Get it here](https://ollama.ai/)  
✅ **Python 3.8+** - Most systems have this  
✅ **5 minutes** - Setup is automated

---

## Step-by-Step Instructions

### 🪟 Windows

```cmd
# Method 1: The Easy Way
git clone https://github.com/jblancuzzi/shamollama.git
cd shamollama
setup.bat      # Installs everything + offers desktop shortcut
run_gui.bat    # Starts ShamaOllama
```

```cmd
# Method 2: Manual Setup
git clone https://github.com/jblancuzzi/shamollama.git
cd shamollama
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
create_desktop_shortcut.bat  # Optional: Create desktop shortcut
python main.py
```

### 🐧 Linux

```bash
# Method 1: The Easy Way
git clone https://github.com/jblancuzzi/shamollama.git
cd shamollama
chmod +x run_gui.sh
./run_gui.sh   # Handles everything automatically
chmod +x create_desktop_shortcut.sh
./create_desktop_shortcut.sh  # Optional: Create desktop shortcut
```

```bash
# Method 2: Manual Setup
git clone https://github.com/jblancuzzi/shamollama.git
cd shamollama
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 🍎 macOS

```bash
# Method 1: The Easy Way
git clone https://github.com/jblancuzzi/shamollama.git
cd shamollama
chmod +x run_gui.sh
./run_gui.sh   # Handles everything automatically
chmod +x create_desktop_shortcut_macos.sh
./create_desktop_shortcut_macos.sh  # Optional: Create app bundle
```

```bash
# Method 2: Manual Setup
git clone https://github.com/jblancuzzi/shamollama.git
cd shamollama
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 🔧 Enhanced GPU Detection (Optional)

For **better hardware analysis** and **AI model recommendations**:

```bash
# Windows
install-gpu-support.bat

# Linux/Mac
pip install -r requirements-gpu.txt
```

This adds:

- 🎮 **Detailed GPU information** (VRAM, driver, temperature)
- 🖥️ **System specs** (accurate RAM, CPU frequency)
- 🤖 **Smart model recommendations** based on your hardware
- 📊 **Performance tier classification**

---

## 🖥️ Desktop Shortcuts (Optional)

For **one-click access** to ShamaOllama:

### Windows

```cmd
create_desktop_shortcut.bat    # Creates desktop icon
```

### Linux

```bash
chmod +x create_desktop_shortcut.sh
./create_desktop_shortcut.sh   # Creates desktop entry + applications menu
```

### macOS

```bash
chmod +x create_desktop_shortcut_macos.sh
./create_desktop_shortcut_macos.sh   # Creates app bundle
```

### Universal (Linux/Mac)

```bash
chmod +x create_desktop_shortcut_universal.sh
./create_desktop_shortcut_universal.sh   # Auto-detects platform
```

After creating shortcuts, you can:

- **Double-click** the desktop icon to launch
- **Find ShamaOllama** in your applications menu/Launchpad
- **Pin to taskbar/dock** for even faster access

---

## 🎯 First Time Using?

1. **Start Ollama**: `ollama serve` (in another terminal)
2. **Pull a model**: Use the Models tab in ShamaOllama GUI
3. **Start chatting**: Select model and begin conversation
4. **Explore features**: Try the System tab for hardware info!

---

## 🔥 Pro Tips

- **System Information**: Click "🖥️ System" to see your hardware specs
- **Thinking Models**: Enable "Hide thinking process" in Settings for cleaner responses with DeepSeek
- **GPU Support**: Install optional GPU dependencies for enhanced performance analysis
- **Themes**: Toggle between dark/light themes anytime
- **Keyboard**: Use Ctrl+Enter to send messages quickly

---

## 🆘 Need Help?

- 📖 **Full docs**: [INSTALL.md](INSTALL.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/jblancuzzi/shamollama/issues)
- 💬 **Community**: [Discussions](https://github.com/jblancuzzi/shamollama/discussions)

**Happy AI chatting!** 🎸✨
