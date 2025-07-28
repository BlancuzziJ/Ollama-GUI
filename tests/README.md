# 🧪 ShamaOllama Tests

This directory contains test scripts to validate ShamaOllama functionality.

## Running Tests

### Individual Tests

```bash
# Test thinking models filtering
python tests/test_thinking_filter.py

# Test GPU detection
python tests/test_gpu_detection.py

# Test dependencies
python tests/test_dependencies.py

# Test security features
python tests/test_security.py

# Test app functionality
python tests/test_app.py
```

### Run All Tests

```bash
# Windows
python tests/run_all_tests.py

# Linux/Mac
python3 tests/run_all_tests.py
```

## Test Descriptions

### `test_thinking_filter.py`

- **Purpose**: Validates thinking models filtering patterns
- **Tests**: DeepSeek `<think>`, `<thinking>`, bracket styles, markdown patterns
- **Coverage**: All supported reasoning block formats

### `test_gpu_detection.py`

- **Purpose**: Demonstrates plugin architecture for optional dependencies
- **Tests**: GPUtil, psutil integration, graceful fallbacks
- **Coverage**: Hardware detection with and without enhanced dependencies

### `test_dependencies.py`

- **Purpose**: Validates optional dependency installation
- **Tests**: Import checking, version compatibility
- **Coverage**: Core vs enhanced dependency sets

### `test_security.py`

- **Purpose**: Security validation and input sanitization
- **Tests**: URL validation, input filtering, security policies
- **Coverage**: All security-critical user inputs

### `test_app.py`

- **Purpose**: Core application functionality
- **Tests**: API connections, model management, chat features
- **Coverage**: Main application workflows

## For Developers

These tests serve multiple purposes:

1. **Quality Assurance** - Validate features work as expected
2. **Documentation** - Show how features are supposed to work
3. **Regression Testing** - Catch breaking changes
4. **Community Contributions** - Help others understand the codebase

## Adding New Tests

When adding new features:

1. Create a new `test_feature_name.py` file
2. Follow the existing test patterns
3. Add it to `run_all_tests.py`
4. Update this README

## CI/CD Integration

These tests are designed to work with GitHub Actions:

```yaml
- name: Run Tests
  run: python tests/run_all_tests.py
```
