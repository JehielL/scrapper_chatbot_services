import os

def save_to_txt(text, filename="scrap_context.txt", directory="context"):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
