"""
Core functionality methods for OllamaGUI - Part 2
This file contains the remaining methods for the main application
"""

import threading
from datetime import datetime
import json
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk

# GPU information for local AI recommendations
try:
    from gpu_info import get_gpu_info, format_gpu_info_for_display, check_gpu_dependencies, get_dependency_install_message
    GPU_INFO_AVAILABLE = True
except ImportError:
    GPU_INFO_AVAILABLE = False

# Add these methods to the OllamaGUI class in main.py

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
            error_msg = str(e)
            self.root.after(0, lambda: self.status_label.configure(text=f"Error loading models: {error_msg}"))
    
    threading.Thread(target=refresh, daemon=True).start()

def refresh_models_display(self):
    """Refresh the models display in the models panel"""
    self.models_listbox.configure(state="normal")
    self.models_listbox.delete("1.0", "end")
    
    if not self.models:
        self.models_listbox.insert("1.0", "No models available. Pull a model to get started.")
    else:
        for i, model in enumerate(self.models):
            name = model['name']
            size = model.get('size', 0)
            size_mb = size / (1024 * 1024) if size else 0
            modified = model.get('modified_at', 'Unknown')
            
            self.models_listbox.insert("end", f"{i+1}. {name}\n")
            self.models_listbox.insert("end", f"   Size: {size_mb:.1f} MB\n")
            self.models_listbox.insert("end", f"   Modified: {modified[:10]}\n\n")
    
    self.models_listbox.configure(state="disabled")

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

def on_model_selected(self, model_name: str):
    """Handle model selection"""
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
    """Send a message to the AI"""
    if self.is_chatting:
        return
    
    if not self.current_model:
        messagebox.showwarning("No Model", "Please select a model first.")
        return
    
    # Get message
    message = self.message_input.get("1.0", "end-1c").strip()
    if not message:
        return
    
    # Clear input
    self.message_input.delete("1.0", "end")
    
    # Add user message
    self.add_chat_message("user", message)
    self.chat_manager.add_message("user", message, self.current_model)
    
    # Disable send button
    self.is_chatting = True
    self.send_btn.configure(text="Thinking...", state="disabled")
    self.status_label.configure(text="Generating response...")
    
    def chat_thread():
        try:
            # Prepare messages for API
            messages = self.chat_manager.get_messages_for_api()
            
            # Stream response
            response_text = ""
            def stream_callback(chunk):
                nonlocal response_text
                response_text += chunk
                # Update display in real-time
                self.root.after(0, self.update_streaming_response, response_text)
            
            # Send request
            full_response = self.api.chat(self.current_model, messages, stream_callback)
            
            # Add to chat manager
            self.chat_manager.add_message("assistant", full_response, self.current_model)
            
            # Re-enable send button
            self.root.after(0, self.finish_chat_response)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.add_chat_message("System", error_msg, "system"))
            self.root.after(0, self.finish_chat_response)
    
    threading.Thread(target=chat_thread, daemon=True).start()

def update_streaming_response(self, response_text: str):
    """Update the streaming response in real-time"""
    # This is a simplified version - you might want to implement proper streaming display
    pass

def finish_chat_response(self):
    """Re-enable chat interface after response"""
    self.is_chatting = False
    self.send_btn.configure(text="Send", state="normal")
    self.status_label.configure(text="Ready")

def pull_model(self):
    """Pull a new model"""
    model_name = self.pull_entry.get().strip()
    if not model_name:
        messagebox.showwarning("No Model", "Please enter a model name.")
        return
    
    self.pull_btn.configure(text="Pulling...", state="disabled")
    self.progress_label.configure(text=f"Pulling {model_name}...")
    self.progress_bar.set(0)
    
    def pull_thread():
        try:
            def progress_callback(data):
                status = data.get('status', '')
                if 'total' in data and 'completed' in data:
                    progress = data['completed'] / data['total']
                    self.root.after(0, lambda: self.progress_bar.set(progress))
                
                self.root.after(0, lambda: self.progress_label.configure(text=f"{status}..."))
            
            success = self.api.pull_model(model_name, progress_callback)
            
            if success:
                self.root.after(0, lambda: self.progress_label.configure(text=f"Successfully pulled {model_name}"))
                self.root.after(0, self.refresh_models)
                self.root.after(0, lambda: self.pull_entry.delete(0, "end"))
            else:
                self.root.after(0, lambda: self.progress_label.configure(text=f"Failed to pull {model_name}"))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.progress_label.configure(text=f"Error: {error_msg}"))
        finally:
            self.root.after(0, lambda: self.pull_btn.configure(text="Pull", state="normal"))
            self.root.after(0, lambda: self.progress_bar.set(0))
    
    threading.Thread(target=pull_thread, daemon=True).start()

def delete_selected_model(self):
    """Delete the selected model"""
    # This is a simplified version - you'd need to implement model selection
    messagebox.showinfo("Feature", "Model deletion will be implemented with proper selection UI")

def load_selected_session(self):
    """Load a selected chat session"""
    messagebox.showinfo("Feature", "Session loading will be implemented with proper selection UI")

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
    """Test connection manually from settings"""
    url = self.url_entry.get().strip()
    if url:
        self.api.base_url = url
    
    def test():
        is_connected = self.api.test_connection()
        if is_connected:
            self.root.after(0, lambda: messagebox.showinfo("Success", "Connection successful!"))
        else:
            self.root.after(0, lambda: messagebox.showerror("Error", "Cannot connect to Ollama"))
    
    threading.Thread(target=test, daemon=True).start()

def save_settings(self):
    """Save application settings"""
    # Update API URL
    url = self.url_entry.get().strip()
    if url:
        self.api.base_url = url
    
    # Save settings to file (simplified)
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

def show_gpu_info(self):
    """Show GPU information and AI recommendations"""
    if not GPU_INFO_AVAILABLE:
        messagebox.showinfo("GPU Info", 
            "GPU information module not available.\n"
            "The gpu_info.py file may be missing.\n"
            "Please check your installation.")
        return
    
    def load_gpu_info():
        try:
            # Check dependencies first
            deps = check_gpu_dependencies()
            
            gpu_info = get_gpu_info()
            formatted_info = format_gpu_info_for_display(gpu_info)
            
            # Add dependency info if needed
            if not all([deps['GPUtil'], deps['psutil']]):
                dep_message = get_dependency_install_message()
                formatted_info = f"{dep_message}\n\n{'='*50}\n\n{formatted_info}"
            
            # Create info window
            self.root.after(0, lambda: self._show_gpu_info_window(formatted_info))
            
        except Exception as e:
            error_msg = f"Failed to detect GPU information:\n{str(e)}\n\nThis is normal for some systems."
            self.root.after(0, lambda: messagebox.showerror("GPU Detection Error", error_msg))
    
    # Show loading message
    self.status_label.configure(text="Detecting GPU information...")
    threading.Thread(target=load_gpu_info, daemon=True).start()

def _show_gpu_info_window(self, gpu_info_text: str):
    """Display GPU information in a new window"""
    # Create new window
    info_window = ctk.CTkToplevel(self.root)
    info_window.title("GPU Information & AI Recommendations")
    info_window.geometry("800x600")
    info_window.transient(self.root)
    
    # Create scrollable text area
    text_frame = ctk.CTkFrame(info_window)
    text_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    text_widget = ctk.CTkTextbox(text_frame, wrap="word", font=("Consolas", 12))
    text_widget.pack(fill="both", expand=True)
    
    # Insert GPU information
    text_widget.insert("1.0", gpu_info_text)
    text_widget.configure(state="disabled")
    
    # Add buttons
    button_frame = ctk.CTkFrame(info_window)
    button_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    def copy_to_clipboard():
        info_window.clipboard_clear()
        info_window.clipboard_append(gpu_info_text)
        messagebox.showinfo("Copied", "GPU information copied to clipboard!")
    
    copy_btn = ctk.CTkButton(button_frame, text="📋 Copy to Clipboard", command=copy_to_clipboard)
    copy_btn.pack(side="left", padx=10)
    
    close_btn = ctk.CTkButton(button_frame, text="Close", command=info_window.destroy)
    close_btn.pack(side="right", padx=10)
    
    # Center the window
    info_window.focus()
    self.status_label.configure(text="GPU information displayed")

def on_closing(self):
    """Handle application closing"""
    if self.chat_manager.current_session and self.autosave_var.get():
        self.chat_manager.save_session()
    
    self.root.quit()
    self.root.destroy()

# Additional utility methods can be added here as needed
