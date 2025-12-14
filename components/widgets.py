import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkfont

class ModernButton(tk.Button):
    def __init__(self, parent, text="", command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            text=text,
            command=command,
            bg='#1E3A8A',
            fg='white',
            font=('Helvetica', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.config(bg='#3B82F6')
    
    def on_leave(self, e):
        self.config(bg='#1E3A8A')

class CardFrame(tk.Frame):
    def __init__(self, parent, title="", icon="", value="", **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg='white', relief=tk.RAISED, borderwidth=1, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(self, bg='#1E3A8A')
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text=f"{icon} {title}", 
                bg='#1E3A8A', fg='white',
                font=('Helvetica', 10, 'bold')).pack(pady=5)
        
        # Value
        self.value_label = tk.Label(self, text=value, 
                                   font=('Helvetica', 20, 'bold'),
                                   bg='white', fg='#1F2937')
        self.value_label.pack(pady=15)
    
    def update_value(self, new_value):
        self.value_label.config(text=new_value)

class ModernTreeview(ttk.Treeview):
    def __init__(self, parent, columns, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", 
                       background="white",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="white")
        style.map('Treeview', background=[('selected', '#3B82F6')])
        
        # Configure columns
        self['columns'] = columns
        self['show'] = 'headings'
        
        # Configure scrollbars
        self.v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
        self.h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)
        self.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
    
    def pack_with_scrollbars(self, **kwargs):
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, **kwargs)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

class InputField:
    def __init__(self, parent, label_text, input_type="entry", **kwargs):
        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(fill=tk.X, pady=5)
        
        self.label = tk.Label(self.frame, text=label_text, 
                             font=('Helvetica', 10),
                             bg='white', anchor=tk.W)
        self.label.pack(fill=tk.X)
        
        if input_type == "entry":
            self.widget = tk.Entry(self.frame, font=('Helvetica', 10), **kwargs)
        elif input_type == "combobox":
            self.widget = ttk.Combobox(self.frame, font=('Helvetica', 10), **kwargs)
        elif input_type == "text":
            self.widget = tk.Text(self.frame, font=('Helvetica', 10), 
                                 height=kwargs.get('height', 4), **kwargs)
        
        self.widget.pack(fill=tk.X, pady=2)
    
    def get(self):
        if isinstance(self.widget, tk.Text):
            return self.widget.get("1.0", tk.END).strip()
        return self.widget.get()
    
    def set(self, value):
        if isinstance(self.widget, tk.Text):
            self.widget.delete("1.0", tk.END)
            self.widget.insert("1.0", value)
        else:
            self.widget.delete(0, tk.END)
            self.widget.insert(0, value)

class MessageBox:
    @staticmethod
    def show_success(message):
        messagebox.showinfo("Success", message)
    
    @staticmethod
    def show_error(message):
        messagebox.showerror("Error", message)
    
    @staticmethod
    def show_warning(message):
        messagebox.showwarning("Warning", message)
    
    @staticmethod
    def ask_confirm(message):
        return messagebox.askyesno("Confirm", message)

class LoadingScreen:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Loading")
        self.window.geometry("300x100")
        self.window.resizable(False, False)
        
        # Center the window
        self.window.transient(parent)
        self.window.grab_set()
        
        tk.Label(self.window, text="Loading...", 
                font=('Helvetica', 12, 'bold')).pack(pady=20)
        
        self.progress = ttk.Progressbar(self.window, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=20)
        self.progress.start()
    
    def close(self):
        self.progress.stop()
        self.window.destroy()