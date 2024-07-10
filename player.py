
class Player:
    def __init__(self, name):
        self.name = name
        self.pred = 0
        self.wins = 0
        self.points = 0
        self.total = 0

    def calculate_points(self):
        # Win
        if self.pred == self.wins:
            self.points = 20 + 10 * self.pred
        # Lose
        else:
            diff = abs(self.pred-self.wins)
            self.points = -10 * diff
        # Update total
        self.total += self.points
        return self.points 
