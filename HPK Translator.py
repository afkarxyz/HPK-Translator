import os
import customtkinter as ctk
from deep_translator import GoogleTranslator
from PIL import Image

# Inisialisasi aplikasi
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1450x715")
app.title("HPK Translator")

# Set custom icon
icon_path = os.path.join(os.path.dirname(__file__), "translate.ico")
app.iconbitmap(icon_path)

MAX_CHARS = 100

# Custom color for the translate button
TRANSLATE_BUTTON_COLOR = "#1f8b4c"  # A shade of green
TRANSLATE_BUTTON_HOVER_COLOR = "#176839"  # A darker shade of green for hover effect

def limit_chars(text):
    return text[:MAX_CHARS]

def translate_text():
    source_text = source_textbox.get("1.0", "end-1c")
    translations = {
        'ar': arab_textbox,
        'nl': belanda_textbox,
        'en': inggris_textbox,
        'fr': prancis_textbox,
        'de': jerman_textbox,
        'id': indonesia_textbox,
        'it': italia_textbox,
        'ja': jepang_textbox,
        'ru': rusia_textbox,
        'es': spanyol_textbox
    }
    for lang, textbox in translations.items():
        translated_text = GoogleTranslator(source='auto', target=lang).translate(source_text)
        translated_text = limit_chars(translated_text)
        textbox.delete("1.0", ctk.END)
        textbox.insert(ctk.END, translated_text)
    update_character_counts()

def update_character_counts(event=None):
    input_text = source_textbox.get("1.0", "end-1c")
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
    update_character_counts()

RESET_BUTTON_COLOR = "#e74c3c"
RESET_BUTTON_HOVER_COLOR = "#c0392b"

def reset_all_text():
    source_textbox.delete("1.0", ctk.END)
    for textbox in [arab_textbox, belanda_textbox, inggris_textbox, indonesia_textbox, 
                    italia_textbox, jepang_textbox, jerman_textbox, prancis_textbox, 
                    rusia_textbox, spanyol_textbox]:
        textbox.delete("1.0", ctk.END)
    update_character_counts()

# Komponen GUI untuk input
source_label = ctk.CTkLabel(app, text="Input Text")
source_label.pack(pady=(10, 0))

source_frame = ctk.CTkFrame(app)
source_frame.pack(padx=10, pady=5, fill='x')

# Increased the width of the reset button
reset_button = ctk.CTkButton(source_frame, text="Reset", command=reset_all_text, 
                             fg_color=RESET_BUTTON_COLOR, hover_color=RESET_BUTTON_HOVER_COLOR,
                             width=105)  # Increased width from 70 to 120
reset_button.pack(side='left', padx=10, pady=10)

source_textbox = ctk.CTkTextbox(source_frame, height=30)
source_textbox.pack(side='left', padx=10, pady=10, fill='x', expand=True)
source_textbox.bind("<KeyRelease>", update_character_counts)

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

# Membuat bagian untuk setiap bahasa (dalam urutan abjad berdasarkan nama bahasa dalam Bahasa Indonesia)
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

# Menjalankan aplikasi
app.mainloop()
