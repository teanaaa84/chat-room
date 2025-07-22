from typing import Optional

class link_list_node:
    def __init__(self, reply):
        self.reply = reply
        self.next: Optional['link_list_node'] = None

class link_list:
    def __init__(self):
        self.head: Optional[link_list_node] = None

    def add_reply(self, reply):
        new_node = link_list_node(reply)
        if self.head is None:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node
    
    def get_all_replies(self):
        replies = []
        if self.head is None:
            return replies
        temp = self.head 
        while temp:
            replies.append(temp.reply)
            temp = temp.next
        return replies
            
