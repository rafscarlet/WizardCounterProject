from tkinter import *
from tkinter import messagebox
from player import Player
import random

TITLE_FONT = ('Courier', 20, "bold")
NORMAL_FONT = ('Courier', 13, "normal")
BOLD_FONT = ('Courier', 12, "bold")
SMALLER_FONT = ('Courier', 10, "italic")

with open("phrases/round.txt") as phrases:
    round_phrases = phrases.readlines()

with open("phrases/leader.txt") as phrases:
    leader_phrases = phrases.readlines()

with open("phrases/loser.txt") as phrases:
    loser_phrases = phrases.readlines()


class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.title('Wizard Counter by gRaF')
        self.geometry('600x500')
        self.config(padx=40, pady=10)

        # Dictionary to hold references to frames
        self.frames = {}

        # Start with the main screen
        self.show_frame("StartScreen", None)

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
                messagebox.showwarning(
                    title='Oops...', message="You can't enter an empty name! Try again")
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
        center_frame.grid(row=0, column=0, sticky="nsew", padx=100, pady=50)

        label1 = Label(center_frame, text="Wizard Counter", font=TITLE_FONT)
        # Add some vertical padding
        label1.grid(row=0, column=0, pady=20, columnspan=2)

        label2 = Label(
            center_frame, text="Enter Player's Names Below\n😎", font=NORMAL_FONT)
        # Add some vertical padding
        label2.grid(row=1, column=0, pady=20, columnspan=2)

        label3 = Label(
            center_frame, text="Note: You have to enter 3-6 names!", font=SMALLER_FONT)
        # Add some vertical padding
        label3.grid(row=2, column=0, pady=20, columnspan=2)

        name_entry = Entry(center_frame, font=NORMAL_FONT)
        name_entry.focus()
        # Anchor removed for grid layout
        name_entry.grid(row=3, column=0, columnspan=2, pady=10)

        names_label = Label(
            center_frame, text='The names you enter will appear here!', font=SMALLER_FONT)
        # Anchor removed for grid layout
        names_label.grid(row=4, column=0, columnspan=2, pady=10)

        add_btn = Button(center_frame, text="Add", width=20,
                         font=NORMAL_FONT, command=add_player)
        # Anchor removed for grid layout
        add_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Button frame
        button_frame = Frame(center_frame)
        button_frame.grid(row=6, column=0, columnspan=2)

        exit_btn = Button(button_frame, text="Exit",
                          font=NORMAL_FONT, command=exit)
        exit_btn.grid(row=0, column=0, padx=10, pady=10)

        next_btn = Button(button_frame, text="Next", font=NORMAL_FONT,
                          command=lambda: self.controller.show_frame(page_name='GameScreen', players=self.players))
        next_btn.grid(row=0, column=1, padx=10, pady=10)


class GameScreen(Frame):
    def __init__(self, parent, controller, players: list[Player]):
        super().__init__(parent)
        self.controller = controller
        # self.players = players
        self.players = {'mike': Player('mike'), 'koko': Player(
            'koko'), 'dona': Player('dona')}

        framebox = Frame(self)
        framebox.grid(row=0, column=0, padx=50, pady=10, sticky='nsew')
        for i, j in zip(range(len(self.players)+1), range(5)):
            framebox.rowconfigure(i, pad=20)
            framebox.columnconfigure(j, weight=1, pad=10)

        label1 = Label(framebox, text='Prediction',
                       font=BOLD_FONT, justify='center')
        label1.grid(row=0, column=1, sticky='EW')

        label2 = Label(framebox, text='Wins', font=BOLD_FONT, justify='center')
        label2.grid(row=0, column=2, sticky='EW')

        label3 = Label(framebox, text='Round',
                       font=BOLD_FONT, justify='center')
        label3.grid(row=0, column=3, sticky='EW')

        label4 = Label(framebox, text='Total',
                       font=BOLD_FONT, justify='center')
        label4.grid(row=0, column=4, sticky='EW')

        # Entry boxes and labels
        self.predbox_dict = {}
        self.winbox_dict = {}
        self.points_dict = {}
        self.total_dict = {}
        label_dict = {p_name: Label(
            framebox, text=p_name, font=BOLD_FONT) for p_name in self.players}

        for name, j in zip(self.players, range(len(self.players))):
            label_dict[name] = Label(framebox, text=name, font=BOLD_FONT)
            label_dict[name].grid(row=j+1, column=0, sticky='EW')

            self.predbox_dict[name] = Entry(
                framebox, font=NORMAL_FONT, width=5, justify='center')
            # self.predbox_dict[name].insert(0, string='0')
            self.predbox_dict[name].grid(row=j+1, column=1)

            self.winbox_dict[name] = Entry(
                framebox, font=NORMAL_FONT, width=5, justify='center')
            # self.winbox_dict[name].insert(0, string='0')
            self.winbox_dict[name].grid(row=j+1, column=2)

            self.points_dict[name] = Label(framebox, text=0, font=BOLD_FONT)
            self.points_dict[name].grid(row=j+1, column=3, sticky='EW')

            self.total_dict[name] = Label(framebox, text=0, font=BOLD_FONT)
            self.total_dict[name].grid(row=j+1, column=4, sticky='EW')

        calculate_btn = Button(framebox, text='Calculate',
                               font=BOLD_FONT, width=15, command=self.calculate_points)
        calculate_btn.grid(row=len(self.players)+1,
                           column=1, columnspan=2, pady=5)

        end_game_btn = Button(framebox, text='End Game',
                              font=BOLD_FONT, width=15, command=self.end_game)
        end_game_btn.grid(row=len(self.players)+1,
                          column=3, columnspan=2, pady=5)

        narratorbox = Frame(self)
        narratorbox.grid(row=len(self.players)+2, column=0, columnspan=5, pady=30,sticky="N")

        self.narrator = Label(narratorbox, text='Play your first round to see who is leading!',
                         font=NORMAL_FONT, justify='center', wraplength=400)
        self.narrator.grid(row=0, column=0, sticky="EW")



    def calculate_points(self):
        
        try: 
            for name, player in self.players.items():
                pred = self.predbox_dict[name].get()
                wins = self.winbox_dict[name].get()

                if len(pred) == 0 or len(pred)>3 or len(wins)>3 or len(wins) ==0:
                    raise ValueError("Empty string or longer than 3-digits.")
                
                player.pred = int(pred)
                player.wins = int(wins)
                player.calculate_points()
                # Update Labels
                self.points_dict[name].config(text=player.points)
                self.total_dict[name].config(text=player.total)


        except ValueError:
                    messagebox.showerror(
                        title="Huh?", message="You shall only input integer numbers with up to 3 digits! (no empty boxes!)")
                    
        else: 
            self.update_narrator()
            self.clear_boxes()

    
    def end_game(self):
        scores = ''
        self.clear_boxes()
        for name, player in self.players.items():
            scores +=f'\n{name}: {player.total}'
        with open('game_logs.txt','w') as logs:
            logs.write(scores)

        winner = self.update_narrator()
        
        self.narrator.config(text=f'Congratulations {winner}!\nYou nailed it!{scores}')


    def clear_boxes(self):
        for name in self.players:
            self.predbox_dict[name].delete(0, END)
            self.winbox_dict[name].delete(0, END)
            self.points_dict[name].config(text='0')


    def update_narrator(self):
        round_phr = random.choice(round_phrases)
        leader_phr = random.choice(leader_phrases)
        loser_phr = random.choice(loser_phrases)
        
        round_list = [player.points for player in self.players.values()]
        total_list = [player.total for player in self.players.values()]

        max_round = max(round_list)
        max_total = max(total_list)
        min_total = min(total_list)

        rounders = [name for name, player in self.players.items() if player.points == max_round]
        leaders = [name for name, player in self.players.items() if player.total == max_total]
        losers = [name for name, player in self.players.items() if player.total == min_total]

        rounders = ' and '.join(rounders)
        leaders = ' and '.join(leaders)
        losers = ' and '.join(losers)

        round_phr = round_phr.replace('[NAME]', rounders)
        leader_phr = leader_phr.replace('[NAME]', leaders)
        loser_phr = loser_phr.replace('[NAME]', losers)

        phrase_choice = random.choice([round_phr, leader_phr, loser_phr])

        self.narrator.config(text=phrase_choice)

        return leaders

app = MyApp()
app.mainloop()
