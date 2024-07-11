
class Player:
    def __init__(self, name, total=0):
        self.name = name
        self.points = 0
        self.total = int(total)

    def calculate_points(self, pred, wins):
        # Win
        if pred == wins:
            self.points = 20 + 10 * pred
        # Lose
        else:
            diff = abs(pred-wins)
            self.points = -10 * diff
        # Update total
        self.total += self.points
        return self.points 
