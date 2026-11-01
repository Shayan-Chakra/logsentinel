import pyautogui
import pyperclip
import time

pyautogui.FAILSAFE = True

messages = [
    "Oooooo Maaaaa Ki korchoooo...."
]

count = int(input("Enter number of messages (maximum 100): "))

if not 1 <= count <= 100:
    print("Please enter a number between 1 and 100.")
    exit()

confirm = input("Confirm you have opened your own Saved Messages (YES/NO): ")

if confirm.upper() != "YES":
    print("Cancelled.")
    exit()

print("Click the Telegram message box.")
print("Starting in 5 seconds...")
time.sleep(5)

for i in range(count):
    message = messages[i % len(messages)]

    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    pyautogui.press("enter")

    print(f"Message {i + 1}/{count}: {message}")
    time.sleep(0.5)

print("Task completed!")