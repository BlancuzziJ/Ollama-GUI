"""
Security module for ShamaOllama
Provides comprehensive security measures including input validation,
URL validation, file path validation, and security monitoring.

Copyright (c) 2025 John Blancuzzi
Licensed under the MIT License
"""

import re
import os
import urllib.parse
from pathlib import Path
from typing import Union, List, Dict, Any
import hashlib
import secrets
import logging
import json


class SecurityValidator:
    """Comprehensive security validation for ShamaOllama"""
    
    # Allowed URL schemes for external links
    ALLOWED_SCHEMES = {'http', 'https'}
    
    # Maximum lengths for various inputs
    MAX_MESSAGE_LENGTH = 10000
    MAX_MODEL_NAME_LENGTH = 100
    MAX_URL_LENGTH = 2000
    MAX_FILENAME_LENGTH = 255
    
    # Dangerous patterns to detect
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',               # JavaScript URLs
        r'data:',                    # Data URLs
        r'vbscript:',                # VBScript URLs
        r'file://',                  # File protocol
        r'[<>"\']',                  # HTML injection characters
    ]
    
    def __init__(self):
        """Initialize security validator"""
        self.setup_logging()
        self.session_token = self.generate_session_token()
        
    def setup_logging(self):
        """Setup security logging"""
        log_dir = Path.home() / '.shamollama' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger('ShamaOllama.Security')
        handler = logging.FileHandler(log_dir / 'security.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
        
    def validate_url(self, url: str) -> bool:
        """Validate URL for security"""
        try:
            if not url or len(url) > self.MAX_URL_LENGTH:
                self.logger.warning(f"URL validation failed: Invalid length - {len(url) if url else 0}")
                return False
                
            parsed = urllib.parse.urlparse(url)
            
            # Check scheme
            if parsed.scheme.lower() not in self.ALLOWED_SCHEMES:
                self.logger.warning(f"URL validation failed: Invalid scheme - {parsed.scheme}")
                return False
                
            # Check for dangerous patterns
            if self.contains_dangerous_patterns(url):
                self.logger.warning(f"URL validation failed: Contains dangerous patterns - {url}")
                return False
                
            # Validate domain
            if not self.validate_domain(parsed.netloc):
                self.logger.warning(f"URL validation failed: Invalid domain - {parsed.netloc}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"URL validation error: {e}")
            return False
            
    def validate_domain(self, domain: str) -> bool:
        """Validate domain name"""
        if not domain:
            return False
            
        # Split domain and port
        host = domain.split(':')[0] if ':' in domain else domain
        
        # Allow localhost for Ollama
        if host in ['localhost', '127.0.0.1', '::1']:
            return True
            
        # Allow github.com for our project links
        github_domains = [
            'github.com',
            'www.github.com',
            'github.io',
            'githubusercontent.com'
        ]
        
        if any(host.endswith(allowed) for allowed in github_domains):
            return True
            
        # Basic domain validation
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )
        
        return bool(domain_pattern.match(host))
        
    def validate_message_input(self, message: str) -> bool:
        """Validate user message input"""
        try:
            if not message:
                return False
                
            if len(message) > self.MAX_MESSAGE_LENGTH:
                self.logger.warning(f"Message validation failed: Too long - {len(message)}")
                return False
                
            # Check for dangerous patterns
            if self.contains_dangerous_patterns(message):
                self.logger.warning("Message validation failed: Contains dangerous patterns")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Message validation error: {e}")
            return False
            
    def validate_model_name(self, model_name: str) -> bool:
        """Validate model name"""
        try:
            if not model_name or len(model_name) > self.MAX_MODEL_NAME_LENGTH:
                return False
                
            # Allow alphanumeric, hyphens, underscores, colons, and dots
            pattern = re.compile(r'^[a-zA-Z0-9._:-]+$')
            return bool(pattern.match(model_name))
            
        except Exception as e:
            self.logger.error(f"Model name validation error: {e}")
            return False
            
    def validate_file_path(self, file_path: Union[str, Path]) -> bool:
        """Validate file path for security"""
        try:
            path = Path(file_path)
            
            # Check filename length
            if len(path.name) > self.MAX_FILENAME_LENGTH:
                self.logger.warning(f"File path validation failed: Name too long - {path.name}")
                return False
                
            # Prevent path traversal
            if '..' in str(path) or str(path).startswith('/'):
                self.logger.warning(f"File path validation failed: Path traversal attempt - {path}")
                return False
                
            # Ensure it's within user directory
            user_dir = Path.home() / '.shamollama'
            try:
                path.resolve().relative_to(user_dir.resolve())
            except ValueError:
                self.logger.warning(f"File path validation failed: Outside user directory - {path}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"File path validation error: {e}")
            return False
            
    def contains_dangerous_patterns(self, text: str) -> bool:
        """Check if text contains dangerous patterns"""
        text_lower = text.lower()
        
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
                
        return False
        
    def sanitize_input(self, text: str) -> str:
        """Sanitize user input"""
        if not text:
            return ""
            
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Limit length
        if len(text) > self.MAX_MESSAGE_LENGTH:
            text = text[:self.MAX_MESSAGE_LENGTH]
            
        return text
        
    def validate_json_data(self, data: Any) -> bool:
        """Validate JSON data structure"""
        try:
            # Ensure it's not too large when serialized
            json_str = json.dumps(data)
            if len(json_str) > 100000:  # 100KB limit
                self.logger.warning("JSON validation failed: Too large")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"JSON validation error: {e}")
            return False
            
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events"""
        self.logger.info(f"Security Event: {event_type} - {details}")
        
    def create_secure_temp_file(self, suffix: str = '.tmp') -> Path:
        """Create a secure temporary file"""
        temp_dir = Path.home() / '.shamollama' / 'temp'
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate secure filename
        filename = f"{secrets.token_urlsafe(16)}{suffix}"
        return temp_dir / filename


# Global security instance
security = SecurityValidator()


def require_valid_url(func):
    """Decorator to validate URL parameters"""
    def wrapper(*args, **kwargs):
        # Check if first argument is a URL
        if args and isinstance(args[0], str) and args[0].startswith(('http://', 'https://')):
            if not security.validate_url(args[0]):
                security.log_security_event("Invalid URL blocked", {"url": args[0]})
                raise ValueError("Invalid URL provided")
        return func(*args, **kwargs)
    return wrapper


def require_valid_input(func):
    """Decorator to validate input parameters"""
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, str) and len(arg) > 0:
                if security.contains_dangerous_patterns(arg):
                    security.log_security_event("Dangerous input blocked", {"input": arg[:100]})
                    raise ValueError("Invalid input detected")
        return func(*args, **kwargs)
    return wrapper
