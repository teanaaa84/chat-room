print("Starting messenger app...")

try:
    print("Importing LoginWindow...")
    from ui.login import LoginWindow
    print("LoginWindow imported successfully")
    
    if __name__ == "__main__":
        print("Creating LoginWindow instance...")
        login = LoginWindow()
        print("LoginWindow created, starting run()...")
        login.run()
        print("App finished")
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
