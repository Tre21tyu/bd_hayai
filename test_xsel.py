import pyperclip

# Check which copy/paste method pyperclip is using
# print(pyperclip._executable_paths)
  

 # Attempt to copy a simple string
# try:
#     pyperclip.copy("Hello from pyperclip on Linux!")
#     print("Copied text to clipboard!")
# except pyperclip.PyperclipException as e:
#     print(f"Error copying to clipboard: {e}")


# Check which clipboard method pyperclip is using
print(pyperclip.determine_clipboard())
