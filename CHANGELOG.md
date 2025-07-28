# Changel## [1.0.0] - 2025-07-28

### 🧠 Added - Thinking Models Support

- **NEW**: Added support for thinking models like DeepSeek
- **NEW**: "Hide thinking/reasoning process" setting in Settings panel
- **NEW**: Automatic filtering of thinking blocks (`<thinking>`, `[thinking]`, etc.)
- **NEW**: Information dialog explaining the thinking models feature
- **NEW**: Test script (`test_thinking_filter.py`) to demonstrate filtering
- Improved user experience with cleaner, more concise responses from thinking models

### 🎸 Rebranded

All notable changes to ShamaOllama will be documented in this file.

_Paying homage to "Shama Lama Ding Dong" from Animal House (1978)_

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-28

### 🎸 Rebranded

- **BREAKING**: Renamed from "Ollama GUI" to "ShamaOllama"
- Added homage to "Shama Lama Ding Dong" from Animal House (1978)
- Updated all branding, documentation, and file references
- Changed data directory from `.ollama_gui` to `.shamollama`
- Updated author information (John Blancuzzi, john@blancuzzi.org)

## [1.0.0] - 2025-07-28

### Added

- **Initial release** of Ollama GUI
- **Modern CustomTkinter interface** with dark/light theme support
- **Real-time streaming responses** with live text generation
- **Animated typing indicators** and visual feedback system
- **Professional model management** with pull/delete functionality
- **Chat history management** with persistent storage
- **Session export functionality** (JSON and text formats)
- **Settings panel** with configurable Ollama URL
- **Connection status monitoring** with automatic health checks
- **Modular architecture** for easy extension
- **Comprehensive error handling** with fallback mechanisms
- **Keyboard shortcuts** (Ctrl+Enter to send messages)
- **Auto-save functionality** for chat sessions
- **Progress tracking** for model downloads
- **Thread-safe operations** for non-blocking UI
- **Professional styling** with role-based message formatting

### Technical Features

- **CustomTkinter 5.2.2** for modern GUI components
- **Requests-based API** communication with Ollama
- **JSON-based configuration** and data persistence
- **Multi-threading** for responsive user experience
- **Comprehensive logging** and error reporting
- **Cross-platform compatibility** (Windows, Linux, Mac)

### Documentation

- **Comprehensive README** with installation and usage guides
- **MIT License** for open-source distribution
- **Contributing guidelines** for community participation
- **Code documentation** with docstrings and type hints
- **Architecture overview** and extension guidelines

## [Unreleased]

### Planned Features

- Real-time model parameters (temperature, top_p, etc.)
- Multi-model conversation comparison
- Advanced search in chat history
- Conversation templates and prompt library
- Plugin system for extensions
- Model performance metrics
- Docker containerization
- Web interface option

---

## Version History Guidelines

### Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

### Version Numbering

- **Major version** (X.0.0): Breaking changes or major new features
- **Minor version** (1.X.0): New features, backwards compatible
- **Patch version** (1.0.X): Bug fixes, backwards compatible
