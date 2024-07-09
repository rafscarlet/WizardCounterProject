from tkinter import *
from tkinter import messagebox
from player import Player

TITLE_FONT = ('Courier', 20, "bold")
NORMAL_FONT = ('Courier', 13, "normal")
BOLD_FONT = ('Courier', 10, "bold")
SMALLER_FONT = ('Courier', 8, "italic")

class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.title('Wizard Counter by gRaF')
        self.geometry('380x500')
        self.config(padx=50, pady=50)

        # Dictionary to hold references to frames
        self.frames = {}

        # Start with the main screen
        self.show_frame("StartScreen", [])

    def show_frame(self, page_name, players):
        if page_name not in self.frames:
            frame_class = globals()[page_name]
            frame = frame_class(parent=self, controller=self, players=players)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # Use grid layout
        
        frame = self.frames[page_name]
        frame.tkraise() 


class StartScreen(Frame):
    def __init__(self, parent, controller: MyApp, players: list[Player]):
        super().__init__(parent)
        self.controller = controller
        self.player_names = []
        self.players = {}

        def add_player():
            name = name_entry.get()

            if len(name.strip()) == 0:
                messagebox.showwarning(title='Oops...', message="You can't enter an empty name! Try again")
            else:
                # Make a string with all the names and show it in the label
                self.player_names.append(name)
                players_str = 'Names: ' + ', '.join(self.player_names)
                names_label.config(text=players_str)

                # Add each name to player dictionary 
                self.players[name] = Player(name)

            # Clear the entry box
            name_entry.delete(0, END)

        # Create a frame to center the content
        center_frame = Frame(self)
        center_frame.grid(row=0, column=0, sticky="nsew")

        label1 = Label(center_frame, text="Wizard Counter", font=TITLE_FONT)
        label1.grid(row=0, column=0, pady=20, columnspan=2)  # Add some vertical padding

        label2 = Label(center_frame, text="Enter Player's Names Below\n😎", font=NORMAL_FONT)
        label2.grid(row=1, column=0, pady=20, columnspan=2)  # Add some vertical padding

        label3 = Label(center_frame, text="Note: You have to enter 3-6 names!", font=SMALLER_FONT)
        label3.grid(row=2, column=0, pady=20, columnspan=2)  # Add some vertical padding

        name_entry = Entry(center_frame, font=NORMAL_FONT)
        name_entry.focus()
        name_entry.grid(row=3, column=0, columnspan=2, pady=10)  # Anchor removed for grid layout

        names_label = Label(center_frame, text='The names you enter will appear here!', font=SMALLER_FONT)
        names_label.grid(row=4, column=0, columnspan=2, pady=10)  # Anchor removed for grid layout

        add_btn = Button(center_frame, text="Add", width=20, font=NORMAL_FONT, command=add_player)
        add_btn.grid(row=5, column=0, columnspan=2, pady=10)  # Anchor removed for grid layout

        # Button frame
        button_frame = Frame(center_frame)
        button_frame.grid(row=6, column=0, columnspan=2)

        exit_btn = Button(button_frame, text="Exit", font=NORMAL_FONT, command=exit)
        exit_btn.grid(row=0, column=0, padx=10, pady=10)

        next_btn = Button(button_frame, text="Next", font=NORMAL_FONT,
                          command=lambda: self.controller.show_frame(page_name='GameScreen', players=self.players))
        next_btn.grid(row=0, column=1, padx=10, pady=10)


class GameScreen(Frame):
    def __init__(self, parent, controller, players: list[Player]):
        super().__init__(parent)
        self.controller = controller
        self.players = players
        print(self.players)

        label = Label(self, text='Game Screen', font=TITLE_FONT, justify='center')
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')  # Adjust padding and alignment for grid

        # Add more widgets or functionality as needed



app = MyApp()
app.mainloop()
