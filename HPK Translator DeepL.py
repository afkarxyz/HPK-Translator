import os
import customtkinter as ctk
from deepl import Translator
from PIL import Image
import tkinter as tk
from functools import partial

# Initialize application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1450x675")
app.title("HPK Translator (DeepL)")

# Set custom icon
icon_path = os.path.join(os.path.dirname(__file__), "translate.ico")
app.iconbitmap(icon_path)

MAX_CHARS = 100

# Custom colors
TRANSLATE_BUTTON_COLOR = "#1f8b4c"
TRANSLATE_BUTTON_HOVER_COLOR = "#176839"
RESET_BUTTON_COLOR = "#e74c3c"
RESET_BUTTON_HOVER_COLOR = "#c0392b"
INPUT_FRAME_COLOR = "#424242"
ARABIC_SCROLL_COLOR = "#1d1e1e"  # New color for Arabic scroll

# Initialize DeepL translator
translator = Translator("input your API key")

def limit_chars(text):
    return text[:MAX_CHARS]

def translate_text():
    source_text = source_textbox.get("1.0", "end-1c")
    for lang, textbox in translations.items():
        try:
            result = translator.translate_text(source_text, target_lang=lang)
            translated_text = limit_chars(result.text)
            textbox.delete("1.0", tk.END)
            if lang == 'AR':
                textbox.insert(tk.END, translated_text, "rtl")
            else:
                textbox.insert(tk.END, translated_text)
        except Exception as e:
            textbox.delete("1.0", tk.END)
            textbox.insert(tk.END, f"Error: {str(e)}")
    update_character_counts()

def update_character_counts(event=None):
    input_text = source_textbox.get("1.0", "end-1c")
    if len(input_text) > MAX_CHARS:
        input_text = limit_chars(input_text)
        source_textbox.delete("1.0", ctk.END)
        source_textbox.insert(ctk.END, input_text)
    input_char_count_label.configure(text=f"{len(input_text)}/{MAX_CHARS}")
    
    for textbox, label in char_count_labels.items():
        text = textbox.get("1.0", "end-1c")
        if len(text) > MAX_CHARS:
            text = limit_chars(text)
            textbox.delete("1.0", ctk.END)
            textbox.insert(ctk.END, text)
        label.configure(text=f"{len(text)}/{MAX_CHARS}")

def copy_to_clipboard(textbox, copy_button):
    text_to_copy = textbox.get("1.0", "end-1c")
    app.clipboard_clear()
    app.clipboard_append(text_to_copy)
    app.update()  # This is necessary to finalize the clipboard operation
    
    original_text = copy_button.cget("text")
    copy_button.configure(text="Copied!")
    app.after(2000, lambda: copy_button.configure(text=original_text))

def reset_all_text():
    source_textbox.delete("1.0", ctk.END)
    for textbox in translations.values():
        textbox.delete("1.0", ctk.END)
    update_character_counts()

def create_language_section(label_text, lang_code, is_input=False):
    outer_frame = ctk.CTkFrame(app)
    outer_frame.pack(padx=10, pady=5, fill='x')

    if is_input:
        outer_frame.configure(fg_color=INPUT_FRAME_COLOR)
        translate_button = ctk.CTkButton(outer_frame, text="Translate", command=translate_text, 
                                         fg_color=TRANSLATE_BUTTON_COLOR, hover_color=TRANSLATE_BUTTON_HOVER_COLOR,
                                         width=105)
        translate_button.pack(side='left', padx=10, pady=10)
    else:
        try:
            icon_path = os.path.join(os.path.dirname(__file__), f"{lang_code}.png")
            icon = ctk.CTkImage(Image.open(icon_path).resize((20, 20)))
            ctk.CTkLabel(outer_frame, image=icon, text="").pack(side='left', padx=(10, 5), pady=10)
        except FileNotFoundError:
            ctk.CTkLabel(outer_frame, text="", width=20).pack(side='left', padx=(10, 5), pady=10)

        ctk.CTkLabel(outer_frame, text=label_text, width=80).pack(side='left', padx=(0, 10), pady=10)

    textbox_frame = ctk.CTkFrame(outer_frame, fg_color="transparent")
    textbox_frame.pack(side='left', padx=10, pady=10, fill='x', expand=True)

    textbox = ctk.CTkTextbox(textbox_frame, height=30)
    textbox.pack(fill='both', expand=True)
    
    if lang_code == 'ar':
        textbox.configure(font=("Calibri", 12))  # Set font for Arabic text
        textbox.configure(scrollbar_button_color=ARABIC_SCROLL_COLOR)  # Set scroll color for Arabic

    textbox.bind("<KeyRelease>", update_character_counts)

    button_frame = ctk.CTkFrame(outer_frame, fg_color="transparent")
    button_frame.pack(side='left', padx=10, pady=10)

    char_count_label = ctk.CTkLabel(button_frame, text=f"0/{MAX_CHARS}", width=70)
    char_count_label.pack(side='left', padx=5)

    if is_input:
        reset_button = ctk.CTkButton(button_frame, text="Reset", command=reset_all_text, 
                                     fg_color=RESET_BUTTON_COLOR, hover_color=RESET_BUTTON_HOVER_COLOR,
                                     width=70)
        reset_button.pack(side='left', padx=5)
    else:
        copy_button = ctk.CTkButton(button_frame, text="Copy", 
                                    command=lambda: copy_to_clipboard(textbox, copy_button), width=70)
        copy_button.pack(side='left', padx=5)

    return textbox, char_count_label

def insert_text_with_alignment(textbox, text, lang):
    textbox.delete("1.0", tk.END)
    if lang == 'AR':
        lines = text.split('\n')
        for line in lines:
            textbox.insert(tk.END, line.rjust(len(line) + 2) + '\n')
    else:
        textbox.insert(tk.END, text)

def translate_text():
    source_text = source_textbox.get("1.0", "end-1c")
    for lang, textbox in translations.items():
        try:
            result = translator.translate_text(source_text, target_lang=lang)
            translated_text = limit_chars(result.text)
            insert_text_with_alignment(textbox, translated_text, lang)
        except Exception as e:
            insert_text_with_alignment(textbox, f"Error: {str(e)}", lang)
    update_character_counts()

# Create input section
source_textbox, input_char_count_label = create_language_section("", 'input', is_input=True)

# Create sections for each language
languages = [
    ("Arab", 'AR'), ("Belanda", 'NL'), ("Inggris", 'EN-US'), ("Indonesia", 'ID'),
    ("Italia", 'IT'), ("Jepang", 'JA'), ("Jerman", 'DE'), ("Prancis", 'FR'),
    ("Rusia", 'RU'), ("Spanyol", 'ES')
]

translations = {}
char_count_labels = {}

for label, code in languages:
    textbox, char_count_label = create_language_section(label, code.lower())
    translations[code] = textbox
    char_count_labels[textbox] = char_count_label

# Run the application
app.mainloop()
