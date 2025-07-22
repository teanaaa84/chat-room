import customtkinter as ctk
from datetime import datetime
import functools

class ChatApp(ctk.CTk):
    def __init__(self, current_user, db_manager):
        print("ChatApp: __init__ current_user=", current_user)
        print("ChatApp: __init__ db_manager=", db_manager)
        super().__init__()
        self.title("Messenger")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color="#1E1B2E")

        self.current_user = current_user
        self.db_manager = db_manager
        self.selected_user = None

        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.user_list = ctk.CTkFrame(self, fg_color="#2C2641", width=200)
        self.user_list.grid(row=0, column=0, sticky="ns")

        # Search box above user list
        self.user_search_entry = ctk.CTkEntry(
            self.user_list,
            placeholder_text="Search user...",
            width=180,
            height=30,
            corner_radius=8,
            font=("Arial", 12)
        )
        self.user_search_entry.pack(pady=(10, 0), padx=10)
        self.user_search_entry.bind("<KeyRelease>", lambda e: self.refresh_user_list())

        # User info header
        user_info_frame = ctk.CTkFrame(self.user_list, fg_color="#2C2641")
        user_info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            user_info_frame,
            text=f"Welcome, {self.current_user.username}!",
            font=("Arial", 14, "bold"),
            text_color="#BB86FC",
        ).pack(pady=10)
        
        # Logout button
        ctk.CTkButton(
            user_info_frame,
            text="Logout",
            command=self.logout,
            width=120,
            height=30,
            corner_radius=8,
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            font=("Arial", 12)
        ).pack(pady=5)
        
        # Add User button
        ctk.CTkButton(
            user_info_frame,
            text="Add User",
            command=self.show_add_user_dialog,
            width=120,
            height=30,
            corner_radius=8,
            fg_color="#03DAC5",
            hover_color="#018786",
            font=("Arial", 12)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            self.user_list,
            text="Users",
            font=("Arial", 20, "bold"),
            text_color="#BB86FC",
        ).pack(pady=20)

        self.user_buttons_frame = ctk.CTkScrollableFrame(
            self.user_list, fg_color="#2C2641", width=180
        )
        self.user_buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_user_list()

        self.chat_frame = ctk.CTkFrame(self, fg_color="#2C2641")
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.chat_frame.grid_rowconfigure(1, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        # Chat message search box
        self.chat_search_entry = ctk.CTkEntry(
            self.chat_frame,
            placeholder_text="Search in chat...",
            width=300,
            height=30,
            corner_radius=8,
            font=("Arial", 12)
        )
        self.chat_search_entry.grid(row=0, column=0, sticky="e", padx=(200, 10), pady=10)
        self.chat_search_entry.bind("<KeyRelease>", lambda e: self.refresh_chat())

        # Show all replies button
        self.show_replies_btn = ctk.CTkButton(
            self.chat_frame,
            text="all replies",
            command=self.show_all_replies,
            width=180,
            height=30,
            corner_radius=8,
            fg_color="#03DAC5",
            hover_color="#018786",
            font=("Arial", 12)
        )
        self.show_replies_btn.grid(row=0, column=0, sticky="e", padx=10, pady=10)

        self.chat_title = ctk.CTkLabel(
            self.chat_frame,
            text="Select a user to chat",
            font=("Arial", 18, "bold"),
            text_color="#BB86FC",
        )
        self.chat_title.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.chat_canvas = ctk.CTkScrollableFrame(self.chat_frame, fg_color="#1E1B2E")
        self.chat_canvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        bottom_frame = ctk.CTkFrame(self.chat_frame, fg_color="#2C2641")
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)

        # Reply label (hidden by default)
        self.reply_label = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=("Arial", 12, "italic"),
            text_color="#03DAC5"
        )
        self.reply_label.grid(row=0, column=0, sticky="w", padx=(0, 2), pady=2)
        self.reply_label.grid_remove()
        self.reply_to_message = None
        # Add close (X) button for reply cancel
        self.reply_close_btn = ctk.CTkButton(
            bottom_frame,
            text="✕",
            width=24,
            height=24,
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            font=("Arial", 12, "bold"),
            command=self.clear_reply_to
        )
        self.reply_close_btn.grid(row=0, column=1, sticky="w", padx=(2, 0), pady=2)
        self.reply_close_btn.grid_remove()

        self.msg_entry = ctk.CTkEntry(
            bottom_frame, placeholder_text="Type a message...", height=30
        )
        self.msg_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=5)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = ctk.CTkButton(
            bottom_frame,
            text="Send",
            width=100,
            height=30,
            corner_radius=10,
            fg_color="#BB86FC",
            hover_color="#9B6CFF",
            command=self.send_message,
        )
        self.send_button.grid(row=1, column=1)

    def show_reply_to(self, message):
        self.reply_to_message = message
        self.reply_label.configure(text=f"Replying to: {message.content}")
        self.reply_label.grid()
        self.reply_close_btn.grid()

    def clear_reply_to(self):
        self.reply_to_message = None
        self.reply_label.grid_remove()
        self.reply_close_btn.grid_remove()

    def refresh_user_list(self):
        print("refresh_user_list: Starting to refresh user list...")
        print(f"refresh_user_list: Current user is '{self.current_user.username}'")
        for widget in self.user_buttons_frame.winfo_children():
            widget.destroy()
        user_count = 0
        unread_count_by_sender = {}
        if self.current_user.unread_stack:
            temp = self.current_user.unread_stack.top
            while temp:
                msg = temp.value
                if hasattr(msg, 'sender'):
                    unread_count_by_sender[msg.sender] = unread_count_by_sender.get(msg.sender, 0) + 1
                temp = temp.next
        user_last_msg = []
        # Always get search text directly
        search_text = self.user_search_entry.get().strip().lower() if hasattr(self, 'user_search_entry') else ''
        print(f"refresh_user_list: search_text='{search_text}'")
        for i in range(self.db_manager.user_table.size):
            node = self.db_manager.user_table.table[i]
            while node:
                username = node.key
                if username != self.current_user.username:
                    # Search filter
                    if search_text and search_text not in username.lower():
                        node = node.next
                        continue
                    last_time = None
                    all_msgs = []
                    for m in self.current_user.get_all_messages():
                        if getattr(m, 'to', None) == username:
                            all_msgs.append(m)
                    user_obj = self.db_manager.get_user(username)
                    if user_obj:
                        for m in user_obj.get_all_messages():
                            if getattr(m, 'to', None) == self.current_user.username:
                                all_msgs.append(m)
                    if all_msgs:
                        last_time = max(m.time for m in all_msgs)
                    unread_count = unread_count_by_sender.get(username, 0)
                    user_last_msg.append((username, last_time, unread_count))
                node = node.next
        print(f"refresh_user_list: filtered users: {[u[0] for u in user_last_msg]}")
        user_last_msg.sort(key=lambda x: (x[1] if x[1] else '', x[0]), reverse=True)
        for username, _, unread_count in user_last_msg:
            btn_text = username
            if unread_count > 0:
                btn_text += f" ({unread_count})"
            print(f"refresh_user_list: Adding button for user '{username}' with {unread_count} unread")
            btn = ctk.CTkButton(
                self.user_buttons_frame,
                text=btn_text,
                command=lambda u=username: self.open_chat(u),
                width=160,
                height=40,
                corner_radius=12,
                fg_color="#3A2E58",
                hover_color="#6F4B94",
            )
            btn.pack(pady=5)
            user_count += 1
        print(f"refresh_user_list: Total users found: {user_count}")
        if user_count == 0:
            no_users_label = ctk.CTkLabel(
                self.user_buttons_frame,
                text="No other users found.\nRegister more users to chat!",
                text_color="#888",
                font=("Arial", 12)
            )
            no_users_label.pack(pady=20)

    def open_chat(self, username):
        self.selected_user = username
        self.chat_title.configure(text=f"Chat with {username}")
        # Mark messages from this user as read (remove from unread_stack)
        changed = False
        if self.current_user.unread_stack:
            prev = None
            temp = self.current_user.unread_stack.top
            while temp:
                next_temp = temp.next
                msg = temp.value
                if hasattr(msg, 'sender') and msg.sender == username:
                    # Remove this node from stack
                    changed = True
                    if prev:
                        prev.next = temp.next
                    else:
                        self.current_user.unread_stack.top = temp.next
                else:
                    prev = temp
                temp = next_temp
        if changed:
            self.db_manager.save_data()
        self.refresh_user_list()
        self.refresh_chat()

    def refresh_chat(self):
        import functools
        print("refresh_chat: Starting to refresh chat...")
        for widget in self.chat_canvas.winfo_children():
            widget.destroy()
        if not self.selected_user:
            print("refresh_chat: No user selected")
            return
        messages = self.get_conversation_messages()
        # Filter messages by chat search
        search_text = self.chat_search_entry.get().strip().lower() if hasattr(self, 'chat_search_entry') else ''
        if search_text:
            messages = [m for m in messages if search_text in m.content.lower()]
        print(f"refresh_chat: Found {len(messages)} messages")
        # Build a dict of id->message for fast parent lookup
        msg_dict = {m.id: m for m in messages}
        for m in messages:
            print(f"refresh_chat: Displaying message from {m.sender}: {m.content}")
            side = "e" if m.sender == self.current_user.username else "w"
            color = "#BB86FC" if side == "e" else "#03DAC5"
            frame = ctk.CTkFrame(self.chat_canvas, fg_color=color, corner_radius=15)
            frame.pack(anchor=side, pady=2, padx=20)
            # If this message is a reply, show parent message content above
            if getattr(m, 'parent_id', None):
                parent_msg = msg_dict.get(m.parent_id)
                parent_text = parent_msg.content if parent_msg else "(Original message not found)"
                ctk.CTkLabel(
                    frame,
                    text=f"Reply to: {parent_text}",
                    text_color="#03DAC5",
                    font=("Arial", 10, "italic"),
                    anchor=side,
                    justify="left",
                    wraplength=500,
                    padx=8,
                    pady=2,
                ).pack(anchor=side)
            label = ctk.CTkLabel(
                frame,
                text=m.content,
                text_color="white",
                fg_color=color,
                anchor=side,
                justify="left",
                wraplength=600,
                padx=12,
                pady=6,
            )
            label.pack(anchor=side)
            # Show reply info if this message is a reply to another
            if hasattr(m, 'replies') and m.replies and m.replies.get_all_replies():
                replies = m.replies.get_all_replies()
                for reply in replies:
                    reply_text = f"↪ {reply['from']}: {reply['content']}"
                    ctk.CTkLabel(
                        frame,
                        text=reply_text,
                        text_color="#03DAC5",
                        font=("Arial", 10, "italic"),
                        anchor=side,
                        justify="left",
                        wraplength=500,
                        padx=16,
                        pady=2,
                    ).pack(anchor=side)
            time = m.time
            ctk.CTkLabel(
                frame, text=time, text_color="#ddd", font=("Arial", 7), padx=6
            ).pack(anchor=side)
            label.bind("<Button-3>", functools.partial(self.show_reply_menu, message=m))

    def show_reply_menu(self, event, message):
        import tkinter as tk
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Reply", command=lambda: self.show_reply_to(message))
        menu.add_command(label="Cancel", command=self.clear_reply_to)
        menu.tk_popup(event.x_root, event.y_root)
        menu.grab_release()

    def get_conversation_messages(self):
        print(f"get_conversation_messages: Getting messages between {self.current_user.username} and {self.selected_user}")
        user_obj = self.db_manager.get_user(self.selected_user)
        if not user_obj:
            print("get_conversation_messages: Selected user not found")
            return []
        my_msgs = self.current_user.get_all_messages()
        their_msgs = user_obj.get_all_messages()
        print(f"get_conversation_messages: Current user has {len(my_msgs)} messages")
        print(f"get_conversation_messages: Selected user has {len(their_msgs)} messages")
        conversation = []
        seen_ids = set()
        # Only show messages sent from current_user to selected_user, or from selected_user to current_user
        for m in my_msgs + their_msgs:
            if (m.sender == self.current_user.username and getattr(m, 'to', None) == self.selected_user) or \
               (m.sender == self.selected_user and getattr(m, 'to', None) == self.current_user.username):
                if m.id not in seen_ids:
                    conversation.append(m)
                    seen_ids.add(m.id)
                    print(f"get_conversation_messages: Added message from {m.sender} to {getattr(m, 'to', None)}: {m.content}")
        conversation.sort(key=lambda m: m.time)
        print(f"get_conversation_messages: Total conversation messages: {len(conversation)}")
        return conversation

    def send_message(self):
        text = self.msg_entry.get().strip()
        print(f"send_message: sender={self.current_user.username}, receiver={self.selected_user}, text={text}")
        if not text:
            return
        if not self.selected_user:
            print("send_message: No user selected for chat")
            self.chat_title.configure(text="Please select a user to chat with")
            return
        # If replying to a message, add as reply
        reply_to = self.reply_to_message
        parent_id = reply_to.id if reply_to else None
        success = self.db_manager.send_message(self.current_user, self.selected_user, text, parent_id=parent_id)
        if success:
            print(f"send_message: Message sent successfully")
            self.msg_entry.delete(0, ctk.END)
            self.clear_reply_to()
            self.refresh_chat()
        else:
            print(f"send_message: Failed to send message")

    def logout(self):
        self.destroy()

    def show_add_user_dialog(self):
        """Shows a dialog to add a new user or load from users.json"""
        import tkinter as tk
        import uuid
        from models.user import User
        
        def on_submit():
            username = username_entry.get().strip()
            user_id = user_id_entry.get().strip()
            print(f"show_add_user_dialog: Username entered: '{username}'")
            print(f"show_add_user_dialog: User ID entered: '{user_id}'")
            win.destroy()
            if not username:
                print("show_add_user_dialog: Username is required")
                return
            if not user_id:
                user_id = str(uuid.uuid4())[:8].upper()
                print(f"show_add_user_dialog: Generated user_id: '{user_id}'")
            existing_user = self.db_manager.get_user(username)
            if existing_user:
                print(f"show_add_user_dialog: User '{username}' already exists")
            else:
                new_user = User(
                    user_id=user_id,
                    username=username,
                    password="123456"
                )
                self.db_manager.add_user(new_user)
                print(f"show_add_user_dialog: Added new user '{username}' with id '{user_id}'")
            self.refresh_user_list()
        
        win = tk.Toplevel(self)
        win.title("Add New User")
        win.geometry("300x160")
        win.grab_set()
        
        tk.Label(win, text="Username:").pack(pady=(10, 0))
        username_entry = tk.Entry(win)
        username_entry.pack(pady=5)
        
        tk.Label(win, text="User ID (optional):").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack(pady=5)
        
        tk.Button(win, text="Add User", command=on_submit).pack(pady=10)
        
        # Focus on username entry
        username_entry.focus()
        win.focus_force()
        
        # Bind Enter key to submit
        win.bind("<Return>", lambda e: on_submit())
        
        win.mainloop()

    def show_all_replies(self):
        import tkinter as tk
        # Gather all replies for the current chat
        if not self.selected_user:
            return
        messages = self.get_conversation_messages()
        reply_pairs = []
        msg_dict = {m.id: m for m in messages}
        for m in messages:
            if hasattr(m, 'replies') and m.replies and m.replies.get_all_replies():
                parent_text = m.content
                for reply in m.replies.get_all_replies():
                    reply_pairs.append((parent_text, reply['from'], reply['content'], reply['time']))
        # Show in a popup window
        win = tk.Toplevel(self)
        win.title("All Replies in This Chat")
        win.geometry("500x400")
        win.grab_set()
        tk.Label(win, text="All replies in this chat:", font=("Arial", 14, "bold")).pack(pady=10)
        if not reply_pairs:
            tk.Label(win, text="No replies found.", font=("Arial", 12)).pack(pady=20)
        else:
            canvas = tk.Canvas(win)
            scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
            frame = tk.Frame(canvas)
            frame.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            for parent_text, reply_from, reply_content, reply_time in reply_pairs:
                tk.Label(frame, text=f"Parent message: {parent_text}", font=("Arial", 11, "bold"), fg="#03DAC5").pack(anchor="w", padx=10, pady=(10, 0))
                tk.Label(frame, text=f"↪ {reply_from}: {reply_content}", font=("Arial", 11), fg="#333").pack(anchor="w", padx=30)
                tk.Label(frame, text=f"Time: {reply_time}", font=("Arial", 9), fg="#888").pack(anchor="w", padx=30, pady=(0, 5))
        win.focus_force()
