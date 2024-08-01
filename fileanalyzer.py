import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import difflib
from tkinterdnd2 import TkinterDnD, DND_FILES

class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = self.read_file()

    def read_file(self):
        with open(self.file_path, 'r') as file:
            return file.readlines()

    def search_word(self, word):
        results = [line for line in self.content if word in line]
        return results

    def sort_lines(self):
        return sorted(self.content)

    def filter_lines(self, keywords):
        results = [line for line in self.content if any(keyword in line for keyword in keywords)]
        return results

    def save_to_file(self, new_content, output_path):
        with open(output_path, 'w') as file:
            file.writelines(new_content)

    @staticmethod
    def compare_files(file1_path, file2_path):
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        diff = difflib.unified_diff(file1_lines, file2_lines)
        return ''.join(diff)

class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text File Processor")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Drag and drop a file or use the button to select a file")
        self.label.pack(pady=10)

        self.textbox = tk.Text(self, height=15, width=70)
        self.textbox.pack(pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.open_button = tk.Button(self.button_frame, text="Open File", command=self.open_file)
        self.open_button.grid(row=0, column=0, padx=10)

        self.search_button = tk.Button(self.button_frame, text="Search Word", command=self.search_word)
        self.search_button.grid(row=0, column=1, padx=10)

        self.sort_button = tk.Button(self.button_frame, text="Sort Lines", command=self.sort_lines)
        self.sort_button.grid(row=0, column=2, padx=10)

        self.filter_button = tk.Button(self.button_frame, text="Filter Lines", command=self.filter_lines)
        self.filter_button.grid(row=0, column=3, padx=10)

        self.compare_button = tk.Button(self.button_frame, text="Compare Files", command=self.compare_files)
        self.compare_button.grid(row=0, column=4, padx=10)

        self.textbox.drop_target_register(DND_FILES)
        self.textbox.dnd_bind('<<Drop>>', self.drop_file)

        self.file_processor = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.load_file(file_path)

    def drop_file(self, event):
        file_path = event.data.strip("{}")
        if os.path.isfile(file_path):
            self.load_file(file_path)

    def load_file(self, file_path):
        self.file_processor = TextFileProcessor(file_path)
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, "".join(self.file_processor.content))

    def search_word(self):
        if self.file_processor:
            word = simpledialog.askstring("Search Word", "Enter the word to search:")
            results = self.file_processor.search_word(word)
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, "".join(results))

    def sort_lines(self):
        if self.file_processor:
            sorted_lines = self.file_processor.sort_lines()
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, "".join(sorted_lines))

    def filter_lines(self):
        if self.file_processor:
            keywords = simpledialog.askstring("Filter Lines", "Enter keywords separated by commas:").split(',')
            filtered_lines = self.file_processor.filter_lines(keywords)
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, "".join(filtered_lines))

    def compare_files(self):
        file1_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        file2_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file1_path and file2_path:
            diff = TextFileProcessor.compare_files(file1_path, file2_path)
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, diff)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
