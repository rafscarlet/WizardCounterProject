import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Screen Switcher")
        self.geometry("300x200")

        # Dictionary to hold references to frames
        self.frames = {}

        # Start with the main screen
        self.show_frame("MainScreen")

    def show_frame(self, page_name):
        if page_name not in self.frames:
            frame_class = globals()[page_name]
            frame = frame_class(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        frame = self.frames[page_name]
        frame.tkraise()  # Bring the frame to the front

class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Main Screen")
        label.pack(pady=10)
        button1 = ttk.Button(self, text="Go to Screen 1",
                             command=lambda: controller.show_frame("Screen1"))
        button1.pack(pady=5)
        button2 = ttk.Button(self, text="Go to Screen 2",
                             command=lambda: controller.show_frame("Screen2"))
        button2.pack(pady=5)

class Screen1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="This is Screen 1")
        label.pack(pady=10)
        button = ttk.Button(self, text="Back to Main Screen",
                            command=lambda: controller.show_frame("MainScreen"))
        button.pack(pady=5)

class Screen2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="This is Screen 2")
        label.pack(pady=10)
        button = ttk.Button(self, text="Back to Main Screen",
                            command=lambda: controller.show_frame("MainScreen"))
        button.pack(pady=5)

        

if __name__ == "__main__":
    app = App()
    app.mainloop()
