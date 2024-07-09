
class Player:
    def __init__(self, name):
        self.name = name
        self.pred = 0
        self.wins = 0
        # self.points = 0
        self.total = 0

    def calculate_points(self):
        if self.pred == self.wins:
            points = 20 + 10 * self.pred

        else:
            diff = abs(self.pred-self.wins)
            points = -10 * diff
        return points 
