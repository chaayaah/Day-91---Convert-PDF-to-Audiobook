from tkinter import *
from tkinter import filedialog as fd
import gtts
import pdfplumber
import threading

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

audio_file_name = ""


def open_file():
    global audio_file_name
    audio_file_name = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=[('PDF files', '*.pdf')])
    if audio_file_name:
        pdf_path_var.set(audio_file_name)


def extract_text():
    if audio_file_name:
        with pdfplumber.open(audio_file_name) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages):
                # Extract text and ignore text within tables and figures
                current_text = page.extract_text() or ""
                tables = page.extract_tables()
                images = page.images

                if tables or images:
                    current_text += "See PDF for tables and figures"
                text += current_text

        return text


def text_to_speech(text, output_path, language='en'):
    tts = gtts.gTTS(text, lang=language)
    tts.save(output_path)


def convert_to_mp3():
    pdf_path = pdf_path_var.get()
    if not pdf_path:
        return
    output_path = fd.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if not output_path:
        return
    result_var.set("working...")

    def conversion_thread():
        try:
            text = extract_text()
            text_to_speech(text, output_path)
            result_var.set(f"Complete.\nMP3 file saved at {output_path}")
        except Exception as e:
            result_var.set("Conversion Failed")

    threading.Thread(target=conversion_thread, daemon=True).start()


# create the root window
root = Tk()
root.title('PDF to Audio Converter')

root.geometry("500x200")
root.config(bg=YELLOW, padx=10, pady=20)

pdf_path_var = StringVar()
result_var = StringVar()

frame = Frame(root, padx=10, pady=20, bg=YELLOW)
frame.pack()

pdf_label = Label(frame, text="PDF File: ", font=(FONT_NAME, 10), bg=YELLOW)
pdf_label.grid(column=0, row=1, sticky="e")

pdf_entry = Entry(frame, width=50, textvariable=pdf_path_var)
pdf_entry.grid(column=1, row=1)

# open button
open_button = Button(frame, text='Open', command=open_file, bg=YELLOW, font=(FONT_NAME, 10))
open_button.grid(column=2, row=1, padx=10)

# convert button
convert_button = Button(frame, text="Convert PDF to MP3", command=convert_to_mp3, bg=YELLOW, font=(FONT_NAME, 10))
convert_button.grid(column=1, row=2, pady=20)

ready_entry = Label(frame, textvariable=result_var, bg=YELLOW, font=(FONT_NAME, 10))
ready_entry.grid(column=0, row=3, columnspan=3)

# run the application
root.mainloop()