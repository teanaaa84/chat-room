class link_list_node:
    def __init__(self,reply):
        self.reply=reply
        self.next=None

class link_list:
    def __init__(self):
        self.head=None

    def add_reply(self,reply):
        new_node=link_list_node(reply)
        if self.head is None:
            self.head=new_node
        temp=self.head
        while temp.next:
            temp=temp.next
        temp.next=new_node
    
    
    def get_all_replies(self):
        replies=[]
        if self.head is None:
            return
        temp=self.head 
        while temp :
            replies.append(temp.reply)
            temp=temp.next
        return replies
            
