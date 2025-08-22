import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip

try:
    import opencc
    converter = opencc.OpenCC('t2s')  # Traditional to Simplified
except ImportError:
    converter = None

class ChineseConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Traditional to Simplified Chinese Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style for better Windows 11 appearance
        style = ttk.Style()
        style.theme_use('winnative')
        
        self.setup_ui()
        
        # Check if opencc is available
        if converter is None:
            self.show_install_message()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Input label
        input_label = ttk.Label(main_frame, text="Traditional Chinese Input:", font=("Microsoft YaHei", 10))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Input text area
        self.input_text = scrolledtext.ScrolledText(
            main_frame, 
            width=70, 
            height=10, 
            font=("Microsoft YaHei", 12),
            wrap=tk.WORD
        )
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(0, 10))
        
        # Convert button
        self.convert_btn = ttk.Button(
            button_frame, 
            text="Convert to Simplified Chinese", 
            command=self.convert_text,
            style="Accent.TButton"
        )
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(
            button_frame, 
            text="Clear All", 
            command=self.clear_all
        )
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Copy button
        copy_btn = ttk.Button(
            button_frame, 
            text="Copy Output", 
            command=self.copy_output
        )
        copy_btn.pack(side=tk.LEFT)
        
        # Output label
        output_label = ttk.Label(main_frame, text="Simplified Chinese Output:", font=("Microsoft YaHei", 10))
        output_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        # Output text area (read-only)
        self.output_text = scrolledtext.ScrolledText(
            main_frame, 
            width=70, 
            height=10, 
            font=("Microsoft YaHei", 12),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.output_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Enter Traditional Chinese text above")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.convert_text())
        self.root.bind('<Control-c>', lambda e: self.copy_output())
        self.root.bind('<Control-l>', lambda e: self.clear_all())
        
    def show_install_message(self):
        message = """OpenCC library is not installed. 
        
To use this converter, please install it using:
pip install opencc-python-reimplemented

Without this library, the conversion will use a basic fallback method."""
        
        messagebox.showwarning("Library Missing", message)
        self.status_var.set("Warning: OpenCC not installed - using basic conversion")
    
    def convert_text(self):
        input_content = self.input_text.get("1.0", tk.END).strip()
        
        if not input_content:
            self.status_var.set("Please enter some Traditional Chinese text first")
            return
        
        try:
            if converter:
                # Use OpenCC for accurate conversion
                simplified = converter.convert(input_content)
                self.status_var.set("Conversion completed using OpenCC")
            else:
                # Basic fallback conversion (limited accuracy)
                simplified = self.basic_conversion(input_content)
                self.status_var.set("Conversion completed using basic method")
            
            # Update output text
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", simplified)
            self.output_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Conversion Error", f"Error during conversion: {str(e)}")
            self.status_var.set("Conversion failed")
    
    def basic_conversion(self, text):
        # Basic traditional to simplified mapping (very limited)
        # This is just a fallback - OpenCC is much more accurate
        basic_map = {
            '繁': '繁', '體': '体', '中': '中', '文': '文',
            '轉': '转', '換': '换', '簡': '简', '化': '化',
            '傳': '传', '統': '统', '對': '对', '應': '应',
            '語': '语', '言': '言', '處': '处', '理': '理',
            '資': '资', '料': '料', '數': '数', '據': '据',
            '電': '电', '腦': '脑', '網': '网', '頁': '页',
            '時': '时', '間': '间', '問': '问', '題': '题',
            '學': '学', '習': '习', '會': '会', '議': '议',
            '國': '国', '家': '家', '經': '经', '濟': '济',
        }
        
        result = ""
        for char in text:
            result += basic_map.get(char, char)
        
        return result
    
    def copy_output(self):
        output_content = self.output_text.get("1.0", tk.END).strip()
        
        if not output_content:
            self.status_var.set("No output to copy")
            return
        
        try:
            pyperclip.copy(output_content)
            self.status_var.set("Output copied to clipboard!")
        except Exception as e:
            # Fallback to tkinter clipboard
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(output_content)
                self.root.update()
                self.status_var.set("Output copied to clipboard!")
            except Exception:
                messagebox.showerror("Copy Error", "Failed to copy to clipboard")
    
    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.status_var.set("Ready - Enter Traditional Chinese text above")

def main():
    # Create the main window
    root = tk.Tk()
    
    # Create and run the application
    app = ChineseConverter(root)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()