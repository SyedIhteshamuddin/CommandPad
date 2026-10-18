
print("=== COMMANDPAD TEST ===")

keys = {
    "1": "Copy (Ctrl+C)",
    "2": "Paste (Ctrl+V)",
    "3": "Undo (Ctrl+Z)",
    "4": "Switch Window (Alt+Tab)",
    "5": "Screenshot (Win+Shift+S)"
}

while True:
    print("\nPress 1, 2, 3, 4, or 5. Type q to quit.")

    choice = input("Your key: ").strip()

    if choice.lower() == "q":
        print("CommandPad simulator closed.")
        break
    elif choice in keys:
        print("Key", choice, "selected:", keys[choice])
    else:
        print("Invalid key. Try again.")
python -m pip install pyautogui
