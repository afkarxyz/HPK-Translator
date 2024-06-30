import os
import customtkinter as ctk
from deepl import Translator
from PIL import Image

# Initialize application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1450x715")
app.title("HPK Translator (DeepL)")

# Set custom icon
icon_path = os.path.join(os.path.dirname(__file__), "translate.ico")
app.iconbitmap(icon_path)

MAX_CHARS = 100

# Custom color for the translate button
TRANSLATE_BUTTON_COLOR = "#1f8b4c"  # A shade of green
TRANSLATE_BUTTON_HOVER_COLOR = "#176839"  # A darker shade of green for hover effect

# Initialize DeepL translator
translator = Translator("input your API key")

def limit_chars(text):
    return text[:MAX_CHARS]

def translate_text():
    source_text = source_textbox.get("1.0", "end-1c")
    if source_text == "Input Text...":
        return
    translations = {
        'AR': arab_textbox,
        'NL': belanda_textbox,
        'EN-US': inggris_textbox,
        'FR': prancis_textbox,
        'DE': jerman_textbox,
        'ID': indonesia_textbox,
        'IT': italia_textbox,
        'JA': jepang_textbox,
        'RU': rusia_textbox,
        'ES': spanyol_textbox
    }
    for lang, textbox in translations.items():
        try:
            result = translator.translate_text(source_text, target_lang=lang)
            translated_text = limit_chars(result.text)
            textbox.delete("1.0", ctk.END)
            textbox.insert(ctk.END, translated_text)
        except Exception as e:
            textbox.delete("1.0", ctk.END)
            textbox.insert(ctk.END, f"Error: {str(e)}")
    update_character_counts()

def update_character_counts(event=None):
    input_text = source_textbox.get("1.0", "end-1c")
    if input_text == "Input Text...":
        input_char_count_label.configure(text=f"0/{MAX_CHARS}")
        return
    if len(input_text) > MAX_CHARS:
        input_text = limit_chars(input_text)
        source_textbox.delete("1.0", ctk.END)
        source_textbox.insert(ctk.END, input_text)
    input_char_count_label.configure(text=f"{len(input_text)}/{MAX_CHARS}")
    
    translations = {
        arab_textbox: arab_char_count_label,
        belanda_textbox: belanda_char_count_label,
        inggris_textbox: inggris_char_count_label,
        indonesia_textbox: indonesia_char_count_label,
        italia_textbox: italia_char_count_label,
        jepang_textbox: jepang_char_count_label,
        jerman_textbox: jerman_char_count_label,
        prancis_textbox: prancis_char_count_label,
        rusia_textbox: rusia_char_count_label,
        spanyol_textbox: spanyol_char_count_label
    }
    for textbox, label in translations.items():
        text = textbox.get("1.0", "end-1c")
        if len(text) > MAX_CHARS:
            text = limit_chars(text)
            textbox.delete("1.0", ctk.END)
            textbox.insert(ctk.END, text)
        label.configure(text=f"{len(text)}/{MAX_CHARS}")

def copy_to_clipboard(textbox, copy_button):
    app.clipboard_clear()
    app.clipboard_append(textbox.get("1.0", "end-1c"))
    
    # Change button text to "Copied"
    original_text = copy_button.cget("text")
    copy_button.configure(text="Copied")
    
    # Schedule the button text to change back after 2 seconds
    app.after(2000, lambda: copy_button.configure(text=original_text))

def reset_input():
    source_textbox.delete("1.0", ctk.END)
    source_textbox.insert("1.0", "Input Text...")
    update_character_counts()

RESET_BUTTON_COLOR = "#e74c3c"
RESET_BUTTON_HOVER_COLOR = "#c0392b"

def reset_all_text():
    reset_input()
    for textbox in [arab_textbox, belanda_textbox, inggris_textbox, indonesia_textbox, 
                    italia_textbox, jepang_textbox, jerman_textbox, prancis_textbox, 
                    rusia_textbox, spanyol_textbox]:
        textbox.delete("1.0", ctk.END)
    update_character_counts()

# GUI components for input
source_frame = ctk.CTkFrame(app)
source_frame.pack(padx=10, pady=5, fill='x')

# Increased the width of the reset button
reset_button = ctk.CTkButton(source_frame, text="Reset", command=reset_all_text, 
                             fg_color=RESET_BUTTON_COLOR, hover_color=RESET_BUTTON_HOVER_COLOR,
                             width=105)
reset_button.pack(side='left', padx=10, pady=10)

source_textbox = ctk.CTkTextbox(source_frame, height=30)
source_textbox.pack(side='left', padx=10, pady=10, fill='x', expand=True)
source_textbox.insert("1.0", "Input Text...")
source_textbox.bind("<FocusIn>", lambda event: on_entry_click(event, source_textbox))
source_textbox.bind("<FocusOut>", lambda event: on_focusout(event, source_textbox))
source_textbox.bind("<KeyRelease>", update_character_counts)

def on_entry_click(event, textbox):
    if textbox.get("1.0", "end-1c") == "Input Text...":
        textbox.delete("1.0", ctk.END)
        textbox.configure(text_color=("black", "white"))  # Change text color to default

def on_focusout(event, textbox):
    if textbox.get("1.0", "end-1c") == "":
        textbox.insert("1.0", "Input Text...")
        textbox.configure(text_color="gray")  # Change text color to gray

# Green translate button with hover effect
translate_button = ctk.CTkButton(source_frame, text="Translate", command=translate_text, 
                                 fg_color=TRANSLATE_BUTTON_COLOR, hover_color=TRANSLATE_BUTTON_HOVER_COLOR)
translate_button.pack(side='right', padx=10, pady=10)

input_char_count_label = ctk.CTkLabel(source_frame, text=f"0/{MAX_CHARS}")
input_char_count_label.pack(side='right', padx=10, pady=10)

def create_language_section(label_text, lang_code):
    frame = ctk.CTkFrame(app)
    frame.pack(padx=10, pady=5, fill='x')

    # Try to load the icon, use a default or skip if not found
    try:
        icon_path = os.path.join(os.path.dirname(__file__), f"{lang_code}.png")
        icon = Image.open(icon_path)
        icon = icon.resize((20, 20))  # Adjust size as needed
        icon_ctk = ctk.CTkImage(icon)
        icon_label = ctk.CTkLabel(frame, image=icon_ctk, text="")
        icon_label.pack(side='left', padx=(10, 5), pady=10)
    except FileNotFoundError:
        print(f"Icon for {lang_code} not found. Skipping icon.")
        # Add a blank space to maintain alignment
        blank_label = ctk.CTkLabel(frame, text="", width=20)
        blank_label.pack(side='left', padx=(10, 5), pady=10)

    label = ctk.CTkLabel(frame, text=label_text, width=80)
    label.pack(side='left', padx=(0, 10), pady=10)

    textbox = ctk.CTkTextbox(frame, height=30, width=200)  # Set a fixed width
    textbox.pack(side='left', padx=10, pady=10, fill='x', expand=True)
    textbox.bind("<KeyRelease>", update_character_counts)

    char_count_label = ctk.CTkLabel(frame, text=f"0/{MAX_CHARS}", width=70)  # Set a fixed width
    char_count_label.pack(side='left', padx=10, pady=10)

    copy_button = ctk.CTkButton(frame, text="Copy", command=lambda: copy_to_clipboard(textbox, copy_button), width=70)
    copy_button.pack(side='left', padx=10, pady=10)

    return textbox, char_count_label

# Create sections for each language (in alphabetical order based on language names in Indonesian)
arab_textbox, arab_char_count_label = create_language_section("Arab", 'ar')
belanda_textbox, belanda_char_count_label = create_language_section("Belanda", 'nl')
inggris_textbox, inggris_char_count_label = create_language_section("Inggris", 'en')
indonesia_textbox, indonesia_char_count_label = create_language_section("Indonesia", 'id')
italia_textbox, italia_char_count_label = create_language_section("Italia", 'it')
jepang_textbox, jepang_char_count_label = create_language_section("Jepang", 'ja')
jerman_textbox, jerman_char_count_label = create_language_section("Jerman", 'de')
prancis_textbox, prancis_char_count_label = create_language_section("Prancis", 'fr')
rusia_textbox, rusia_char_count_label = create_language_section("Rusia", 'ru')
spanyol_textbox, spanyol_char_count_label = create_language_section("Spanyol", 'es')

# Run the application
app.mainloop()
