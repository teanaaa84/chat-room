from customtkinter import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from storage.database_manager import DatabaseManager
from models.user import User
from ui.main_window import ChatApp
import uuid

class LoginWindow(CTk):
    def __init__(self):
        print("LoginWindow: Starting initialization...")
        super().__init__()
        
        print("LoginWindow: Setting window properties...")
        self.title("Messenger - Login")
        self.geometry("400x500")
        self.resizable(False, False)
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        
        print("LoginWindow: Initializing database manager...")
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Current user for session management
        self.current_user = None
        
        print("LoginWindow: Building UI...")
        self.build_ui()
        print("LoginWindow: Initialization complete")
        
    def build_ui(self):
        self.configure(fg_color="#1E1B2E")
        
        # Title
        self.title_label = CTkLabel(
            self, 
            text="Welcome to Messenger", 
            font=("Arial", 24, "bold"), 
            text_color="#BB86FC"
        )
        self.title_label.pack(pady=(40, 20))
        
        # Main frame
        self.main_frame = CTkFrame(self, fg_color="#2C2641", corner_radius=15)
        self.main_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Username field
        self.username_label = CTkLabel(
            self.main_frame, 
            text="Username:", 
            font=("Arial", 14),
            text_color="#FFFFFF"
        )
        self.username_label.pack(pady=(30, 5), padx=20, anchor="w")
        
        self.username_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Enter your username",
            width=300,
            height=40,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.username_entry.pack(pady=(0, 20), padx=20)
        
        # Password field
        self.password_label = CTkLabel(
            self.main_frame, 
            text="Password:", 
            font=("Arial", 14),
            text_color="#FFFFFF"
        )
        self.password_label.pack(pady=(0, 5), padx=20, anchor="w")
        
        self.password_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Enter your password",
            show="*",
            width=300,
            height=40,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.password_entry.pack(pady=(0, 20), padx=20)
        
        # Show/Hide password button
        self.show_password_var = BooleanVar()
        self.show_password_checkbox = CTkCheckBox(
            self.main_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            text_color="#FFFFFF",
            fg_color="#BB86FC",
            hover_color="#9B6CFF"
        )
        self.show_password_checkbox.pack(pady=(0, 20), padx=20, anchor="w")
        
        # Login button
        self.login_button = CTkButton(
            self.main_frame,
            text="Login",
            command=self.login,
            width=300,
            height=45,
            corner_radius=10,
            fg_color="#BB86FC",
            hover_color="#9B6CFF",
            font=("Arial", 14, "bold")
        )
        self.login_button.pack(pady=(0, 20), padx=20)
        
        # Register button
        self.register_button = CTkButton(
            self.main_frame,
            text="Create New Account",
            command=self.show_register,
            width=300,
            height=45,
            corner_radius=10,
            fg_color="#03DAC5",
            hover_color="#018786",
            font=("Arial", 14, "bold")
        )
        self.register_button.pack(pady=(0, 20), padx=20)
        
        # Status label
        self.status_label = CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 12),
            text_color="#FF6B6B"
        )
        self.status_label.pack(pady=(0, 20), padx=20)
        
        # Bind Enter key to login
        self.bind("<Return>", lambda event: self.login())
        
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
    
    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_status("Please enter both username and password", error=True)
            return
        
        # Check if user exists
        user = self.db_manager.get_user(username)
        
        if user is None:
            self.show_status("User not found. Please register first.", error=True)
            return
        
        if user.password != password:
            self.show_status("Incorrect password. Please try again.", error=True)
            return
        
        # Login successful
        self.current_user = user
        self.show_status("Login successful! Opening chat...", error=False)
        self.after(500, self.open_chat_window)
    
    def show_register(self):
        print("show_register: Opening RegisterWindow")
        self.withdraw()  # Hide login window
        register_window = RegisterWindow(self)
        register_window.grab_set()  # Make it modal
        register_window.focus_force()  # Force focus
        register_window.protocol("WM_DELETE_WINDOW", register_window.back_to_login)
        register_window.lift()  # Bring to front
        register_window.attributes('-topmost', True)  # Keep on top
        print("show_register: RegisterWindow created and focused")
        # Don't use wait_window() - let it run normally
        # register_window.wait_window()  # Wait until register window is closed
        # self.deiconify()  # Restore login window
    
    def open_chat_window(self):
        print("open_chat_window: current_user=", self.current_user)
        if not self.current_user:
            print("open_chat_window: ERROR - current_user is None!")
            self.show_status("Login error: user not found!", error=True)
            return
        self.withdraw()  # Hide login window
        chat_app = ChatApp(self.current_user, self.db_manager)
        chat_app.protocol("WM_DELETE_WINDOW", self.on_chat_close)
        chat_app.mainloop()
    
    def on_chat_close(self):
        """Handle chat window close"""
        import sys
        try:
            self.destroy()  # Close the entire application
        except Exception as e:
            print(f"Error closing application: {e}")
        finally:
            sys.exit(0)
    
    def show_status(self, message, error=True):
        """Show status message"""
        color = "#FF6B6B" if error else "#4CAF50"
        self.status_label.configure(text=message, text_color=color)
        self.after(3000, lambda: self.status_label.configure(text=""))  # Clear after 3 seconds
    
    def run(self):
        """Start the login application"""
        print("LoginWindow: Starting mainloop...")
        self.mainloop()
        print("LoginWindow: Mainloop finished")


class RegisterWindow(CTk):
    def __init__(self, login_window):
        print("RegisterWindow: Starting initialization...")
        super().__init__()
        
        print("RegisterWindow: Setting window properties...")
        self.login_window = login_window
        self.db_manager = login_window.db_manager
        
        self.title("Messenger - Register")
        self.geometry("400x600")
        self.resizable(False, False)
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"400x600+{x}+{y}")
        
        print("RegisterWindow: Building UI...")
        self.build_ui()
        print("RegisterWindow: Initialization complete")
        
        # Ensure window is visible
        self.deiconify()
        self.lift()
        self.focus_force()
    
    def build_ui(self):
        self.configure(fg_color="#1E1B2E")
        
        # Title
        self.title_label = CTkLabel(
            self, 
            text="Create New Account", 
            font=("Arial", 24, "bold"), 
            text_color="#BB86FC"
        )
        self.title_label.pack(pady=(40, 20))
        
        # Main frame
        self.main_frame = CTkFrame(self, fg_color="#2C2641", corner_radius=15)
        self.main_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Username field
        self.username_label = CTkLabel(
            self.main_frame, 
            text="Username:", 
            font=("Arial", 14),
            text_color="#FFFFFF"
        )
        self.username_label.pack(pady=(30, 5), padx=20, anchor="w")
        
        self.username_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Choose a username",
            width=300,
            height=40,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.username_entry.pack(pady=(0, 20), padx=20)
        
        # Password field
        self.password_label = CTkLabel(
            self.main_frame, 
            text="Password:", 
            font=("Arial", 14),
            text_color="#FFFFFF"
        )
        self.password_label.pack(pady=(0, 5), padx=20, anchor="w")
        
        self.password_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Choose a password",
            show="*",
            width=300,
            height=40,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.password_entry.pack(pady=(0, 20), padx=20)
        
        # Confirm password field
        self.confirm_label = CTkLabel(
            self.main_frame, 
            text="Confirm Password:", 
            font=("Arial", 14),
            text_color="#FFFFFF"
        )
        self.confirm_label.pack(pady=(0, 5), padx=20, anchor="w")
        
        self.confirm_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Confirm your password",
            show="*",
            width=300,
            height=40,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.confirm_entry.pack(pady=(0, 20), padx=20)
        
        # Show/Hide password button
        self.show_password_var = BooleanVar()
        self.show_password_checkbox = CTkCheckBox(
            self.main_frame,
            text="Show passwords",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            text_color="#FFFFFF",
            fg_color="#BB86FC",
            hover_color="#9B6CFF"
        )
        self.show_password_checkbox.pack(pady=(0, 20), padx=20, anchor="w")
        
        # Register button
        self.register_button = CTkButton(
            self.main_frame,
            text="Create Account",
            command=self.register,
            width=300,
            height=45,
            corner_radius=10,
            fg_color="#03DAC5",
            hover_color="#018786",
            font=("Arial", 14, "bold")
        )
        self.register_button.pack(pady=(0, 20), padx=20)
        
        # Back to login button
        self.back_button = CTkButton(
            self.main_frame,
            text="Back to Login",
            command=self.back_to_login,
            width=300,
            height=45,
            corner_radius=10,
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            font=("Arial", 14, "bold")
        )
        self.back_button.pack(pady=(0, 20), padx=20)
        
        # Status label
        self.status_label = CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 12),
            text_color="#FF6B6B"
        )
        self.status_label.pack(pady=(0, 20), padx=20)
        
        # Bind Enter key to register
        self.bind("<Return>", lambda event: self.register())
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
            self.confirm_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
            self.confirm_entry.configure(show="*")
    
    def register(self):
        """Handle registration attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        
        if not username or not password or not confirm:
            self.show_status("Please fill in all fields", error=True)
            return
        
        if password != confirm:
            self.show_status("Passwords do not match", error=True)
            return
        
        if len(password) < 4:
            self.show_status("Password must be at least 4 characters", error=True)
            return
        
        # Check if user already exists
        existing_user = self.db_manager.get_user(username)
        if existing_user is not None:
            self.show_status("Username already exists. Please choose another.", error=True)
            return
        
        # Create new user
        user_id = str(uuid.uuid4())[:8].upper()  # Generate unique ID
        new_user = User(user_id=user_id, username=username, password=password)
        
        # Add user to database
        self.db_manager.add_user(new_user)
        
        self.show_status("Account created successfully! You can now login.", error=False)
        
        # Clear fields
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.confirm_entry.delete(0, END)
        # After 1.5s, close register and show login
        self.after(1500, self.back_to_login)
    
    def back_to_login(self):
        """Return to login window"""
        print("back_to_login: Closing RegisterWindow and restoring LoginWindow")
        self.destroy()
        self.login_window.deiconify()  # Show login window again
        self.login_window.focus_force()  # Force focus back to login
    
    def show_status(self, message, error=True):
        """Show status message"""
        color = "#FF6B6B" if error else "#4CAF50"
        self.status_label.configure(text=message, text_color=color)
        self.after(3000, lambda: self.status_label.configure(text=""))  # Clear after 3 seconds


if __name__ == "__main__":
    app = LoginWindow()
    app.run()