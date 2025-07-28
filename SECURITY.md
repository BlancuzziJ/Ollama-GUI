# Security Policy

## Supported Versions

We take security seriously and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## 🔒 Security Features

ShamaOllama implements comprehensive security measures to protect users:

### Input Validation

- **Message Content Validation**: All user messages are validated for length, dangerous patterns, and malicious content
- **Model Name Validation**: Model names are validated to prevent injection attacks
- **URL Validation**: All URLs are validated before opening to prevent malicious redirects
- **File Path Validation**: File operations are restricted to safe directories

### Data Protection

- **Secure Logging**: Security events are logged for monitoring and debugging
- **Safe File Operations**: All file operations are restricted to the user's `.shamollama` directory
- **Session Management**: Secure session tokens are generated for internal operations
- **Input Sanitization**: User inputs are sanitized before processing

### Network Security

- **URL Scheme Validation**: Only HTTP and HTTPS URLs are allowed
- **Domain Validation**: URLs are validated against allowed domain patterns
- **Connection Timeouts**: All network requests have appropriate timeouts
- **Error Handling**: Network errors are logged without exposing sensitive information

## 🛡️ Threat Protection

### Protected Against

- **Code Injection**: Script tags and executable code are blocked
- **Path Traversal**: File operations are restricted to safe directories
- **XSS Attacks**: Cross-site scripting attempts are filtered
- **Malicious URLs**: Dangerous URLs are blocked before opening
- **Data Exfiltration**: File access is limited to the application directory

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

Ollama GUI includes several security features:

- **Local-first architecture** - No data sent to external servers
- **Encrypted storage** for sensitive configuration data
- **Input validation** to prevent injection attacks
- **Safe file handling** for exports and imports
- **Secure API communication** with proper error handling

### Known Security Considerations

- **Local network access**: Ollama GUI connects to local Ollama instances
- **File system access**: Application stores data in user's home directory
- **Chat history**: Conversations are stored locally in plain text
- **Model downloads**: Models are downloaded through Ollama's API

Thank you for helping keep Ollama GUI secure!
