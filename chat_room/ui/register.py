from customtkinter import *
from models.user import User


class LoginApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("Login / Signup")
        self.geometry("600x550")
        self.resizable(False, False)
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")

        self.is_login = True
        self.build_ui()

    def handle_submit(self):
        if self.is_login:
            # بررسی وجود کاربر در HashTable
            user = self.user_table.get(self.username_entry.get())
            if user and user.password == self.password_entry.get():
                self.open_main_window(user)
        else:
            # ثبت کاربر جدید در HashTable
            new_user = User(
                user_id=generate_id(),
                username=self.username_entry.get(),
                password=self.password_entry.get(),
            )
            self.user_table.insert(new_user.username, new_user)

    def build_ui(self):
        self.configure(fg_color="#1E1B2E")

        self.title_label = CTkLabel(
            self, text="", font=("Arial", 26, "bold"), text_color="#BB86FC"
        )
        self.title_label.pack(pady=30)

        self.form_frame = CTkFrame(self, corner_radius=15, fg_color="#2C2641")
        self.form_frame.pack(pady=20, padx=40)

        # Username
        username_frame = CTkFrame(self.form_frame, fg_color="#2C2641", corner_radius=10)
        username_frame.pack(pady=(20, 10), fill="x", padx=20)

        self.username_label = CTkLabel(
            username_frame, text="Username", width=100, anchor="w"
        )
        self.username_label.pack(side="left", padx=10)

        self.username_entry = CTkEntry(
            username_frame,
            placeholder_text="Enter username",
            width=250,
            height=40,
            corner_radius=10,
        )
        self.username_entry.pack(side="left", padx=10)

        # Password
        self.password_frame = CTkFrame(
            self.form_frame, fg_color="#2C2641", corner_radius=10
        )
        self.password_frame.pack(pady=10, fill="x", padx=20)

        self.password_label = CTkLabel(
            self.password_frame, text="Password", width=100, anchor="w"
        )
        self.password_label.pack(side="left", padx=10)

        self.password_entry = CTkEntry(
            self.password_frame,
            placeholder_text="Enter password",
            show="*",
            width=250,
            height=40,
            corner_radius=10,
        )
        self.password_entry.pack(side="left", padx=(10, 5))

        self.show_password_button = CTkButton(
            self.password_frame,
            text="Show",
            width=50,
            height=30,
            fg_color="#3192A8",
            hover_color="#0D5497",
            corner_radius=8,
            command=self.toggle_password_visibility,
        )
        self.show_password_button.pack(side="left", padx=(5, 10))

        # Confirm Password (Signup only)
        self.confirm_frame = CTkFrame(
            self.form_frame, fg_color="#2C2641", corner_radius=10
        )

        self.confirm_label = CTkLabel(
            self.confirm_frame, text="Confirm Password", width=100, anchor="w"
        )
        self.confirm_label.pack(side="left", padx=10)

        self.confirm_entry = CTkEntry(
            self.confirm_frame,
            placeholder_text="Repeat password",
            show="*",
            width=250,
            height=40,
            corner_radius=10,
        )
        self.confirm_entry.pack(side="left", padx=(10, 5))

        self.show_confirm_button = CTkButton(
            self.confirm_frame,
            text="Show",
            width=50,
            height=30,
            fg_color="#3192A8",
            hover_color="#0D5497",
            corner_radius=8,
            command=self.toggle_confirm_visibility,
        )
        self.show_confirm_button.pack(side="left", padx=(5, 10))

        # دکمه submit - همیشه داخل فرم اصلیه
        self.submit_button = CTkButton(
            self.form_frame,
            text="",
            command=self.handle_submit,
            fg_color="#BB86FC",
            hover_color="#9B6CFF",
            corner_radius=10,
            width=360,
            height=45,
        )

        # لینک جابه‌جایی
        self.switch_label = CTkLabel(
            self, text="", text_color="#888", font=("Arial", 12), cursor="hand2"
        )
        self.switch_label.pack(pady=10)
        self.switch_label.bind("<Button-1>", lambda e: self.toggle_mode())

        self.password_visible = False
        self.confirm_visible = False

        self.update_mode()

    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password_entry.configure(show="")
            self.show_password_button.configure(text="Hide")
        else:
            self.password_entry.configure(show="*")
            self.show_password_button.configure(text="Show")

    def toggle_confirm_visibility(self):
        self.confirm_visible = not self.confirm_visible
        if self.confirm_visible:
            self.confirm_entry.configure(show="")
            self.show_confirm_button.configure(text="Hide")
        else:
            self.confirm_entry.configure(show="*")
            self.show_confirm_button.configure(text="Show")

    def update_mode(self):
        if self.is_login:
            self.title_label.configure(text="Login")
            self.submit_button.configure(text="Login")

            self.confirm_frame.pack_forget()
            self.submit_button.pack_forget()

            # دکمه رو زیر password_frame میذاریم
            self.submit_button.pack(pady=20, in_=self.form_frame)

            self.switch_label.configure(text="Don’t have an account? Sign up here")

        else:
            self.title_label.configure(text="Sign Up")
            self.submit_button.configure(text="Sign Up")

            self.confirm_frame.pack(pady=10, fill="x", padx=20)
            self.submit_button.pack_forget()

            # دکمه رو زیر confirm_frame میذاریم (ولی تو فرم اصلی)
            self.submit_button.pack(pady=20, in_=self.form_frame)

            self.switch_label.configure(text="Already have an account? Login here")

        self.clear_entries()
        self.password_visible = False
        self.confirm_visible = False
        self.password_entry.configure(show="*")
        self.confirm_entry.configure(show="*")
        self.show_password_button.configure(text="Show")
        self.show_confirm_button.configure(text="Show")

    def toggle_mode(self):
        self.is_login = not self.is_login
        self.update_mode()

    def clear_entries(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.confirm_entry.delete(0, END)

    def handle_submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if self.is_login:
            print(f"Logging in with: {username} / {password}")
        else:
            if password != confirm:
                print("Passwords do not match.")
            else:
                print(f"Signing up: {username} / {password}")


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
