# Project Structure

This document outlines the architecture and structure of the Ollama GUI project.

## Directory Structure

```
ollama-gui/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── config_template.json    # Configuration template
├── core_methods.py         # Additional methods reference
├── run_gui.bat            # Windows launcher script
├── run_gui.ps1            # Enhanced PowerShell launcher
├── run_gui.sh             # Linux/macOS launcher script
├── README.md              # Project documentation
├── INSTALL.md             # Installation guide
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version history
├── SECURITY.md            # Security policy
├── LICENSE                # MIT license
├── .gitignore             # Git ignore rules
├── docs/                  # Additional documentation
│   ├── api.md            # API documentation
│   ├── architecture.md   # Architecture overview
│   └── screenshots/      # Application screenshots
└── tests/                 # Test suite (future)
    ├── test_api.py       # API tests
    ├── test_gui.py       # GUI tests
    └── test_utils.py     # Utility tests
```

## Code Architecture

### Main Components

#### 1. OllamaAPI Class

**File**: `main.py` (lines 22-95)
**Purpose**: Handles all communication with Ollama API

```python
class OllamaAPI:
    - test_connection()    # Health check
    - get_models()         # List available models
    - pull_model()         # Download new models
    - delete_model()       # Remove models
    - chat()              # Send chat requests
```

**Key Features**:

- **🌐 Remote Connectivity** - Support for any Ollama endpoint (local or remote)
- **🔒 Secure Communications** - HTTP and HTTPS support with certificate validation
- **📡 Streaming Responses** - Real-time message streaming from any Ollama instance
- **📊 Progress Callbacks** - Download progress tracking across network connections
- **🛡️ Robust Error Handling** - Network timeout and connection failure management
- **⚙️ Configurable Base URL** - Dynamic endpoint configuration at runtime

**Remote Architecture Benefits**:

- **Deployment Flexibility**: Connect to localhost, LAN servers, or cloud instances
- **Team Collaboration**: Multiple clients connecting to shared Ollama infrastructure
- **Resource Optimization**: Centralized model hosting on powerful hardware
- **Scalability**: Support for load-balanced and distributed Ollama deployments

#### 2. ChatManager Class

**File**: `main.py` (lines 97-172)
**Purpose**: Manages chat sessions and history

```python
class ChatManager:
    - add_message()        # Add message to session
    - get_messages_for_api() # Format for API
    - save_session()       # Persist session
    - load_session()       # Restore session
    - export_session()     # Export to file
```

**Key Features**:

- JSON-based persistence
- Session management
- Export functionality
- Message formatting

#### 3. OllamaGUI Class

**File**: `main.py` (lines 174-1040)
**Purpose**: Main application interface

```python
class OllamaGUI:
    - setup_gui()          # Initialize interface
    - create_panels()      # Build UI components
    - handle_events()      # Process user interactions
    - manage_state()       # Application state
```

**Panels**:

- **Chat Panel**: Main conversation interface
- **Models Panel**: Model management tools
- **History Panel**: Session browser
- **Settings Panel**: Configuration options

### Data Flow

```
User Input → GUI Event → API Call → Response Processing → UI Update
     ↓
  Chat Manager ← Session Storage ← JSON Persistence
```

### Threading Model

- **Main Thread**: GUI operations and user interaction
- **Background Threads**: API calls, model downloads, connection checks
- **Thread Safety**: `root.after()` for UI updates from threads

### Configuration Management

- **Runtime Config**: In-memory settings and state
- **Persistent Config**: JSON files in `~/.ollama_gui/`
- **Default Values**: Hardcoded fallbacks

### Error Handling Strategy

1. **Graceful Degradation**: Features fail safely
2. **User Feedback**: Clear error messages
3. **Logging**: Debug information for troubleshooting
4. **Recovery**: Automatic retry and fallback mechanisms

## Design Patterns

### 1. Observer Pattern

- GUI components observe state changes
- Automatic UI updates on data changes

### 2. Command Pattern

- Menu actions and button clicks
- Consistent command handling

### 3. Model-View Pattern

- Clear separation of data and presentation
- Testable business logic

### 4. Strategy Pattern

- Different export formats
- Pluggable API implementations

## Styling and Theming

### CustomTkinter Integration

- Modern widget styling
- Dark/light theme support
- Consistent visual design
- Responsive layouts

### Color Scheme

```python
# Dark Theme
Background: #2b2b2b
Text: #ffffff
Accent: #4A9EFF (Blue)
Success: #50C878 (Green)
Error: #FF6B6B (Red)
Warning: #FFD93D (Yellow)

# Light Theme
Background: #ffffff
Text: #000000
# ... (inverse colors)
```

### Typography

- **Headers**: CTkFont(size=18-20, weight="bold")
- **Body**: CTkFont(size=14)
- **Status**: CTkFont(size=12)
- **Monospace**: For code/technical content

## Performance Considerations

### Memory Management

- Limit chat history size
- Clean up resources on close
- Efficient string handling for streaming

### CPU Optimization

- Background threading for I/O
- Minimal UI redraws
- Lazy loading of data

### Network Efficiency

- Connection pooling
- Request timeouts
- Retry mechanisms

## Security Architecture

### Data Protection

- Local-only data storage
- No external data transmission
- Secure file handling

### Input Validation

- Sanitize user inputs
- Validate API responses
- Prevent injection attacks

### Network Security

- HTTPS support for remote Ollama
- Certificate validation
- Secure error messages

## Extensibility Points

### Plugin System (Future)

- Event hooks for extensions
- API for custom panels
- Theme system expansion

### Configuration Expansion

- Additional model parameters
- Custom keyboard shortcuts
- Advanced UI preferences

### API Extensions

- Support for other LLM services
- Custom model providers
- Enhanced streaming protocols

## Testing Strategy

### Unit Tests

- API communication
- Data persistence
- Utility functions

### Integration Tests

- GUI component interaction
- End-to-end workflows
- Error handling scenarios

### Manual Testing

- Cross-platform compatibility
- User experience validation
- Performance benchmarking

## Deployment Architecture

### Standalone Application

- Self-contained Python environment
- All dependencies bundled
- Platform-specific launchers

### Container Deployment

- Docker image with all components
- Web interface option
- Scalable deployment

### Development Environment

- Virtual environment isolation
- Hot reload capability
- Debug mode support

## Future Architecture Plans

### Microservices Split

- Separate API service
- Web frontend option
- Mobile app support

### Database Integration

- SQLite for complex queries
- Full-text search
- Advanced analytics

### Cloud Integration

- Remote model hosting
- Synchronized settings
- Collaborative features

---

This architecture supports the current features while providing flexibility for future enhancements. The modular design ensures maintainability and extensibility as the project grows.
