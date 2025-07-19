from data_structure.hash import HashTable

# یه کلاس آبجکت ساده برای تست (به جای User)
class Dummy:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Dummy({self.value})"

# تابع کمکی برای پرینت وضعیت جدول هش
def print_table(ht):
    print("\n📊 وضعیت جدول هش:")
    for i, node in enumerate(ht.table):
        print(f"Index {i}:", end=" ")
        temp = node
        while temp:
            print(f"[{temp.key}: {temp.user}]", end=" -> ")
            temp = temp.next
        print("None")

# شروع تست
print("🚀 شروع تست بزرگ هش‌تیبل:\n")
ht = HashTable(size=7)  # سایز کوچیک برای افزایش احتمال برخورد

# 🔢 مرحله 1: وارد کردن چند کلید
keys = ["a", "b", "c", "aa", "bb", "ab", "z", "zz", "az", "ba", "aaa"]
for k in keys:
    ht.insert(k, Dummy(f"val_{k}"))
    print(f"➕ Insert {k} → val_{k}")
print_table(ht)

# 🔍 مرحله 2: بازیابی چند کلید
print("\n🔍 تست بازیابی:")
for k in ["a", "z", "aa", "aaa", "ba"]:
    result = ht.get(k)
    print(f"Get {k} →", result)

# 🗑️ مرحله 3: حذف چند کلید (با برخورد هم)
print("\n🗑️ حذف بعضی کلیدها:")
for k in ["a", "aa", "bb", "z", "not_in_table"]:
    result = ht.delete(k)
    print(f"Delete {k} → {'✅ success' if result else '❌ fail'}")
print_table(ht)

# 🔄 مرحله 4: دوباره اضافه‌کردن و بررسی برخورد جدید
print("\n🔁 اضافه‌کردن دوباره:")
ht.insert("new1", Dummy("val_new1"))
ht.insert("new2", Dummy("val_new2"))
ht.insert("new3", Dummy("val_new3"))
print_table(ht)

# 🎯 مرحله نهایی: بررسی همه کلیدهای باقی‌مانده
print("\n🎯 بررسی نهایی:")
for k in keys + ["new1", "new2", "new3"]:
    value = ht.get(k)
    print(f"🔎 {k} →", value)
