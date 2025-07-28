# Contributing to ShamaOllama

Thank you for your interest in contributing to ShamaOllama! This document provides guidelines and information for contributors.

_Paying homage to "Shama Lama Ding Dong" from Animal House (1978) - let's keep the fun spirit alive while building great software!_

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful and inclusive** to all participants
- **Use welcoming and inclusive language**
- **Be collaborative and constructive** in discussions
- **Focus on what is best for the community**
- **Show empathy towards other community members**

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Ollama installed locally
- Basic knowledge of Python and GUI development

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/YOUR_USERNAME/ollama-gui.git
   cd ollama-gui
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application** to ensure it works:
   ```bash
   python main.py
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-model-parameters` - New features
- `bugfix/fix-streaming-issue` - Bug fixes
- `docs/update-readme` - Documentation changes
- `refactor/cleanup-api-class` - Code refactoring

### Commit Messages

Write clear, descriptive commit messages:

```
Add real-time model parameter controls

- Add temperature and top_p sliders to settings panel
- Implement parameter validation and persistence
- Update API calls to include model parameters
- Add tooltips explaining each parameter

Fixes #123
```

## Pull Request Process

1. **Update documentation** if you've made changes to functionality
2. **Add or update tests** for new features
3. **Ensure all tests pass** locally
4. **Update the README.md** if you've added new features
5. **Create a detailed pull request description**:

```markdown
## Description

Brief description of changes made.

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update

## Testing

- [ ] I have tested these changes locally
- [ ] I have updated/added relevant tests
- [ ] All tests pass

## Screenshots (if applicable)

Add screenshots to help explain your changes.

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
```

## Coding Standards

### Python Style

- **Follow PEP 8** style guidelines
- **Use type hints** for function parameters and return values
- **Include docstrings** for all classes and functions
- **Use meaningful variable names**
- **Keep functions focused** (single responsibility principle)

### Example Code Style

```python
def update_streaming_response(self, chunk: str) -> None:
    """
    Update the streaming response with new chunk.

    Args:
        chunk: New text chunk from the streaming response

    Returns:
        None
    """
    if chunk and self.response_start_pos:
        # Implementation here
        pass
```

### GUI Guidelines

- **Use CustomTkinter** consistently for all GUI elements
- **Maintain visual consistency** with existing design
- **Add proper error handling** for all user interactions
- **Include loading states** for long-running operations
- **Provide clear user feedback** for all actions

### Architecture Principles

- **Separation of concerns** - Keep API, GUI, and data management separate
- **Modularity** - Write reusable, focused components
- **Error handling** - Graceful degradation and user-friendly error messages
- **Thread safety** - Use proper threading for non-blocking operations

## Testing Guidelines

### Manual Testing

Before submitting:

1. **Test all major features** work correctly
2. **Test error conditions** (no Ollama connection, invalid models, etc.)
3. **Test on different window sizes** and themes
4. **Verify streaming responses** work properly
5. **Check model management** functions

### Future Testing Framework

We plan to add automated testing with:

- Unit tests for API classes
- Integration tests for GUI components
- Mock tests for Ollama API interactions

## Documentation

### Code Documentation

- **Add docstrings** to all public methods and classes
- **Comment complex logic** inline
- **Update README.md** for new features
- **Include type hints** for better code clarity

### User Documentation

- **Update README.md** for user-facing changes
- **Add screenshots** for new UI features
- **Update installation instructions** if needed
- **Document new configuration options**

## Feature Requests

### High Priority Features

These are features we'd love help with:

- Real-time model parameters (temperature, top_p)
- Multi-model conversation comparison
- Advanced chat history search
- Conversation templates and prompts
- Plugin system architecture

### Suggesting New Features

1. **Check existing issues** to avoid duplicates
2. **Create a detailed feature request** with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach
   - Mockups or examples if applicable

## Questions?

If you have questions about contributing:

1. **Check the [Issues](https://github.com/jblancuzzi/ollama-gui/issues)** page
2. **Start a [Discussion](https://github.com/jblancuzzi/ollama-gui/discussions)**
3. **Contact the maintainer**: jblancuzzi@cupid.org

## Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for their contributions
- **Special thanks** in documentation

---

Thank you for contributing to Ollama GUI! 🚀
