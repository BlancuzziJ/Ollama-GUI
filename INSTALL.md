# 🎸 ShamaOllama Installation Guide

This guide provides detailed installation instructions for ShamaOllama on different platforms.

_Paying homage to "Shama Lama Ding Dong" from Animal House (1978) - let's get this rockin' AI interface up and running!_

## Table of Contents

- [Prerequisites](#prerequisites)
- [Windows Installation](#windows-installation)
- [Linux Installation](#linux-installation)
- [macOS Installation](#macos-installation)
- [Docker Installation](#docker-installation)
- [Development Installation](#development-installation)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Python 3.8 or higher**
- **Ollama installed and running**
- **4GB RAM minimum** (8GB recommended)
- **50MB free disk space**

### Ollama Installation

Before installing Ollama GUI, ensure Ollama is installed:

#### Windows

```bash
# Download from https://ollama.ai/download/windows
# Or using winget
winget install Ollama.Ollama
```

#### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS

```bash
# Download from https://ollama.ai/download/mac
# Or using Homebrew
brew install ollama
```

## Windows Installation

### Method 1: Simple Installation (Recommended)

1. **Download the latest release** from [GitHub Releases](https://github.com/jblancuzzi/ollama-gui/releases)

2. **Extract the ZIP file** to your desired location

3. **Run the setup script**:

   ```cmd
   setup.bat
   ```

4. **Launch the application**:
   ```cmd
   run_gui.bat
   ```

### Method 2: Manual Installation

1. **Clone the repository**:

   ```cmd
   git clone https://github.com/jblancuzzi/ollama-gui.git
   cd ollama-gui
   ```

2. **Create virtual environment**:

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```cmd
   python main.py
   ```

### Method 3: PowerShell Installation

1. **Open PowerShell as Administrator**

2. **Set execution policy** (if needed):

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Run the PowerShell launcher**:
   ```powershell
   .\run_gui.ps1
   ```

## Linux Installation

### Ubuntu/Debian

1. **Install dependencies**:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git
   ```

2. **Clone repository**:

   ```bash
   git clone https://github.com/jblancuzzi/ollama-gui.git
   cd ollama-gui
   ```

3. **Create virtual environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Make launcher executable**:

   ```bash
   chmod +x run_gui.sh
   ```

6. **Run the application**:
   ```bash
   ./run_gui.sh
   ```

### Arch Linux

1. **Install dependencies**:

   ```bash
   sudo pacman -S python python-pip git
   ```

2. **Follow steps 2-6** from Ubuntu installation

### Fedora/RHEL/CentOS

1. **Install dependencies**:

   ```bash
   sudo dnf install python3 python3-pip git
   # or for older versions:
   sudo yum install python3 python3-pip git
   ```

2. **Follow steps 2-6** from Ubuntu installation

## macOS Installation

### Method 1: Using Homebrew (Recommended)

1. **Install Homebrew** (if not installed):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install dependencies**:

   ```bash
   brew install python git
   ```

3. **Clone repository**:

   ```bash
   git clone https://github.com/jblancuzzi/ollama-gui.git
   cd ollama-gui
   ```

4. **Create virtual environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```bash
   python main.py
   ```

### Method 2: Manual Installation

1. **Install Python** from [python.org](https://www.python.org/downloads/mac-osx/)

2. **Follow steps 3-6** from Homebrew method

## Docker Installation

### Using Docker Compose (Recommended)

1. **Create docker-compose.yml**:

   ```yaml
   version: "3.8"
   services:
     ollama-gui:
       image: jblancuzzi/ollama-gui:latest
       ports:
         - "8080:8080"
       environment:
         - OLLAMA_URL=http://ollama:11434
       depends_on:
         - ollama

     ollama:
       image: ollama/ollama:latest
       ports:
         - "11434:11434"
       volumes:
         - ollama_data:/root/.ollama

   volumes:
     ollama_data:
   ```

2. **Run the containers**:

   ```bash
   docker-compose up -d
   ```

3. **Access the GUI** at http://localhost:8080

### Using Docker Run

```bash
# Run Ollama
docker run -d --name ollama -p 11434:11434 -v ollama_data:/root/.ollama ollama/ollama

# Run Ollama GUI
docker run -d --name ollama-gui -p 8080:8080 -e OLLAMA_URL=http://ollama:11434 --link ollama jblancuzzi/ollama-gui
```

## Development Installation

For contributors and developers:

1. **Fork the repository** on GitHub

2. **Clone your fork**:

   ```bash
   git clone https://github.com/YOUR_USERNAME/ollama-gui.git
   cd ollama-gui
   ```

3. **Set up development environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

4. **Install development dependencies**:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

5. **Install pre-commit hooks**:

   ```bash
   pre-commit install
   ```

6. **Run tests**:
   ```bash
   python -m pytest
   ```

## Troubleshooting

### Common Issues

#### "Command not found: python"

**Solution**: Install Python or use `python3` instead of `python`

#### "Permission denied" on Linux/Mac

**Solution**: Make the script executable:

```bash
chmod +x run_gui.sh
```

#### "Cannot connect to Ollama"

**Solutions**:

1. Start Ollama: `ollama serve`
2. Check Ollama is running: `curl http://localhost:11434/api/version`
3. Verify URL in settings

#### "ModuleNotFoundError: No module named 'customtkinter'"

**Solution**: Activate virtual environment and install dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

#### Windows: "Scripts\activate.bat is not digitally signed"

**Solution**: Set execution policy:

```cmd
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Performance Issues

#### Slow startup

- Check Ollama connection
- Reduce model list refresh frequency
- Close other applications

#### High memory usage

- Limit chat history size in settings
- Use smaller models
- Restart application periodically

### Platform-Specific Issues

#### Linux: Tkinter not found

```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install tkinter

# Arch
sudo pacman -S tk
```

#### macOS: SSL certificate errors

```bash
# Update certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Getting Help

If you encounter issues not covered here:

1. **Check [GitHub Issues](https://github.com/jblancuzzi/ollama-gui/issues)**
2. **Review [Troubleshooting](README.md#troubleshooting)** in README
3. **Create a new issue** with:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce

## Next Steps

After installation:

1. **Start Ollama**: `ollama serve` (for local installation)
2. **Pull a model**: Use the Models panel or `ollama pull llama2`
3. **Start chatting**: Select a model and begin your conversation
4. **Explore features**: Try different themes, export chats, manage models

### 🌐 Connecting to Remote Ollama (Optional)

If you want to connect to a remote Ollama instance instead of running locally:

1. **Open ShamaOllama** and go to the Settings panel
2. **Update Ollama URL** to your remote server:
   - Local network: `http://192.168.1.100:11434`
   - Cloud server: `https://ollama.yourcompany.com`
   - Docker container: `http://ollama-container:11434`
3. **Test the connection** to verify connectivity
4. **Save settings** and start using remote models

**Benefits of Remote Setup:**

- 🚀 **Powerful Hardware** - Use high-end servers for model inference
- 👥 **Team Sharing** - Multiple users accessing the same models
- ☁️ **Cloud Flexibility** - Deploy anywhere with proper infrastructure
- 🔄 **Resource Efficiency** - Centralized model management

Enjoy using ShamaOllama! 🚀
