"""
ShamaOllama - A modern, professional interface for Ollama
Built with CustomTkinter for a clean, fast, and robust experience

Paying homage to "Shama Lama Ding Dong" from Animal House (1978)
- A classic comedy that brought joy to generations

The name "Shama" carries beautiful meanings across cultures:
- Sanskrit: Equanimity, calmness, peace of mind (balanced AI interaction)
- Hebrew: To listen, to hear, to obey (responsive AI conversation)  
- Persian: Candle/enlightenment (the light of knowledge AI provides)

Copyright (c) 2025 John Blancuzzi
Licensed under the MIT License - see LICENSE file for details

Author: John Blancuzzi
Email: john@blancuzzi.org
Project: https://github.com/BlancuzziJ/Ollama-GUI
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image
import requests
import json
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Callable
import os
import logging
from pathlib import Path
import webbrowser
from security import security  # Minimal security for URLs only
from gpu_info import get_gpu_info, format_gpu_info_for_display, check_gpu_dependencies

# Configure logging to suppress debug messages from GPU detection
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

# Set appearance mode and theme
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class OllamaAPI:
    """Handles all communication with the Ollama API with security validation"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        # Validate URL before setting
        if not security.validate_url(base_url):
            security.log_security_event("Invalid Ollama URL", {"url": base_url})
            raise ValueError("Invalid Ollama URL provided")
        self.base_url = base_url.rstrip('/')
        
    def test_connection(self) -> bool:
        """Test if Ollama is running and accessible - fast, no validation"""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            security.log_security_event("Connection test failed", {"error": str(e)})
            return False
    
    def get_models(self) -> List[Dict]:
        """Get list of available models with security validation"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                # Validate each model name
                validated_models = []
                for model in models:
                    if isinstance(model, dict) and 'name' in model:
                        if security.validate_model_name(model['name']):
                            validated_models.append(model)
                        else:
                            security.log_security_event("Invalid model name detected", {"model": model['name']})
                return validated_models
        except requests.RequestException as e:
            security.log_security_event("Failed to get models", {"error": str(e)})
        return []
    
    def pull_model(self, model_name: str, progress_callback: Optional[Callable] = None) -> bool:
        """Pull a new model with progress tracking and validation"""
        # Validate model name
        if not security.validate_model_name(model_name):
            security.log_security_event("Invalid model name for pull", {"model": model_name})
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=300
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode())
                        if progress_callback:
                            progress_callback(data)
                        if data.get('status') == 'success':
                            return True
        except requests.RequestException:
            pass
        return False
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a model with validation"""
        # Validate model name
        if not security.validate_model_name(model_name):
            security.log_security_event("Invalid model name for deletion", {"model": model_name})
            return False
            
        try:
            response = requests.delete(f"{self.base_url}/api/delete", json={"name": model_name}, timeout=30)
            return response.status_code == 200
        except requests.RequestException as e:
            security.log_security_event("Failed to delete model", {"model": model_name, "error": str(e)})
            return False
    
    def chat(self, model: str, messages: List[Dict], stream_callback: Optional[Callable] = None, hide_thinking: bool = False) -> str:
        """Send chat request to Ollama with security validation"""
        # Validate model name
        if not security.validate_model_name(model):
            security.log_security_event("Invalid model name for chat", {"model": model})
            return ""
        
        # Fast path - construct request immediately
        request_data = {
            "model": model,
            "messages": messages,
            "stream": bool(stream_callback)
        }
        
        # Add options for thinking models
        if hide_thinking:
            # Common parameters to suppress thinking/reasoning
            request_data["options"] = {
                "temperature": 0.7,  # Keep default temperature
                "hide_thinking": True,  # Custom parameter for some models
                "show_reasoning": False,  # Alternative parameter name
                "thinking": False,  # Another common parameter
            }
        
        if not security.validate_json_data(request_data):
            security.log_security_event("Request data too large", {"model": model})
            return ""
            
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=request_data,
                stream=bool(stream_callback),
                timeout=60
            )
            
            if response.status_code == 200:
                if stream_callback:
                    full_response = ""
                    thinking_content = ""
                    in_thinking_block = False
                    
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line.decode())
                            if 'message' in data and 'content' in data['message']:
                                content = data['message']['content']
                                
                                if hide_thinking:
                                    # Try to detect and filter thinking blocks
                                    # Common patterns: <thinking>, [THINKING], **Thinking:**
                                    if any(marker in content.lower() for marker in ['<thinking>', '[thinking]', '**thinking', 'thinking:']):
                                        in_thinking_block = True
                                        thinking_content += content
                                        continue
                                    elif any(marker in content.lower() for marker in ['</thinking>', '[/thinking]', '**answer', 'answer:']):
                                        in_thinking_block = False
                                        thinking_content = ""
                                        # Skip this chunk as it's the end of thinking
                                        continue
                                    elif in_thinking_block:
                                        thinking_content += content
                                        continue
                                
                                full_response += content
                                stream_callback(content)
                            if data.get('done', False):
                                break
                    return full_response
                else:
                    data = response.json()
                    response_content = data['message']['content']
                    
                    if hide_thinking:
                        # Post-process to remove thinking blocks from non-streaming response
                        response_content = self._filter_thinking_content(response_content)
                    
                    return response_content
        except requests.RequestException as e:
            raise Exception(f"Chat request failed: {str(e)}")
        return ""
    
    def _filter_thinking_content(self, content: str) -> str:
        """Filter out thinking/reasoning blocks from response content"""
        import re
        
        # Remove common thinking block patterns
        patterns = [
            r'<think>.*?</think>',  # <think>...</think> (DeepSeek style)
            r'<thinking>.*?</thinking>',  # <thinking>...</thinking>
            r'\[thinking\].*?\[/thinking\]',  # [thinking]...[/thinking]
            r'\*\*thinking:?\*\*.*?(?=\*\*answer|\*\*response|\n\n|\Z)',  # **Thinking:**...
            r'thinking:.*?(?=answer:|response:|\n\n|\Z)',  # thinking:...
            r'<thought>.*?</thought>',  # <thought>...</thought>
            r'\[thought\].*?\[/thought\]',  # [thought]...[/thought]
        ]
        
        filtered_content = content
        for pattern in patterns:
            filtered_content = re.sub(pattern, '', filtered_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up extra whitespace and newlines
        filtered_content = re.sub(r'\n\s*\n\s*\n', '\n\n', filtered_content)
        filtered_content = filtered_content.strip()
        
        return filtered_content


class ChatManager:
    """Manages chat sessions and history"""
    
    def __init__(self):
        self.current_session = []
        self.chat_history = []
        self.data_dir = Path.home() / ".shamollama"
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "chat_history.json"
        self.load_history()
    
    def add_message(self, role: str, content: str, model: str = ""):
        """Add a message to current session"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "model": model
        }
        self.current_session.append(message)
    
    def get_messages_for_api(self) -> List[Dict]:
        """Get messages formatted for Ollama API"""
        return [{"role": msg["role"], "content": msg["content"]} 
                for msg in self.current_session if msg["role"] in ["user", "assistant"]]
    
    def save_session(self, title: str = ""):
        """Save current session to history"""
        if not self.current_session:
            return
            
        session = {
            "title": title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "timestamp": datetime.now().isoformat(),
            "messages": self.current_session.copy()
        }
        self.chat_history.append(session)
        self.save_history()
    
    def new_session(self):
        """Start a new chat session"""
        if self.current_session:
            self.save_session()
        self.current_session = []
    
    def load_session(self, index: int):
        """Load a session from history"""
        if 0 <= index < len(self.chat_history):
            self.current_session = self.chat_history[index]["messages"].copy()
    
    def save_history(self):
        """Save chat history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_history(self):
        """Load chat history from file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.chat_history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            self.chat_history = []
    
    def export_session(self, filepath: str, session_index: int = -1):
        """Export a session to file"""
        session = self.chat_history[session_index] if session_index >= 0 else {
            "title": "Current Session",
            "timestamp": datetime.now().isoformat(),
            "messages": self.current_session
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if filepath.endswith('.json'):
                    json.dump(session, f, indent=2, ensure_ascii=False)
                else:  # Text format
                    f.write(f"# {session['title']}\n")
                    f.write(f"Date: {session['timestamp']}\n\n")
                    for msg in session['messages']:
                        role = msg['role'].title()
                        f.write(f"**{role}**: {msg['content']}\n\n")
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")


class ShamaOllamaGUI:
    """Main GUI application"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ShamaOllama - Streaming AI Interface")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set application icon - CustomTkinter specific approach
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "images", "icons", "ShamaOllama_Icon.ico")
            if os.path.exists(icon_path):
                # Set icon after the window is fully initialized
                self.root.after(100, lambda: self._set_window_icon(icon_path))
        except Exception as e:
            # Icon loading failed, continue without icon
            pass
        
        # Initialize components
        self.api = OllamaAPI()
        self.chat_manager = ChatManager()
        self.current_model = None
        self.models = []
        self.is_chatting = False
        
        # Streaming response variables
        self.current_response = ""
        self.response_start_pos = None
        self.typing_animation_active = False
        self.first_token_received = False
        
        # Settings variables
        self.autosave_var = ctk.BooleanVar(value=True)
        
        # Setup GUI
        self.setup_gui()
        self.refresh_models()
        self.check_connection()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _set_window_icon(self, icon_path):
        """Helper method to set window icon with multiple fallback approaches"""
        try:
            # Try different methods for setting icon with CustomTkinter
            
            # Method 1: wm_iconbitmap (works best on Windows)
            self.root.wm_iconbitmap(icon_path)
            
        except Exception:
            try:
                # Method 2: iconphoto with PNG fallback
                png_path = icon_path.replace('.ico', '.png')
                if os.path.exists(png_path):
                    icon_image = tk.PhotoImage(file=png_path)
                    self.root.iconphoto(True, icon_image)
            except Exception:
                # Method 3: Try to set the icon using the underlying tk window
                try:
                    self.root.tk.call('wm', 'iconbitmap', self.root._w, icon_path)
                except Exception:
                    pass  # All methods failed, continue without icon
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_area()
        
        # Create status bar
        self.create_status_bar()
    
    def create_sidebar(self):
        """Create the left sidebar with navigation and controls"""
        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.sidebar, 
            text="ShamaOllama", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Model selection
        model_label = ctk.CTkLabel(self.sidebar, text="Select Model:")
        model_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.model_dropdown = ctk.CTkComboBox(
            self.sidebar,
            values=["No models available"],
            command=self.on_model_dropdown_selected,
            state="readonly"
        )
        self.model_dropdown.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        # Control buttons
        self.new_chat_btn = ctk.CTkButton(
            self.sidebar,
            text="New Chat",
            command=self.new_chat,
            height=35
        )
        self.new_chat_btn.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        # Navigation frame
        nav_frame = ctk.CTkFrame(self.sidebar)
        nav_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        nav_frame.grid_rowconfigure(3, weight=1)
        
        # Navigation buttons
        nav_buttons = [
            ("💬 Chat", self.show_chat),
            ("🔧 Models", self.show_models),
            ("📜 History", self.show_history),
            ("🖥️ System", self.show_system),
            ("⚙️ Settings", self.show_settings),
            ("ℹ️ About", self.show_about)
        ]
        
        self.nav_buttons = {}
        for i, (text, command) in enumerate(nav_buttons):
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                height=35,
                corner_radius=6
            )
            btn.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            self.nav_buttons[text.split()[1]] = btn
        
        # Select chat by default
        self.nav_buttons["Chat"].configure(fg_color=("gray75", "gray25"))
        
        # Theme toggle
        self.theme_btn = ctk.CTkButton(
            self.sidebar,
            text="🌙 Dark Theme",
            command=self.toggle_theme,
            height=30
        )
        self.theme_btn.grid(row=5, column=0, padx=20, pady=(10, 5), sticky="ew")
        
        # Support button
        self.support_btn = ctk.CTkButton(
            self.sidebar,
            text="💖 Support ShamaOllama",
            command=lambda: self.open_url("https://github.com/sponsors/BlancuzziJ"),
            height=30,
            fg_color=("pink", "darkred"),
            hover_color=("lightpink", "red"),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.support_btn.grid(row=6, column=0, padx=20, pady=(5, 20), sticky="ew")
    
    def create_main_area(self):
        """Create the main content area"""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create different panels
        self.create_chat_panel()
        self.create_models_panel()
        self.create_history_panel()
        self.create_system_panel()
        self.create_settings_panel()
        self.create_about_panel()
        
        # Show chat panel by default
        self.current_panel = "chat"
        self.chat_panel.grid(row=0, column=0, sticky="nsew")
    
    def create_chat_panel(self):
        """Create the chat interface panel"""
        self.chat_panel = ctk.CTkFrame(self.main_frame)
        self.chat_panel.grid_columnconfigure(0, weight=1)
        self.chat_panel.grid_rowconfigure(0, weight=1)
        
        # Chat display area
        self.chat_display = ctk.CTkTextbox(
            self.chat_panel,
            wrap="word",
            font=ctk.CTkFont(size=14),
            state="disabled"
        )
        self.chat_display.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        
        # Input frame
        input_frame = ctk.CTkFrame(self.chat_panel, height=100)
        input_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_rowconfigure(0, weight=1)
        
        # Message input
        self.message_input = ctk.CTkTextbox(
            input_frame,
            height=80,
            font=ctk.CTkFont(size=14),
            wrap="word"
        )
        self.message_input.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Send button
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self.send_message,
            width=80,
            height=35
        )
        self.send_btn.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="s")
        
        # Bind Enter key
        self.message_input.bind("<Control-Return>", lambda e: self.send_message())
        
        # Add welcome message
        self.add_chat_message("System", "Welcome to ShamaOllama! Select a model from the sidebar to start chatting.", "system")
    
    def create_models_panel(self):
        """Create the comprehensive models management panel"""
        self.models_panel = ctk.CTkFrame(self.main_frame)
        self.models_panel.grid_columnconfigure(0, weight=1)
        self.models_panel.grid_rowconfigure(2, weight=1)
        
        # Header with status
        header_frame = ctk.CTkFrame(self.models_panel)
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)
        
        header = ctk.CTkLabel(
            header_frame,
            text="🔧 Ollama Model Manager",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.models_count_label = ctk.CTkLabel(
            header_frame,
            text="Loading models...",
            font=ctk.CTkFont(size=12)
        )
        self.models_count_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        
        # Control buttons frame (top)
        controls_frame = ctk.CTkFrame(self.models_panel)
        controls_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        controls_frame.grid_columnconfigure(2, weight=1)
        
        # Pull model section
        pull_frame = ctk.CTkFrame(controls_frame)
        pull_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        pull_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(pull_frame, text="📥 Pull Model:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.pull_entry = ctk.CTkEntry(
            pull_frame, 
            placeholder_text="Enter model name (e.g., llama3.2, mistral, codellama:13b)",
            height=35
        )
        self.pull_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.pull_btn = ctk.CTkButton(
            pull_frame, 
            text="Pull Model", 
            command=self.pull_model, 
            width=100,
            height=35,
            font=ctk.CTkFont(weight="bold")
        )
        self.pull_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Quick pull buttons for popular models
        quick_pull_frame = ctk.CTkFrame(pull_frame)
        quick_pull_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(quick_pull_frame, text="Quick Pull:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        
        popular_models = [
            ("Llama 3.2", "llama3.2"),
            ("Mistral", "mistral"),
            ("CodeLlama", "codellama"),
            ("Phi-3", "phi3"),
            ("Gemma", "gemma")
        ]
        
        for i, (display_name, model_name) in enumerate(popular_models):
            btn = ctk.CTkButton(
                quick_pull_frame,
                text=display_name,
                command=lambda m=model_name: self.quick_pull_model(m),
                width=80,
                height=25,
                font=ctk.CTkFont(size=10)
            )
            btn.grid(row=0, column=i+1, padx=2, pady=2)
        
        # Models list frame with selection
        list_frame = ctk.CTkFrame(self.models_panel)
        list_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        # List header with selection controls
        list_header_frame = ctk.CTkFrame(list_frame)
        list_header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        list_header_frame.grid_columnconfigure(1, weight=1)
        
        self.select_all_var = ctk.BooleanVar()
        self.select_all_check = ctk.CTkCheckBox(
            list_header_frame,
            text="Select All",
            variable=self.select_all_var,
            command=self.toggle_select_all
        )
        self.select_all_check.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(
            list_header_frame,
            text="📋 Available Models",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Scrollable models list
        self.models_scroll_frame = ctk.CTkScrollableFrame(list_frame, height=300)
        self.models_scroll_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.models_scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize models tracking
        self.model_checkboxes = {}
        self.model_info_labels = {}
        self.selected_models = set()
        
        # Action buttons frame (bottom)
        actions_frame = ctk.CTkFrame(self.models_panel)
        actions_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        # Model actions
        action_buttons = [
            ("🔄 Refresh", self.refresh_models, "blue", None),
            ("❌ Delete Selected", self.delete_selected_models, "red", "darkred"),
            ("📋 Copy Names", self.copy_selected_model_names, "gray", "darkgray"),
            ("📊 Model Info", self.show_selected_model_info, "green", "darkgreen"),
            ("🔧 Manage Tags", self.manage_model_tags, "orange", "darkorange")
        ]
        
        for i, (text, command, color, hover_color) in enumerate(action_buttons):
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                command=command,
                height=35,
                fg_color=color if color != "blue" else None,
                hover_color=hover_color
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            actions_frame.grid_columnconfigure(i, weight=1)
        
        # Progress section
        progress_frame = ctk.CTkFrame(self.models_panel)
        progress_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame, 
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.grid(row=0, column=0, padx=10, pady=2, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=2, sticky="ew")
        self.progress_bar.set(0)
        
        self.progress_percentage = ctk.CTkLabel(
            progress_frame,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.progress_percentage.grid(row=1, column=1, padx=5, pady=2)
    
    def create_history_panel(self):
        """Create the chat history panel"""
        self.history_panel = ctk.CTkFrame(self.main_frame)
        self.history_panel.grid_columnconfigure(0, weight=1)
        self.history_panel.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            self.history_panel,
            text="Chat History",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, pady=10)
        
        # History list
        self.history_listbox = ctk.CTkTextbox(self.history_panel, state="disabled")
        self.history_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Controls
        controls_frame = ctk.CTkFrame(self.history_panel)
        controls_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.load_session_btn = ctk.CTkButton(
            controls_frame,
            text="Load Session",
            command=self.load_selected_session
        )
        self.load_session_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.export_btn = ctk.CTkButton(
            controls_frame,
            text="Export Session",
            command=self.export_selected_session
        )
        self.export_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.clear_history_btn = ctk.CTkButton(
            controls_frame,
            text="Clear History",
            command=self.clear_history,
            fg_color="red",
            hover_color="darkred"
        )
        self.clear_history_btn.grid(row=0, column=2, padx=5, pady=5)
    
    def create_settings_panel(self):
        """Create the settings panel"""
        self.settings_panel = ctk.CTkFrame(self.main_frame)
        self.settings_panel.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            self.settings_panel,
            text="Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, pady=10)
        
        # Settings form
        form_frame = ctk.CTkFrame(self.settings_panel)
        form_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Ollama URL
        ctk.CTkLabel(form_frame, text="Ollama URL:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.url_entry = ctk.CTkEntry(form_frame, placeholder_text="http://localhost:11434")
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.url_entry.insert(0, self.api.base_url)
        
        # Test connection button
        self.test_btn = ctk.CTkButton(
            form_frame,
            text="Test Connection",
            command=self.test_connection_manual
        )
        self.test_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Auto-save chats
        self.autosave_var = ctk.BooleanVar(value=True)
        self.autosave_check = ctk.CTkCheckBox(
            form_frame,
            text="Auto-save chat sessions",
            variable=self.autosave_var
        )
        self.autosave_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Hide thinking/reasoning for thinking models
        self.hide_thinking_var = ctk.BooleanVar(value=False)
        self.hide_thinking_check = ctk.CTkCheckBox(
            form_frame,
            text="Hide thinking/reasoning process (for models like DeepSeek)",
            variable=self.hide_thinking_var
        )
        self.hide_thinking_check.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Add info button for thinking models feature
        self.thinking_info_btn = ctk.CTkButton(
            form_frame,
            text="ℹ️",
            width=30,
            height=30,
            command=self.show_thinking_info,
            fg_color="transparent",
            text_color="gray"
        )
        self.thinking_info_btn.grid(row=2, column=2, padx=5, pady=5)
        
        # Max history
        ctk.CTkLabel(form_frame, text="Max history entries:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.max_history_entry = ctk.CTkEntry(form_frame, width=100)
        self.max_history_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.max_history_entry.insert(0, "100")
        
        # Security section
        security_frame = ctk.CTkFrame(self.settings_panel)
        security_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        security_frame.grid_columnconfigure(1, weight=1)
        
        security_header = ctk.CTkLabel(
            security_frame,
            text="🔒 Security Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        security_header.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Security logging
        self.security_logging_var = ctk.BooleanVar(value=True)
        self.security_logging_check = ctk.CTkCheckBox(
            security_frame,
            text="Enable security logging",
            variable=self.security_logging_var
        )
        self.security_logging_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Input validation
        self.input_validation_var = ctk.BooleanVar(value=True)
        self.input_validation_check = ctk.CTkCheckBox(
            security_frame,
            text="Enable input validation (recommended)",
            variable=self.input_validation_var
        )
        self.input_validation_check.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # URL validation
        self.url_validation_var = ctk.BooleanVar(value=True)
        self.url_validation_check = ctk.CTkCheckBox(
            security_frame,
            text="Enable URL validation (recommended)",
            variable=self.url_validation_var
        )
        self.url_validation_check.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # View security logs button
        self.view_logs_btn = ctk.CTkButton(
            security_frame,
            text="View Security Logs",
            command=self.view_security_logs,
            height=30
        )
        self.view_logs_btn.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        
        # Clear logs button
        self.clear_logs_btn = ctk.CTkButton(
            security_frame,
            text="Clear Logs",
            command=self.clear_security_logs,
            height=30,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.clear_logs_btn.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # Save settings button
        self.save_settings_btn = ctk.CTkButton(
            form_frame,
            text="Save Settings",
            command=self.save_settings
        )
        self.save_settings_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=20)
    
    def create_system_panel(self):
        """Create the system information panel"""
        self.system_panel = ctk.CTkFrame(self.main_frame)
        self.system_panel.grid_columnconfigure(0, weight=1)
        self.system_panel.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            self.system_panel,
            text="System Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, pady=10)
        
        # System info display
        self.system_info_display = ctk.CTkTextbox(
            self.system_panel,
            wrap="none",
            font=ctk.CTkFont(family="Courier", size=12),
            state="disabled"
        )
        self.system_info_display.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Refresh button
        refresh_frame = ctk.CTkFrame(self.system_panel, height=50)
        refresh_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.refresh_system_btn = ctk.CTkButton(
            refresh_frame,
            text="🔄 Refresh System Info",
            command=self.refresh_system_info,
            height=35
        )
        self.refresh_system_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Load system info on creation
        self.refresh_system_info()
    
    def create_about_panel(self):
        """Create the about panel with app info and donation links"""
        self.about_panel = ctk.CTkFrame(self.main_frame)
        self.about_panel.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for content
        scroll_frame = ctk.CTkScrollableFrame(self.about_panel, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        scroll_frame.grid_columnconfigure(0, weight=1)
        self.about_panel.grid_rowconfigure(0, weight=1)
        
        # App Header
        app_title = ctk.CTkLabel(
            scroll_frame,
            text="ShamaOllama",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        app_title.grid(row=0, column=0, pady=(0, 5))
        
        # Add the ShamaOllama icon image
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "images", "icons", "ShamaOllama_Icon.png")
            if os.path.exists(icon_path):
                # Load and display the PNG image
                icon_image = ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    dark_image=Image.open(icon_path),
                    size=(128, 128)  # Larger size for about page
                )
                icon_label = ctk.CTkLabel(scroll_frame, image=icon_image, text="")
                icon_label.grid(row=1, column=0, pady=10)
        except Exception:
            # If image loading fails, continue without image
            pass
        
        version_label = ctk.CTkLabel(
            scroll_frame,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=14)
        )
        version_label.grid(row=2, column=0, pady=(0, 20))
        
        # Homage section
        homage_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray90", "gray10"))
        homage_frame.grid(row=3, column=0, pady=10, padx=20, sticky="ew")
        homage_frame.grid_columnconfigure(0, weight=1)
        
        homage_title = ctk.CTkLabel(
            homage_frame,
            text="🎬 Animal House Homage",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        homage_title.grid(row=0, column=0, pady=(10, 5))
        
        homage_text = ctk.CTkLabel(
            homage_frame,
            text='Paying tribute to "Shama Lama Ding Dong" from the classic\ncomedy Animal House (1978) - a song that brought joy to generations!',
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        homage_text.grid(row=1, column=0, pady=(0, 10), padx=20)
        
        # Cultural significance section
        cultural_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray90", "gray10"))
        cultural_frame.grid(row=4, column=0, pady=10, padx=20, sticky="ew")
        cultural_frame.grid_columnconfigure(0, weight=1)
        
        cultural_title = ctk.CTkLabel(
            cultural_frame,
            text="🌍 Cultural Significance of 'Shama'",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cultural_title.grid(row=0, column=0, pady=(10, 10))
        
        cultural_meanings = [
            "• Sanskrit: Equanimity, calmness, peace of mind",
            "• Hebrew: To listen, to hear, to understand", 
            "• Persian: Candle, enlightenment, the light of knowledge"
        ]
        
        for i, meaning in enumerate(cultural_meanings):
            meaning_label = ctk.CTkLabel(
                cultural_frame,
                text=meaning,
                font=ctk.CTkFont(size=12),
                justify="left",
                anchor="w"
            )
            meaning_label.grid(row=i+1, column=0, pady=2, padx=20, sticky="w")
        
        # Perfect fit text
        fit_label = ctk.CTkLabel(
            cultural_frame,
            text="These meanings perfectly embody our vision for AI interaction:\nbalanced, responsive, and enlightening.",
            font=ctk.CTkFont(size=12, weight="bold"),
            justify="center"
        )
        fit_label.grid(row=len(cultural_meanings)+1, column=0, pady=(10, 10), padx=20)
        
        # Author and project info
        info_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray90", "gray10"))
        info_frame.grid(row=5, column=0, pady=10, padx=20, sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1)
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="📝 Project Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_title.grid(row=0, column=0, pady=(10, 10))
        
        author_label = ctk.CTkLabel(
            info_frame,
            text="Author: John Blancuzzi\nEmail: john@blancuzzi.org\nLicense: MIT License",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        author_label.grid(row=1, column=0, pady=(0, 10), padx=20)
        
        # Donation section
        donation_frame = ctk.CTkFrame(scroll_frame, fg_color=("lightblue", "darkblue"))
        donation_frame.grid(row=6, column=0, pady=20, padx=20, sticky="ew")
        donation_frame.grid_columnconfigure(0, weight=1)
        
        donation_title = ctk.CTkLabel(
            donation_frame,
            text="💖 Support ShamaOllama Development",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        donation_title.grid(row=0, column=0, pady=(15, 10))
        
        donation_text = ctk.CTkLabel(
            donation_frame,
            text="If ShamaOllama has been helpful to you, consider supporting its development!\nYour contributions help keep this project free and open source.",
            font=ctk.CTkFont(size=12),
            justify="center",
            text_color="white"
        )
        donation_text.grid(row=1, column=0, pady=(0, 10), padx=20)
        
        # Donation buttons
        button_frame = ctk.CTkFrame(donation_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=(0, 15))
        
        github_sponsor_btn = ctk.CTkButton(
            button_frame,
            text="💕 GitHub Sponsors",
            command=lambda: self.open_url("https://github.com/sponsors/BlancuzziJ"),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("pink", "darkred"),
            hover_color=("lightpink", "red")
        )
        github_sponsor_btn.grid(row=0, column=0, padx=10, pady=5)
        
        github_repo_btn = ctk.CTkButton(
            button_frame,
            text="⭐ Star on GitHub",
            command=lambda: self.open_url("https://github.com/BlancuzziJ/Ollama-GUI"),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("gray", "darkgray"),
            hover_color=("lightgray", "gray")
        )
        github_repo_btn.grid(row=0, column=1, padx=10, pady=5)
        
        # Appreciation message
        thanks_label = ctk.CTkLabel(
            scroll_frame,
            text="Thank you for using ShamaOllama! 🙏\nBuilt with ❤️ for the AI community",
            font=ctk.CTkFont(size=14, weight="bold"),
            justify="center"
        )
        thanks_label.grid(row=6, column=0, pady=20)
    
    def open_url(self, url):
        """Open URL in the default web browser - fast, direct"""
        # Direct open for speed - browsers handle security
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {e}")
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_frame = ctk.CTkFrame(self.root, height=30, corner_radius=0)
        self.status_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=(0, 10))
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.connection_label = ctk.CTkLabel(
            self.status_frame,
            text="⚫ Disconnected",
            font=ctk.CTkFont(size=12)
        )
        self.connection_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
    # Navigation methods
    def show_panel(self, panel_name: str):
        """Show specific panel and update navigation"""
        # Hide all panels
        for panel in [self.chat_panel, self.models_panel, self.history_panel, self.system_panel, self.settings_panel, self.about_panel]:
            panel.grid_remove()
        
        # Reset button colors
        for btn in self.nav_buttons.values():
            btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Show selected panel
        if panel_name == "chat":
            self.chat_panel.grid(row=0, column=0, sticky="nsew")
            self.nav_buttons["Chat"].configure(fg_color=("gray75", "gray25"))
        elif panel_name == "models":
            self.models_panel.grid(row=0, column=0, sticky="nsew")
            self.nav_buttons["Models"].configure(fg_color=("gray75", "gray25"))
            self.refresh_models_display()
        elif panel_name == "history":
            self.history_panel.grid(row=0, column=0, sticky="nsew")
            self.nav_buttons["History"].configure(fg_color=("gray75", "gray25"))
            self.refresh_history_display()
        elif panel_name == "system":
            self.system_panel.grid(row=0, column=0, sticky="nsew")
            self.nav_buttons["System"].configure(fg_color=("gray75", "gray25"))
            self.refresh_system_info()
        elif panel_name == "settings":
            self.settings_panel.grid(row=0, column=0, sticky="nsew")
            self.nav_buttons["Settings"].configure(fg_color=("gray75", "gray25"))
        elif panel_name == "about":
            self.about_panel.grid(row=0, column=0, sticky="nsew")
            self.nav_buttons["About"].configure(fg_color=("gray75", "gray25"))
        
        self.current_panel = panel_name
    
    def show_chat(self):
        """Show chat panel"""
        self.show_panel("chat")
    
    def show_models(self):
        """Show models panel"""
        self.show_panel("models")
    
    def show_history(self):
        """Show history panel"""
        self.show_panel("history")
    
    def show_system(self):
        """Show system information panel"""
        self.show_panel("system")
    
    def show_settings(self):
        """Show settings panel"""
        self.show_panel("settings")
    
    def show_about(self):
        """Show about panel"""
        self.show_panel("about")
    
    def show_thinking_info(self):
        """Show information about the thinking models feature"""
        info_text = """Thinking Models Feature

Some AI models like DeepSeek show their "thinking" or reasoning process before providing the final answer. This can be helpful for understanding how the model arrived at its conclusion, but it can also make responses longer and slower to read.

When this option is enabled:
• The thinking/reasoning blocks will be filtered out
• You'll see only the final answer
• Responses will appear cleaner and more concise

Common thinking block patterns that will be hidden:
• <think>...</think> (DeepSeek style)
• <thinking>...</thinking>
• [thinking]...[/thinking]  
• **Thinking:** sections
• **Answer:** sections (keeps the answer content)

Note: This feature works best with models specifically designed to show thinking processes. Regular models are not affected by this setting."""

        messagebox.showinfo("Thinking Models Feature", info_text)

    # Core functionality methods
    def check_connection(self):
        """Check Ollama connection status"""
        def check():
            is_connected = self.api.test_connection()
            if is_connected:
                self.connection_label.configure(text="🟢 Connected", text_color="green")
                self.status_label.configure(text="Connected to Ollama")
            else:
                self.connection_label.configure(text="🔴 Disconnected", text_color="red")
                self.status_label.configure(text="Cannot connect to Ollama")
            
            # Schedule next check
            self.root.after(10000, self.check_connection)  # Check every 10 seconds
        
        threading.Thread(target=check, daemon=True).start()

    def refresh_models(self):
        """Refresh the list of available models"""
        def refresh():
            try:
                self.models = self.api.get_models()
                model_names = [model['name'] for model in self.models] if self.models else ["No models available"]
                
                # Update dropdown
                self.root.after(0, lambda: self.model_dropdown.configure(values=model_names))
                
                if self.models and not self.current_model:
                    self.root.after(0, lambda: self.model_dropdown.set(model_names[0]))
                    self.current_model = model_names[0]
                
                self.root.after(0, lambda: self.status_label.configure(text=f"Found {len(self.models)} models"))
            except Exception as e:
                self.root.after(0, lambda: self.status_label.configure(text=f"Error loading models: {str(e)}"))
        
        threading.Thread(target=refresh, daemon=True).start()

    def refresh_models_display(self):
        """Refresh the models display with checkbox selection"""
        # Clear existing checkboxes
        for widget in self.models_scroll_frame.winfo_children():
            widget.destroy()
        
        self.model_checkboxes.clear()
        self.model_info_labels.clear()
        self.selected_models.clear()
        
        if not self.models:
            no_models_label = ctk.CTkLabel(
                self.models_scroll_frame,
                text="🚫 No models available\nPull a model to get started!",
                font=ctk.CTkFont(size=14),
                justify="center"
            )
            no_models_label.grid(row=0, column=0, padx=20, pady=20)
            self.models_count_label.configure(text="0 models")
        else:
            for i, model in enumerate(self.models):
                self.create_model_entry(i, model)
            
            self.models_count_label.configure(text=f"{len(self.models)} models")
        
        # Reset select all checkbox
        self.select_all_var.set(False)
    
    def refresh_system_info(self):
        """Refresh system information display"""
        try:
            # Get GPU information
            gpu_info = get_gpu_info()
            
            # Format for display
            info_text = format_gpu_info_for_display(gpu_info)
            
            # Update display
            self.system_info_display.configure(state="normal")
            self.system_info_display.delete("1.0", "end")
            self.system_info_display.insert("1.0", info_text)
            self.system_info_display.configure(state="disabled")
            
        except Exception as e:
            error_text = f"❌ Error getting system information:\n{str(e)}\n\nThis may be due to missing dependencies.\nTry running: pip install -r requirements-gpu.txt"
            self.system_info_display.configure(state="normal")
            self.system_info_display.delete("1.0", "end")
            self.system_info_display.insert("1.0", error_text)
            self.system_info_display.configure(state="disabled")
    
    def create_model_entry(self, index: int, model: Dict):
        """Create a model entry with checkbox and info"""
        name = model['name']
        size = model.get('size', 0)
        size_mb = size / (1024 * 1024) if size else 0
        size_gb = size_mb / 1024 if size_mb > 1024 else 0
        modified = model.get('modified_at', 'Unknown')
        
        # Model frame
        model_frame = ctk.CTkFrame(self.models_scroll_frame)
        model_frame.grid(row=index, column=0, padx=5, pady=2, sticky="ew")
        model_frame.grid_columnconfigure(1, weight=1)
        self.models_scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Checkbox
        var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            model_frame,
            text="",
            variable=var,
            command=lambda: self.on_model_selected(name, var.get()),
            width=20
        )
        checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.model_checkboxes[name] = (checkbox, var)
        
        # Model info frame
        info_frame = ctk.CTkFrame(model_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Model name and tags
        name_parts = name.split(':')
        base_name = name_parts[0]
        tag = ':' + name_parts[1] if len(name_parts) > 1 else ':latest'
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"📦 {base_name}",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="ew")
        
        tag_label = ctk.CTkLabel(
            info_frame,
            text=f"🏷️ {tag}",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        tag_label.grid(row=1, column=0, sticky="ew")
        
        # Size and date info
        if size_gb > 1:
            size_text = f"💾 {size_gb:.1f} GB"
        else:
            size_text = f"💾 {size_mb:.1f} MB"
            
        size_label = ctk.CTkLabel(
            info_frame,
            text=size_text,
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        size_label.grid(row=0, column=1, padx=10, sticky="e")
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=f"📅 {modified[:10] if modified != 'Unknown' else 'Unknown'}",
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        date_label.grid(row=1, column=1, padx=10, sticky="e")
        
        self.model_info_labels[name] = {
            'frame': model_frame,
            'name': name_label,
            'tag': tag_label,
            'size': size_label,
            'date': date_label
        }
    
    def on_model_selected(self, model_name: str, selected: bool):
        """Handle model selection/deselection"""
        if selected:
            self.selected_models.add(model_name)
        else:
            self.selected_models.discard(model_name)
        
        # Update select all checkbox
        if len(self.selected_models) == len(self.models):
            self.select_all_var.set(True)
        else:
            self.select_all_var.set(False)
    
    def toggle_select_all(self):
        """Toggle selection of all models"""
        select_all = self.select_all_var.get()
        
        for name, (checkbox, var) in self.model_checkboxes.items():
            var.set(select_all)
            if select_all:
                self.selected_models.add(name)
            else:
                self.selected_models.discard(name)

    def refresh_history_display(self):
        """Refresh the history display"""
        self.history_listbox.configure(state="normal")
        self.history_listbox.delete("1.0", "end")
        
        if not self.chat_manager.chat_history:
            self.history_listbox.insert("1.0", "No chat history available.")
        else:
            for i, session in enumerate(self.chat_manager.chat_history):
                title = session['title']
                timestamp = session['timestamp'][:16].replace('T', ' ')
                message_count = len(session['messages'])
                
                self.history_listbox.insert("end", f"{i+1}. {title}\n")
                self.history_listbox.insert("end", f"   Date: {timestamp}\n")
                self.history_listbox.insert("end", f"   Messages: {message_count}\n\n")
        
        self.history_listbox.configure(state="disabled")

    def on_model_dropdown_selected(self, model_name: str):
        """Handle model selection from dropdown"""
        if model_name != "No models available":
            self.current_model = model_name
            self.status_label.configure(text=f"Selected model: {model_name}")
            self.add_chat_message("System", f"Switched to model: {model_name}", "system")

    def new_chat(self):
        """Start a new chat session"""
        if self.chat_manager.current_session and self.autosave_var.get():
            self.chat_manager.save_session()
        
        self.chat_manager.new_session()
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        
        self.add_chat_message("System", "New chat session started. How can I help you?", "system")
        self.status_label.configure(text="New chat session started")

    def add_chat_message(self, role: str, content: str, msg_type: str = "normal"):
        """Add a message to the chat display"""
        self.chat_display.configure(state="normal")
        
        # Add timestamp and role
        timestamp = datetime.now().strftime("%H:%M")
        
        if msg_type == "system":
            self.chat_display.insert("end", f"[{timestamp}] System: ", "system_role")
            self.chat_display.insert("end", f"{content}\n\n", "system_msg")
        elif role == "user":
            self.chat_display.insert("end", f"[{timestamp}] You: ", "user_role")
            self.chat_display.insert("end", f"{content}\n\n", "user_msg")
        else:  # assistant
            model_name = self.current_model or "Assistant"
            self.chat_display.insert("end", f"[{timestamp}] {model_name}: ", "assistant_role")
            self.chat_display.insert("end", f"{content}\n\n", "assistant_msg")
        
        # Configure text tags for styling
        self.chat_display.tag_config("system_role", foreground="#888888")
        self.chat_display.tag_config("system_msg", foreground="#888888")
        self.chat_display.tag_config("user_role", foreground="#4A9EFF")
        self.chat_display.tag_config("user_msg", foreground="#FFFFFF")
        self.chat_display.tag_config("assistant_role", foreground="#50C878")
        self.chat_display.tag_config("assistant_msg", foreground="#FFFFFF")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def send_message(self):
        """Send a message to the AI with security validation"""
        if self.is_chatting:
            return
        
        if not self.current_model:
            messagebox.showwarning("No Model", "Please select a model first.")
            return
        
        # Get and validate message
        message = self.message_input.get("1.0", "end-1c").strip()
        if not message:
            return
            
        # Fast path - send directly to Ollama
        # Clear input immediately for responsive feel
        self.message_input.delete("1.0", "end")
        
        # Add user message
        self.add_chat_message("user", message)
        self.chat_manager.add_message("user", message, self.current_model)
        
        # Disable send button and show streaming status
        self.is_chatting = True
        self.typing_animation_active = True
        self.animate_typing_indicator()
        self.status_label.configure(text="Generating response...")
        
        # Prepare streaming response
        self.current_response = ""
        self.response_start_pos = None
        self.first_token_received = False
        
        def chat_thread():
            try:
                # Prepare messages for API
                messages = self.chat_manager.get_messages_for_api()
                
                # Initialize streaming response in UI
                self.root.after(0, self.start_streaming_response)
                
                # Send request with streaming
                def stream_callback(chunk):
                    self.current_response += chunk
                    self.root.after(0, lambda c=chunk: self.update_streaming_response(c))
                
                full_response = self.api.chat(self.current_model, messages, stream_callback, self.hide_thinking_var.get())
                
                # If streaming didn't work (empty response), fall back to regular chat
                if not full_response and not self.current_response:
                    # Fallback to non-streaming
                    self.root.after(0, lambda: self.status_label.configure(text="Fallback to non-streaming mode..."))
                    full_response = self.api.chat(self.current_model, messages, None, self.hide_thinking_var.get())
                    self.root.after(0, lambda: self.add_chat_message("assistant", full_response))
                    self.chat_manager.add_message("assistant", full_response, self.current_model)
                else:
                    # Streaming worked, use the accumulated response
                    if self.current_response:
                        full_response = self.current_response
                    self.chat_manager.add_message("assistant", full_response, self.current_model)
                
                # Re-enable send button
                self.root.after(0, self.finish_chat_response)
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.root.after(0, lambda: self.add_chat_message("System", error_msg, "system"))
                self.root.after(0, self.finish_chat_response)
        
        threading.Thread(target=chat_thread, daemon=True).start()

    def animate_typing_indicator(self):
        """Animate the typing indicator on the send button"""
        if not self.typing_animation_active:
            return
        
        indicators = ["●", "● ●", "● ● ●", "● ●", "●", "", ""]
        current_time = int(time.time() * 2) % len(indicators)  # Change every 0.5 seconds
        
        self.send_btn.configure(text=indicators[current_time], state="disabled")
        
        # Schedule next update
        self.root.after(500, self.animate_typing_indicator)

    def start_streaming_response(self):
        """Initialize the streaming response in the chat display"""
        self.chat_display.configure(state="normal")
        
        # Add timestamp and role for assistant
        timestamp = datetime.now().strftime("%H:%M")
        model_name = self.current_model or "Assistant"
        
        self.chat_display.insert("end", f"[{timestamp}] {model_name}: ", "assistant_role")
        
        # Mark the start position for the response
        self.response_start_pos = self.chat_display.index("end-1c")
        
        # Configure text tags for styling
        self.chat_display.tag_config("assistant_role", foreground="#50C878")
        self.chat_display.tag_config("assistant_msg_streaming", foreground="#FFFFFF")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def update_streaming_response(self, chunk):
        """Update the streaming response with new chunk"""
        if chunk and self.response_start_pos:
            # If this is the first token, stop the typing animation
            if not self.first_token_received:
                self.first_token_received = True
                self.typing_animation_active = False
                self.send_btn.configure(text="📝 Streaming", state="disabled")
            
            self.chat_display.configure(state="normal")
            
            # Insert the new chunk at the current end
            self.chat_display.insert("end", chunk, "assistant_msg_streaming")
            
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")
            
            # Update status to show streaming with character count and words per minute estimate
            response_length = len(self.current_response)
            word_count = len(self.current_response.split())
            self.status_label.configure(text=f"📝 Streaming... {word_count} words ({response_length} chars)")

    def finish_streaming_response(self):
        """Finish the streaming response and add final formatting"""
        if self.response_start_pos:
            self.chat_display.configure(state="normal")
            
            # Add final newlines for proper spacing
            self.chat_display.insert("end", "\n\n")
            
            # Apply final styling to the complete response
            end_pos = self.chat_display.index("end-3c")  # Before the newlines
            self.chat_display.tag_add("assistant_msg", self.response_start_pos, end_pos)
            self.chat_display.tag_config("assistant_msg", foreground="#FFFFFF")
            
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")
        
        # Reset streaming variables
        self.current_response = ""
        self.response_start_pos = None
        self.first_token_received = False

    def finish_chat_response(self):
        """Re-enable chat interface after response"""
        # Stop typing animation
        self.typing_animation_active = False
        
        # Complete the streaming response formatting
        self.finish_streaming_response()
        
        # Re-enable interface
        self.is_chatting = False
        self.send_btn.configure(text="Send", state="normal")
        self.status_label.configure(text="Ready")

    def pull_model(self):
        """Pull a new model with enhanced progress tracking"""
        model_name = self.pull_entry.get().strip()
        if not model_name:
            messagebox.showwarning("No Model", "Please enter a model name.")
            return
        
        # Validate model name
        if not security.validate_model_name(model_name):
            messagebox.showerror("Invalid Model", "Invalid model name. Please use only alphanumeric characters, hyphens, underscores, colons, and dots.")
            return
        
        self.pull_btn.configure(text="Pulling...", state="disabled")
        self.progress_label.configure(text=f"Initializing pull for {model_name}...")
        self.progress_bar.set(0)
        self.progress_percentage.configure(text="0%")
        
        def pull_thread():
            try:
                def progress_callback(data):
                    status = data.get('status', '')
                    
                    if 'total' in data and 'completed' in data and data['total'] > 0:
                        progress = data['completed'] / data['total']
                        percentage = int(progress * 100)
                        self.root.after(0, lambda: self.progress_bar.set(progress))
                        self.root.after(0, lambda: self.progress_percentage.configure(text=f"{percentage}%"))
                    
                    # Update status text
                    if status == 'pulling manifest':
                        display_status = "📥 Downloading manifest"
                    elif status == 'downloading':
                        display_status = "📦 Downloading model"
                    elif status == 'verifying sha256 digest':
                        display_status = "🔍 Verifying integrity"
                    elif status == 'writing manifest':
                        display_status = "💾 Writing manifest"
                    elif status == 'removing any unused layers':
                        display_status = "🧹 Cleaning up"
                    elif status == 'success':
                        display_status = "✅ Pull completed"
                    else:
                        display_status = f"🔄 {status}"
                    
                    self.root.after(0, lambda: self.progress_label.configure(text=display_status))
                
                security.log_security_event("Model pull started", {"model": model_name})
                success = self.api.pull_model(model_name, progress_callback)
                
                if success:
                    self.root.after(0, lambda: self.progress_label.configure(text=f"✅ Successfully pulled {model_name}"))
                    self.root.after(0, lambda: self.progress_percentage.configure(text="100%"))
                    self.root.after(0, self.refresh_models)
                    self.root.after(0, lambda: self.pull_entry.delete(0, "end"))
                    self.root.after(0, lambda: messagebox.showinfo("Success", f"Model '{model_name}' has been pulled successfully!"))
                    security.log_security_event("Model pull completed", {"model": model_name})
                else:
                    self.root.after(0, lambda: self.progress_label.configure(text=f"❌ Failed to pull {model_name}"))
                    self.root.after(0, lambda: messagebox.showerror("Pull Failed", f"Failed to pull model '{model_name}'. Please check the model name and try again."))
                    security.log_security_event("Model pull failed", {"model": model_name})
                
            except Exception as e:
                error_msg = f"Error pulling model: {str(e)}"
                self.root.after(0, lambda: self.progress_label.configure(text="❌ Pull error"))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                security.log_security_event("Model pull error", {"model": model_name, "error": str(e)})
            finally:
                self.root.after(0, lambda: self.pull_btn.configure(text="Pull Model", state="normal"))
                self.root.after(0, lambda: self.progress_bar.set(0))
                self.root.after(0, lambda: self.progress_percentage.configure(text=""))
        
        threading.Thread(target=pull_thread, daemon=True).start()

    def delete_selected_models(self):
        """Delete selected models with confirmation"""
        if not self.selected_models:
            messagebox.showwarning("No Selection", "Please select models to delete.")
            return
        
        # Confirm deletion
        model_list = '\n'.join([f"• {model}" for model in sorted(self.selected_models)])
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the following models?\n\n{model_list}\n\nThis action cannot be undone."
        )
        
        if not result:
            return
        
        def delete_models():
            deleted_count = 0
            failed_models = []
            
            for model_name in list(self.selected_models):
                self.root.after(0, lambda m=model_name: self.progress_label.configure(text=f"Deleting {m}..."))
                
                if self.api.delete_model(model_name):
                    deleted_count += 1
                    security.log_security_event("Model deleted", {"model": model_name})
                else:
                    failed_models.append(model_name)
                    security.log_security_event("Model deletion failed", {"model": model_name})
            
            # Update UI
            self.root.after(0, self.refresh_models)
            
            if failed_models:
                self.root.after(0, lambda: messagebox.showwarning(
                    "Deletion Incomplete",
                    f"Deleted {deleted_count} models successfully.\nFailed to delete: {', '.join(failed_models)}"
                ))
            else:
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"Successfully deleted {deleted_count} models."
                ))
            
            self.root.after(0, lambda: self.progress_label.configure(text="Ready"))
        
        threading.Thread(target=delete_models, daemon=True).start()
    
    def quick_pull_model(self, model_name: str):
        """Quick pull for popular models"""
        self.pull_entry.delete(0, "end")
        self.pull_entry.insert(0, model_name)
        self.pull_model()
    
    def copy_selected_model_names(self):
        """Copy selected model names to clipboard"""
        if not self.selected_models:
            messagebox.showwarning("No Selection", "Please select models to copy.")
            return
        
        model_names = '\n'.join(sorted(self.selected_models))
        self.root.clipboard_clear()
        self.root.clipboard_append(model_names)
        messagebox.showinfo("Copied", f"Copied {len(self.selected_models)} model names to clipboard.")
    
    def show_selected_model_info(self):
        """Show detailed information about selected models"""
        if not self.selected_models:
            messagebox.showwarning("No Selection", "Please select models to view info.")
            return
        
        # Create info window
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Model Information - ShamaOllama")
        info_window.geometry("700x500")
        
        # Info display
        info_text = ctk.CTkTextbox(info_window, wrap="word", font=ctk.CTkFont(family="Courier", size=11))
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Gather info for selected models
        info_content = f"📊 Model Information Report\n{'='*50}\n\n"
        
        for model_name in sorted(self.selected_models):
            model_info = next((m for m in self.models if m['name'] == model_name), None)
            if model_info:
                size = model_info.get('size', 0)
                size_gb = size / (1024 * 1024 * 1024) if size else 0
                modified = model_info.get('modified_at', 'Unknown')
                
                info_content += f"📦 {model_name}\n"
                info_content += f"   Size: {size_gb:.2f} GB ({size:,} bytes)\n"
                info_content += f"   Modified: {modified}\n"
                info_content += f"   Digest: {model_info.get('digest', 'N/A')[:20]}...\n"
                info_content += f"   Parent: {model_info.get('parent_model', 'N/A')}\n"
                info_content += f"   Format: {model_info.get('format', 'N/A')}\n"
                info_content += f"   Family: {model_info.get('family', 'N/A')}\n\n"
        
        total_size = sum(m.get('size', 0) for m in self.models if m['name'] in self.selected_models)
        total_gb = total_size / (1024 * 1024 * 1024)
        info_content += f"📈 Summary:\n"
        info_content += f"   Selected Models: {len(self.selected_models)}\n"
        info_content += f"   Total Size: {total_gb:.2f} GB\n"
        
        info_text.insert("1.0", info_content)
        info_text.configure(state="disabled")
    
    def manage_model_tags(self):
        """Manage model tags and versions"""
        if not self.selected_models:
            messagebox.showwarning("No Selection", "Please select models to manage tags.")
            return
        
        # Create tag management window
        tag_window = ctk.CTkToplevel(self.root)
        tag_window.title("Model Tag Manager - ShamaOllama")
        tag_window.geometry("600x400")
        
        # Header
        header = ctk.CTkLabel(
            tag_window,
            text=f"🏷️ Managing tags for {len(self.selected_models)} models",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.pack(pady=10)
        
        # Instructions
        instructions = ctk.CTkLabel(
            tag_window,
            text="Tag Management Features:\n• View model hierarchies\n• Identify tag relationships\n• Plan cleanup operations",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=5)
        
        # Model list with tag info
        tag_frame = ctk.CTkScrollableFrame(tag_window, height=250)
        tag_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for i, model_name in enumerate(sorted(self.selected_models)):
            model_frame = ctk.CTkFrame(tag_frame)
            model_frame.pack(fill="x", padx=5, pady=2)
            
            name_parts = model_name.split(':')
            base_name = name_parts[0]
            tag = name_parts[1] if len(name_parts) > 1 else 'latest'
            
            ctk.CTkLabel(
                model_frame,
                text=f"📦 {base_name}:{tag}",
                font=ctk.CTkFont(weight="bold"),
                anchor="w"
            ).pack(side="left", padx=10, pady=5)
            
            # Find related models
            related = [m['name'] for m in self.models if m['name'].startswith(base_name + ':')]
            if len(related) > 1:
                ctk.CTkLabel(
                    model_frame,
                    text=f"🔗 {len(related)} variants",
                    font=ctk.CTkFont(size=10),
                    anchor="e"
                ).pack(side="right", padx=10, pady=5)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(tag_window)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📋 Export Tag Report",
            command=lambda: self.export_tag_report(list(self.selected_models))
        ).pack(side="left", padx=5, pady=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh Models",
            command=lambda: [tag_window.destroy(), self.refresh_models()]
        ).pack(side="right", padx=5, pady=5)
    
    def export_tag_report(self, model_names: List[str]):
        """Export a detailed tag report"""
        filename = filedialog.asksaveasfilename(
            title="Export Tag Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("ShamaOllama Model Tag Report\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Models analyzed: {len(model_names)}\n\n")
                    
                    for model_name in sorted(model_names):
                        model_info = next((m for m in self.models if m['name'] == model_name), None)
                        if model_info:
                            f.write(f"Model: {model_name}\n")
                            f.write(f"Size: {model_info.get('size', 0) / (1024**3):.2f} GB\n")
                            f.write(f"Modified: {model_info.get('modified_at', 'Unknown')}\n")
                            f.write(f"Digest: {model_info.get('digest', 'N/A')}\n")
                            f.write("-" * 30 + "\n")
                
                messagebox.showinfo("Export Success", f"Tag report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Failed to export tag report: {e}")
    
    def delete_selected_model(self):
        """Legacy method - redirects to new delete_selected_models"""
        self.delete_selected_models()

    def load_selected_session(self):
        """Load a selected chat session"""
        messagebox.showinfo("Feature", "Session loading feature coming soon!")

    def export_selected_session(self):
        """Export a selected chat session"""
        if not self.chat_manager.current_session:
            messagebox.showwarning("No Session", "No active session to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Chat Session",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.chat_manager.export_session(filename)
                messagebox.showinfo("Success", f"Session exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")

    def clear_history(self):
        """Clear all chat history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all chat history?"):
            self.chat_manager.chat_history = []
            self.chat_manager.save_history()
            self.refresh_history_display()
            self.status_label.configure(text="Chat history cleared")

    def test_connection_manual(self):
        """Test connection manually from settings with security validation"""
        url = self.url_entry.get().strip()
        
        # Validate URL
        if not security.validate_url(url):
            security.log_security_event("Invalid URL in settings", {"url": url})
            messagebox.showerror(
                "Invalid URL", 
                "The provided URL is not valid or safe. Please enter a valid Ollama URL."
            )
            return
        
        if url:
            self.api.base_url = url
        
        def test():
            is_connected = self.api.test_connection()
            if is_connected:
                self.root.after(0, lambda: messagebox.showinfo("Success", "Connection successful!"))
                security.log_security_event("Manual connection test successful", {"url": url})
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "Cannot connect to Ollama"))
                security.log_security_event("Manual connection test failed", {"url": url})
        
        threading.Thread(target=test, daemon=True).start()

    def save_settings(self):
        """Save application settings"""
        # Update API URL
        url = self.url_entry.get().strip()
        if url:
            self.api.base_url = url
        
        # Save settings to file
        settings = {
            "ollama_url": self.api.base_url,
            "auto_save": self.autosave_var.get(),
            "max_history": self.max_history_entry.get()
        }
        
        try:
            settings_file = self.chat_manager.data_dir / "settings.json"
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.status_label.configure(text="Settings saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="☀️ Light Theme")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="🌙 Dark Theme")

    def view_security_logs(self):
        """View security logs in a new window"""
        try:
            log_file = Path.home() / '.shamollama' / 'logs' / 'security.log'
            if not log_file.exists():
                messagebox.showinfo("Security Logs", "No security logs found.")
                return
            
            # Create log viewer window
            log_window = ctk.CTkToplevel(self.root)
            log_window.title("Security Logs - ShamaOllama")
            log_window.geometry("800x600")
            
            # Log display
            log_text = ctk.CTkTextbox(log_window, wrap="word", font=ctk.CTkFont(family="Courier", size=10))
            log_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Read and display logs
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
                log_text.insert("1.0", log_content)
                log_text.configure(state="disabled")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view security logs: {e}")
    
    def clear_security_logs(self):
        """Clear security logs after confirmation"""
        result = messagebox.askyesno(
            "Clear Security Logs",
            "Are you sure you want to clear all security logs? This action cannot be undone."
        )
        
        if result:
            try:
                success = security.clear_logs()
                if success:
                    messagebox.showinfo("Success", "Security logs cleared successfully.")
                    # Try to log the clearing event, but don't fail if it doesn't work
                    try:
                        security.log_security_event("Security logs cleared", {"user_action": True})
                    except:
                        pass  # Ignore logging errors after clearing
                else:
                    messagebox.showerror("Error", "Failed to clear security logs. The log file may be in use.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear security logs: {str(e)}")

    def on_closing(self):
        """Handle application closing"""
        if self.chat_manager.current_session and self.autosave_var.get():
            self.chat_manager.save_session()
        
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ShamaOllamaGUI()
    app.run()
