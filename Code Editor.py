import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Editor for Python")
        self.root.geometry("800x600")

        # Text widget for code editing
        self.text = tk.Text(root, wrap="word", undo=True, background="white", foreground="black")
        self.text.pack(expand="yes", fill="both")

        # Configure tags for syntax highlighting
        self.text.tag_configure("comment", foreground="gray")

        # Menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text.edit_redo)

        # Run menu
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run Code", command=self.run_code)

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.dark_mode_var = tk.BooleanVar()
        self.view_menu.add_checkbutton(label="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode)

        # Font size submenu
        self.font_size_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="Font Size", menu=self.font_size_menu)
        self.font_size_menu.add_command(label="Increase", command=self.increase_font_size)
        self.font_size_menu.add_command(label="Decrease", command=self.decrease_font_size)
        self.font_size_menu.add_command(label="Set Font Size", command=self.set_font_size_dialog)

        # Default font size
        self.font_size = 12
        self.set_font_size()

        # Bind events to update syntax highlighting
        self.text.bind("<KeyRelease>", self.highlight_syntax)

    def set_font_size(self):
        font = f"TkFixedFont {self.font_size}"
        self.text.configure(font=font)

    def increase_font_size(self):
        self.font_size += 1
        self.set_font_size()

    def decrease_font_size(self):
        if self.font_size > 1:
            self.font_size -= 1
            self.set_font_size()

    def set_font_size_dialog(self):
        font_size = simpledialog.askstring("Font Size", "Enter Font Size:")
        if font_size:
            try:
                font_size = int(font_size)
                if font_size > 0:
                    self.font_size = font_size
                    self.set_font_size()
                else:
                    messagebox.showwarning("Invalid Font Size", "Font size must be a positive integer.")
            except ValueError:
                messagebox.showwarning("Invalid Font Size", "Font size must be a positive integer.")

    def toggle_dark_mode(self):
        if self.dark_mode_var.get():
            self.text.config(background="#171414", foreground="white")
        else:
            self.text.config(background="white", foreground="black")

    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.root.title("Code Editor for Python")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, content)
            self.root.title(f"Code Editor - {file_path}")

    def save_file(self):
        if not hasattr(self, "file_path"):
            self.save_as_file()
        else:
            content = self.text.get(1.0, tk.END)
            with open(self.file_path, "w") as file:
                file.write(content)
            messagebox.showinfo("Save", "File saved successfully.")

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            content = self.text.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.file_path = file_path
            self.root.title(f"Code Editor - {file_path}")
            messagebox.showinfo("Save", "File saved successfully.")

    def run_code(self):
        code = self.text.get(1.0, tk.END)
        try:
            exec(code)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def highlight_syntax(self, event):
        self.text.tag_remove("comment", "1.0", tk.END)

        code = self.text.get("1.0", tk.END)

        self.tag_comments(code)

    def tag_comments(self, code):
        start_index = "1.0"
        while True:
            start_index = self.text.search(r'#.*?\n', start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.index(f"{start_index} lineend")
            self.text.tag_add("comment", start_index, end_index)
            start_index = end_index


if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()
