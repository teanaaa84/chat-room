class HashTableNode:
    def __init__(self, key, user):
        self.key = key
        self.user = user
        self.next = None

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        index = sum(ord(char) for char in str(key)) % self.size
        print(f"[HASH] key='{key}' → index={index}")
        return index

    def insert(self, key, user):
        index = self.hash_function(key)
        new_node = HashTableNode(key, user)

        if self.table[index] is None:
            self.table[index] = new_node
            print(f"[INSERT] '{key}' inserted at index {index} (no collision)")
        else:
            print(f"[COLLISION] inserting '{key}' at index {index} (linked list used)")
            temp = self.table[index]
            while temp.next:
                if temp.key == key:
                    print(f"[UPDATE] Key '{key}' already exists, updating value")
                    temp.user = user
                    return
                temp = temp.next
            if temp.key == key:
                print(f"[UPDATE] Key '{key}' already exists at end, updating value")
                temp.user = user
            else:
                temp.next = new_node
                print(f"[INSERT] '{key}' added to chain at index {index}")

    def get(self, key):
        index = self.hash_function(key)
        temp = self.table[index]
        while temp:
            if temp.key == key:
                print(f"[GET] Found '{key}' at index {index} → {temp.user}")
                return temp.user
            temp = temp.next
        print(f"[GET] Key '{key}' not found at index {index}")
        return None

    def delete(self, key):
        index = self.hash_function(key)
        temp = self.table[index]
        prev = None
        while temp:
            if temp.key == key:
                if prev:
                    prev.next = temp.next
                else:
                    self.table[index] = temp.next
                print(f"[DELETE] '{key}' removed from index {index}")
                return True
            prev = temp
            temp = temp.next
        print(f"[DELETE] Key '{key}' not found in index {index}")
        return False


if __name__ == "__main__":
    print("🧪 شروع تست بزرگ HashTable")

    class Dummy:
        def __init__(self, val):
            self.val = val
        def __repr__(self):
            return f"Dummy({self.val})"

    ht = HashTable(size=7)

    # مرحله 1: درج تعداد زیادی کلید
    print("\n🔁 [Insert] وارد کردن داده‌ها:")
    keys = ["a", "b", "ab", "ba", "z", "zz", "aa", "az", "za", "abc", "cab", "bca"]
    for k in keys:
        ht.insert(k, Dummy(f"val_{k}"))

    # مرحله 2: بازیابی همه کلیدها
    print("\n🔍 [Get] بررسی اینکه همه چیز درست وارد شده:")
    for k in keys:
        val = ht.get(k)
        print(f"✅ get('{k}') → {val}")

    # مرحله 3: حذف چند کلید و تست دوباره
    print("\n🗑️ [Delete] حذف چند کلید:")
    to_delete = ["a", "ab", "zz", "not_exist"]
    for k in to_delete:
        result = ht.delete(k)
        print(f"{'✅' if result else '❌'} delete('{k}')")

    print("\n🔍 [Get] بررسی دوباره پس از حذف:")
    for k in keys:
        val = ht.get(k)
        print(f"get('{k}') → {val}")

    print("\n🎉 تست تمام شد.")
