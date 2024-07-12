from tkinter import *
from tkinter import messagebox
from player import Player
import random
import csv
import webbrowser

# ------ FONTS ------- #
TITLE_FONT = ('Courier', 20, "bold")
NORMAL_FONT = ('Courier', 13, "normal")
BOLD_FONT = ('Courier', 12, "bold")
SMALLER_FONT = ('Courier', 10, "italic")

# ------ COLOR PALETTE ------ #
BLACK = '#0F1035'
NAVY = '#365486'
BLUE = '#7FC7D9'
WHITE = '#DCF2F1'

# ------- QUOTES ------ #
with open("phrases/round.txt") as phrases:
    round_phrases = phrases.readlines()

with open("phrases/leader.txt") as phrases:
    leader_phrases = phrases.readlines()

with open("phrases/loser.txt") as phrases:
    loser_phrases = phrases.readlines()

with open("phrases/roast.txt") as phrases:
    roast_phrases = phrases.readlines()


class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.title('Wizard Counter by gRaF')
        self.geometry('600x500')
        self.config(padx=40, pady=10)
        self.config(bg=BLUE)

        # Dictionary to hold references to frames
        self.frames = {}

        # Start with the main screen
        self.show_frame("StartScreen", {})

    def show_frame(self, page_name, players):
        frame_class = globals()[page_name]
        frame = frame_class(parent=self, controller=self, players=players)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[page_name]
        frame.tkraise()


class StartScreen(Frame):
    def __init__(self, parent, controller: MyApp, **kwargs):
        super().__init__(parent)
        self.controller = controller
        self.players = {}
        self.config(bg=BLUE)

        center_frame = Frame(self)
        center_frame.config(bg=BLUE, highlightthickness=0)
        center_frame.grid(row=0, column=0, padx=150, pady=50)

        label1 = Label(center_frame, text="Wizard Counter", font=TITLE_FONT, bg=BLUE, highlightthickness=0)
        label1.grid(row=0, column=0, pady=60, columnspan=2, sticky='EW')

        new_game_btn = Button(center_frame, text="New Game", width = 10,bg=BLACK, fg=WHITE, font=NORMAL_FONT, command=self.new_game)
        new_game_btn.grid(row=1, column=0, sticky='N', padx=50, pady=5)

        load_btn = Button(center_frame, text="Load Game", width = 10,bg=BLACK, fg=WHITE, font=NORMAL_FONT, command=self.load_game)
        load_btn.grid(row=2, column=0, sticky='N', padx=50, pady=5)

        rules_btn = Button(center_frame, text="Rules", width = 10,bg=BLACK, fg=WHITE, font=NORMAL_FONT, command=self.open_pdf)
        rules_btn.grid(row=3, column=0, sticky='N', padx=50, pady=5)

        exit_btn = Button(center_frame, text="Exit", width = 10,bg=BLACK, fg=WHITE, font=NORMAL_FONT, command=exit)
        exit_btn.grid(row=4, column=0, sticky='N', padx=50, pady=5)

    def new_game(self):
        self.players = {}
        self.controller.show_frame("PlayerInputScreen", players=self.players)

    def load_game(self):
        try:
            self.players = {}
            with open('game_logs.csv') as logs:
                reader = csv.reader(logs, delimiter=',', lineterminator='\n')
                for row in reader:
                    name = row[0].strip()
                    score = row[1].strip()
                    self.players[name] = Player(name, total=score)

            if self.players == {}:
                raise ValueError

        except:
            messagebox.showerror(title='Logs Not Found', message="There aren't any game logs. You need to start a new game.")

        else:
            info = ''
            for name, player in self.players.items():
                info += f'↪ {name}: {player.total}\n'

            saidYes = messagebox.askyesno(title='Logs Found', message=f'Here is the data I found:\n\n{info}\n Do you want to continue this game?')
            if saidYes:
                self.controller.show_frame('GameScreen', players=self.players)
            else:
                self.players = {}

    def open_pdf(self):
        webbrowser.open_new_tab(url="https://cdn.1j1ju.com/medias/f1/8e/ad-wizard-rulebook.pdf")
    

class PlayerInputScreen(Frame):
    def __init__(self, parent, controller: MyApp, players):
        super().__init__(parent)
        self.controller = controller
        self.players = players
        self.config(bg=BLUE, highlightthickness=0)

        # Create a frame to center the content
        center_frame = Frame(self)
        center_frame.config(bg=BLUE)
        center_frame.grid(row=0, column=0, sticky="nsew", padx=100, pady=40)

        label1 = Label(center_frame, text="Enter Player's Names Below\n😎", bg=BLUE, highlightthickness=0, font=NORMAL_FONT)
        label1.grid(row=1, column=0, pady=20, columnspan=2)

        label2 = Label(center_frame, text="Note: You have to enter 3-6 names!", bg=BLUE, fg=NAVY, font=SMALLER_FONT)
        label2.grid(row=2, column=0, pady=10, columnspan=2)

        self.name_entry = Entry(center_frame, width=15, font=NORMAL_FONT, bg=WHITE)
        self.name_entry.focus()
        self.name_entry.grid(row=3, column=0, pady=10)

        add_btn = Button(center_frame, text="Add", bg=NAVY, fg=WHITE, width=10, font=BOLD_FONT, command=self.add_player)
        add_btn.grid(row=3, column=1)

        self.names_label = Label(center_frame, bg=BLUE, wraplength=300, width=40, height=2, font=SMALLER_FONT)
        self.update_label()
        self.names_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Button frame
        button_frame = Frame(center_frame)
        button_frame.grid(row=6, column=0, columnspan=2)
        button_frame.config(bg=BLUE)

        reset_btn = Button(button_frame, text="Reset", width=23, bg=NAVY, fg=WHITE,
                           font=NORMAL_FONT, command=self.reset_players)
        reset_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        exit_btn = Button(button_frame, text="Exit", width=10, bg=NAVY, fg=WHITE,
                          font=NORMAL_FONT, command=exit)
        exit_btn.grid(row=1, column=0, padx=5, pady=10)

        next_btn = Button(button_frame, text="Next", width=10, bg=NAVY, fg=WHITE,
                          font=NORMAL_FONT, command=self.go_to_game)
        next_btn.grid(row=1, column=1, padx=5, pady=10)

    def reset_players(self):
        self.players = {}
        self.update_label()
        self.name_entry.delete(0, END)

    def add_player(self):
        name = self.name_entry.get().title()

        # Check user's input
        if len(self.players) >= 6:
            messagebox.showwarning(title='Too many players!', message="There can only be up to 6 players! \n(*Game's rules not mine*)")

        elif len(name.strip()) == 0:
            messagebox.showwarning(title='Empty Name', message="You can't enter an empty name! Try again.")

        elif len(name.strip()) > 10:
            messagebox.showwarning(title='Too big name', message="That's too many characters. Try again.")

        elif name in self.players:
            messagebox.showwarning(title='Repetition', message="You have already entered this name. Try again.")
            self.name_entry.delete(0, END)

        else:
            # Add each name to player dictionary
            self.players[name] = Player(name.strip())
            # Clear the entry box
            self.name_entry.delete(0, END)
            # Update the name label text
            self.update_label()

    def update_label(self):

        if len(self.players) == 0:
            label_text = 'The names you enter will appear here!'
        else:
            namelist = []
            for name in self.players:
                namelist.append(name)
            label_text = 'Names: ' + ', '.join(namelist)

        self.names_label.config(text=label_text)

    def go_to_game(self):
        if len(self.players) < 3:
            messagebox.showwarning(
                title="Hmmm", message="There are not enough players! \nThis game is designed for 3-6 players")
        else:
            self.controller.show_frame(page_name='GameScreen', players=self.players)


class GameScreen(Frame):
    def __init__(self, parent, controller, players: list[Player]):
        super().__init__(parent)
        self.controller = controller
        self.players = players
        self.config(bg=BLUE)

        # -------- UI -------- #
        framebox = Frame(self)
        framebox.config(bg=NAVY, highlightcolor=WHITE, highlightthickness=1)
        framebox.grid(row=0, column=0, pady=50, padx=40)
        for i, j in zip(range(len(self.players)+1), range(5)):
            framebox.rowconfigure(i, pad=20)
            framebox.columnconfigure(j, pad=20)

        label1 = Label(framebox, text='Prediction', bg=NAVY, fg=WHITE, font=BOLD_FONT, justify='center')
        label1.grid(row=0, column=1, sticky='SEW')

        label2 = Label(framebox, text='Wins', font=BOLD_FONT, bg=NAVY, fg=WHITE, justify='center')
        label2.grid(row=0, column=2, sticky='SEW')

        label3 = Label(framebox, text='Round', bg=NAVY, fg=WHITE, font=BOLD_FONT, justify='center')
        label3.grid(row=0, column=3, sticky='SEW')

        label4 = Label(framebox, text='Total  ', bg=NAVY, fg=WHITE, font=BOLD_FONT, justify='center')
        label4.grid(row=0, column=4, sticky='SEW')

        # Entry boxes and labels
        self.predbox_dict = {}
        self.winbox_dict = {}
        self.points_dict = {}
        self.total_dict = {}
        label_dict = {p_name: Label(framebox, text=p_name, font=BOLD_FONT) for p_name in self.players}

        for name, j in zip(self.players, range(len(self.players))):

            label_dict[name] = Label(framebox, text=name, bg=NAVY, fg=WHITE, font=BOLD_FONT)
            label_dict[name].grid(row=j+1, column=0, sticky='EW')

            self.predbox_dict[name] = Entry(framebox, font=NORMAL_FONT, width=5, justify='center')
            # self.predbox_dict[name].insert(0, string='0')
            self.predbox_dict[name].grid(row=j+1, column=1)

            self.winbox_dict[name] = Entry(framebox, font=NORMAL_FONT, width=5, justify='center')
            # self.winbox_dict[name].insert(0, string='0')
            self.winbox_dict[name].grid(row=j+1, column=2)

            self.points_dict[name] = Label(framebox, text=0, bg=NAVY, fg=WHITE, font=BOLD_FONT)
            self.points_dict[name].grid(row=j+1, column=3, sticky='EW')

            self.total_dict[name] = Label(framebox, text=self.players[name].total, bg=NAVY, fg=WHITE, font=BOLD_FONT)
            self.total_dict[name].grid(row=j+1, column=4, sticky='EW')

        # Buttons
        save_btn = Button(framebox, text='Save', bg=BLACK, fg=WHITE,
                          font=BOLD_FONT, width=8, command=self.save_game)
        save_btn.grid(row=len(self.players)+1, column=0, pady=10)

        calculate_btn = Button(framebox, text='Calculate', bg=BLACK, fg=WHITE,
                               font=BOLD_FONT, width=10, command=self.calculate_points)
        calculate_btn.grid(row=len(self.players)+1,
                           column=1, columnspan=2, pady=5)

        end_game_btn = Button(framebox, text='End Game', bg=BLACK, fg=WHITE,
                              font=BOLD_FONT, width=10, command=self.end_game)
        end_game_btn.grid(row=len(self.players)+1,
                          column=3, columnspan=2, pady=5)

        narratorbox = Frame(self)
        narratorbox.config(bg=BLUE, highlightthickness=0)
        narratorbox.grid(row=len(self.players)+2, column=0,
                         columnspan=5, pady=10, sticky="NS")

        self.narrator = Label(narratorbox, text='Play your first round to see who is leading!', bg=BLUE,
                              font=NORMAL_FONT, justify='center', wraplength=400)
        self.narrator.grid(row=0, column=0, sticky="EW")

    def save_game(self):
        with open('game_logs.csv', 'w') as logs:
            writer = csv.writer(logs, lineterminator='\n')
            for name, player in self.players.items():
                writer.writerow([name, player.total])

        messagebox.showinfo(
            title='Success!', message="The game data has been stored! Come back and load it to continue playing!")

    def calculate_points(self):
        try:
            for name, player in self.players.items():
                pred = self.predbox_dict[name].get()
                wins = self.winbox_dict[name].get()

                if len(pred) == 0 or len(pred) > 3 or len(wins) > 3 or len(wins) == 0:
                    raise ValueError("Empty string or longer than 3-digits.")

                player.calculate_points(int(pred), int(wins))

                # Update Labels
                self.points_dict[name].config(text=player.points)
                self.total_dict[name].config(text=player.total)

        except ValueError:
            messagebox.showerror(
                title="Huh?", message="You shall only input integer numbers with up to 3 digits! \n(no empty boxes!)")

        else:
            self.update_narrator()
            self.clear_boxes()

    def clear_boxes(self):
        for name in self.players:
            self.predbox_dict[name].delete(0, END)
            self.winbox_dict[name].delete(0, END)

    def update_narrator(self):
        round_phr = random.choice(round_phrases)
        leader_phr = random.choice(leader_phrases)
        loser_phr = random.choice(loser_phrases)

        round_list = [player.points for player in self.players.values()]
        total_list = [player.total for player in self.players.values()]

        rounders = [name for name, player in self.players.items()
                    if player.points == max(round_list)]
        leaders = [name for name, player in self.players.items()
                   if player.total == max(total_list)]
        losers = [name for name, player in self.players.items()
                  if player.total == min(total_list)]

        # rounders_str = ' and '.join(rounders)
        # losers_str = ' and '.join(losers)
        # leaders_str = ' and '.join(leaders)

        round_phr = round_phr.replace('[NAME]', random.choice(rounders))
        leader_phr = leader_phr.replace('[NAME]', random.choice(leaders))
        loser_phr = loser_phr.replace('[NAME]', random.choice(losers))

        phrase_choice = random.choice([round_phr, leader_phr, loser_phr])

        self.narrator.config(text=phrase_choice)

    def end_game(self):
        go_on = messagebox.askokcancel(title="The End (?)", 
                                    message="If you want to keep the data of this game to continue another time be sure to hit save before leaving!\nDo you want to proceed to the leaderboard?")
        if go_on:
            self.controller.show_frame('LeaderboardScreen', players=self.players)


class LeaderboardScreen(Frame):
    def __init__(self, parent, controller: MyApp, players: list[Player]):
        super().__init__(parent)
        self.controller = controller
        self.players = players
        self.config(bg=BLUE)

        playerlist = [self.players[name] for name in self.players]
        leaderboard = sorted(playerlist, key=lambda x: x.total, reverse=True)

        total_list = [player.total for player in self.players.values()]
        winners = [name for name, player in self.players.items() if player.total == max(total_list)]
        losers = [name for name, player in self.players.items() if player.total == min(total_list)]
        winners_str = ' and '.join(winners)

        namestr = ''
        scorestr = ''
        for player in leaderboard:
            namestr += (f'{player.name}\n')
            scorestr += (f'{player.total}\n')

        # UI
        centerframe = Frame(self)
        centerframe.config(bg=BLUE, highlightthickness=0)
        centerframe.grid(row=0, column=0, sticky='nsew', padx=120)
        for i, j in zip(range(5), range(2)):
            centerframe.rowconfigure(i, weight=1, pad=50)
            centerframe.columnconfigure(j, weight=1)

        title_label = Label(centerframe, text='GG!😎', bg=BLUE, fg= BLACK, font=TITLE_FONT)
        title_label.grid(row=0, column=0, columnspan=2, sticky='EW')

        winner_label = Label(centerframe,  bg=BLUE, fg='red', text=f'Congratulations to \n{winners_str}!🎉', font=BOLD_FONT)
        winner_label.grid(row=1, column=0, columnspan=2, sticky='EW')

        names_label = Label(centerframe, text=namestr,  bg=BLUE, fg= BLACK, font=NORMAL_FONT)
        names_label.grid(row=2, column=0, sticky='ns')

        score_label = Label(centerframe, text=scorestr,  bg=BLUE, fg= BLACK, font=NORMAL_FONT)
        score_label.grid(row=2, column=1, sticky='ns')

        # Roast Label
        winner = random.choice(winners)
        loser = random.choice(losers)
        chosen_phrase = random.choice(roast_phrases)
        chosen_phrase = chosen_phrase.replace("[WINNER]", winner)
        chosen_phrase = chosen_phrase.replace("[LOSER]", loser)
        roast_label = Label(centerframe, text=chosen_phrase,  bg=BLUE, fg= BLACK, font=BOLD_FONT, justify='center', wraplength=300)
        roast_label.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Buttons
        new_game_btn = Button(centerframe, text='New Game', bg=BLACK, fg= WHITE, width=10, font=BOLD_FONT, command=self.new_game)
        new_game_btn.grid(row=4, column=1, pady=20)

        exit_btn = Button(centerframe, text='Exit', width=10,  bg=BLACK, fg= WHITE, font=BOLD_FONT, command=exit)
        exit_btn.grid(row=4, column=0, pady=20)

    def new_game(self):
        same_names = messagebox.askyesno(
            title="Let's go!", message="Will you continue playing with the same names?")
        if same_names:
            for player in self.players.values():
                player.total = 0
            self.controller.show_frame('GameScreen', players=self.players)
        else:
            self.players = {}
            self.controller.show_frame('PlayerInputScreen', players=self.players)


app = MyApp()
app.mainloop()
