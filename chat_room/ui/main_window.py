from customtkinter import *
import json
import os
from datetime import datetime

DATA_FILE = "ui/messages.json"
CURRENT_USER = "mobina"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class ChatApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("Messenger")
        self.geometry("900x600")
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        self.configure(fg_color="#1E1B2E")

        self.data = load_data()
        self.selected_user = None

        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.user_list = CTkFrame(self, fg_color="#2C2641", width=200)
        self.user_list.grid(row=0, column=0, sticky="ns")

        CTkLabel(
            self.user_list,
            text="Users",
            font=("Arial", 20, "bold"),
            text_color="#BB86FC",
        ).pack(pady=20)

        self.user_buttons_frame = CTkScrollableFrame(
            self.user_list, fg_color="#2C2641", width=180
        )
        self.user_buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for username in self.data:
            if username != CURRENT_USER:
                btn = CTkButton(
                    self.user_buttons_frame,
                    text=username,
                    command=lambda u=username: self.open_chat(u),
                    width=160,
                    height=40,
                    corner_radius=12,
                    fg_color="#3A2E58",
                    hover_color="#6F4B94",
                    
                )
                btn.pack(pady=5)

        self.chat_frame = CTkFrame(self, fg_color="#2C2641")
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.chat_frame.grid_rowconfigure(1, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.chat_title = CTkLabel(
            self.chat_frame,
            text="Select a user to chat",
            font=("Arial", 18, "bold"),
            text_color="#BB86FC",
        )
        self.chat_title.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.chat_canvas = CTkScrollableFrame(self.chat_frame, fg_color="#1E1B2E")
        self.chat_canvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        bottom_frame = CTkFrame(self.chat_frame, fg_color="#2C2641")
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.msg_entry = CTkEntry(
            bottom_frame, placeholder_text="Type a message...", height=30
        )
        self.msg_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = CTkButton(
            bottom_frame,
            text="Send",
            width=100,
            height=30,
            corner_radius=10,
            fg_color="#BB86FC",
            hover_color="#9B6CFF",
            command=self.send_message,
        )
        self.send_button.grid(row=0, column=1)

    def open_chat(self, user):
        self.selected_user = user
        self.chat_title.configure(text=f"Chat with {user}")
        self.refresh_chat()

    def refresh_chat(self):
        for widget in self.chat_canvas.winfo_children():
            widget.destroy()

        if self.selected_user:
            msgs = self.data.get(CURRENT_USER, {}).get("messages", []) + self.data.get(
                self.selected_user, {}
            ).get("messages", [])
            msgs = sorted(msgs, key=lambda m: m.get("timestamp", ""))

            for i, m in enumerate(msgs):
                if (m["from"] == CURRENT_USER and m["to"] == self.selected_user) or (
                    m["from"] == self.selected_user and m["to"] == CURRENT_USER
                ):

                    side = "e" if m["from"] == CURRENT_USER else "w"
                    color = "#BB86FC" if side == "e" else "#03DAC5"

                    # فریم پیام با padding خیلی کم
                    frame = CTkFrame(self.chat_canvas, fg_color=color, corner_radius=15)
                    frame.pack(anchor=side, pady=2, padx=20)

                    # لیبل پیام با padding خیلی کم و wraplength بیشتر تا حداکثر جا رو نگیره
                    # تو متد refresh_chat جای CTkLabel پیام رو اینجوری تغییر بده:

                    CTkLabel(
                        frame,
                        text=m["text"],
                        text_color="white",
                        fg_color=color,
                        anchor=side,
                        justify="left",
                        wraplength=600,
                        padx=12,
                        pady=6,
                    ).pack(anchor=side)

                    time = m.get("timestamp", "")
                    CTkLabel(
                        frame, text=time, text_color="#ddd", font=("Arial", 7), padx=6
                    ).pack(anchor=side)

                    if m["from"] == CURRENT_USER:
                        del_btn = CTkButton(
                            frame,
                            text="🗑",
                            width=15,
                            height=15,
                            fg_color="#FF5C5C",
                            command=lambda idx=i: self.delete_message(idx),
                            corner_radius=8,
                        )
                        del_btn.pack(anchor="ne", padx=3, pady=1)

    def send_message(self):
        text = self.msg_entry.get().strip()
        if text and self.selected_user:
            now = datetime.now().strftime("%H:%M")
            message = {
                "from": CURRENT_USER,
                "to": self.selected_user,
                "text": text,
                "timestamp": now,
            }
            self.data.setdefault(CURRENT_USER, {}).setdefault("messages", []).append(
                message
            )
            save_data(self.data)
            self.msg_entry.delete(0, END)
            self.refresh_chat()

    def delete_message(self, index):
        messages = self.data.get(CURRENT_USER, {}).get("messages", [])
        if 0 <= index < len(messages):
            del messages[index]
            save_data(self.data)
            self.refresh_chat()

    def add_search_functionality(self):
        search_frame = CTkFrame(self.user_list, fg_color="#2C2641")
        search_frame.pack(pady=10)
        
        self.search_entry = CTkEntry(search_frame, placeholder_text="Search messages...")
        self.search_entry.pack(side="left", padx=5)
        
        CTkButton(
            search_frame,
            text="🔍",
            width=30,
            command=self.perform_search
        ).pack(side="left")

    def perform_search(self):
        search_term = self.search_entry.get()
        if self.selected_user and search_term:
            found_messages = self.current_user.messages_bst.search_by_content(search_term)
            # نمایش نتایج جستجو
        
    def add_reply_button(self, message_frame, message):
        CTkButton(
            message_frame,
            text="↩️ Reply",
            command=lambda: self.open_reply_dialog(message),
            width=60,
            height=20
        ).pack(anchor="e")

    def open_reply_dialog(self, parent_message):
        dialog = CTkInputDialog(text="Enter your reply:", title=f"Reply to {parent_message.sender}")
        reply_text = dialog.get_input()
        if reply_text:
            parent_message.replies.add_reply(reply_text)
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
