# Security Policy

## Supported Versions

We take security seriously and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## 🔒 Security Features

ShamaOllama implements comprehensive security measures to protect users:

### Input Validation

- **Message Length Validation**: User messages are validated for reasonable length limits
- **Model Name Validation**: Model names are validated to prevent injection attacks
- **URL Validation**: All URLs are validated before opening to prevent malicious redirects
- **File Path Validation**: File operations are restricted to safe directories

_Note: Content validation has been minimized to ensure maximum performance and user freedom. ShamaOllama acts as a fast bridge to Ollama, trusting Ollama's own security mechanisms for content handling._

### Data Protection

- **Secure Logging**: Security events are logged for monitoring and debugging
- **Safe File Operations**: All file operations are restricted to the user's `.shamollama` directory
- **Session Management**: Secure session tokens are generated for internal operations
- **Minimal Input Processing**: User inputs are passed directly to Ollama with minimal interference for maximum speed

_Note: ShamaOllama prioritizes performance and user freedom, delegating content security to Ollama's robust handling mechanisms._

### Network Security

- **URL Scheme Validation**: Only HTTP and HTTPS URLs are allowed
- **Domain Validation**: URLs are validated against allowed domain patterns
- **Connection Timeouts**: All network requests have appropriate timeouts
- **Error Handling**: Network errors are logged without exposing sensitive information

## 🛡️ Threat Protection

### Protected Against

- **Path Traversal**: File operations are restricted to safe directories
- **Malicious URLs**: Dangerous URLs are blocked before opening
- **Data Exfiltration**: File access is limited to the application directory
- **Network Vulnerabilities**: Secure API communication with proper error handling

_Note: Content-based protections (XSS, code injection) are handled by Ollama itself. ShamaOllama focuses on file system, network, and application-level security while maintaining maximum chat performance._

## Reporting a Vulnerability

If you discover a security vulnerability in ShamaOllama, please report it responsibly:

### Contact Information

- **Email**: john@blancuzzi.org
- **Subject**: "SECURITY: ShamaOllama Vulnerability Report"

### What to Include

Please include the following information in your report:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** and severity
4. **Suggested fix** (if you have one)
5. **Your contact information** for follow-up

### Response Timeline

- **Initial response**: Within 48 hours
- **Acknowledgment**: Within 7 days
- **Status updates**: Every 7 days until resolved
- **Resolution**: Target within 30 days for critical issues

### Security Best Practices

When using Ollama GUI:

1. **Keep software updated** to the latest version
2. **Use HTTPS** when configuring custom Ollama URLs
3. **Be cautious** with sensitive information in chat sessions
4. **Review exported files** before sharing
5. **Use secure networks** when accessing remote Ollama instances

### Responsible Disclosure

We follow responsible disclosure practices:

1. **We will acknowledge** your report within 48 hours
2. **We will investigate** and verify the vulnerability
3. **We will develop and test** a fix
4. **We will coordinate** the release with you
5. **We will credit you** (if desired) in the security advisory

### Security Features

ShamaOllama includes several security features:

- **Local-first architecture** - No data sent to external servers
- **Secure file handling** for exports and imports
- **Safe API communication** with proper error handling
- **URL validation** for external links
- **File system protection** - Operations restricted to user directories

_Design Philosophy: ShamaOllama acts as a high-performance bridge to Ollama, focusing on application security while trusting Ollama's content handling. This approach maximizes speed and user freedom while maintaining essential protections._

### Known Security Considerations

- **Local network access**: ShamaOllama connects to local Ollama instances
- **File system access**: Application stores data in user's home directory
- **Chat history**: Conversations are stored locally in plain text
- **Model downloads**: Models are downloaded through Ollama's API
- **Content trust**: Chat content security is delegated to Ollama for maximum performance
- **Performance focus**: Minimal validation overhead to ensure responsive user experience

_Security Approach: ShamaOllama prioritizes speed and user experience while maintaining essential application-level protections. Content security is handled by Ollama's robust mechanisms._

Thank you for helping keep Ollama GUI secure!
