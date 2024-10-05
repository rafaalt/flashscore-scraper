class Game:
    def __init__(self, id, homeTeam, awayTeam, scoreHome, scoreAway):
        self.id = id
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.scoreHome = scoreHome
        self.scoreAway = scoreAway
        self.pointsHome, self.pointsAway = self.getPoints(int(scoreHome), int(scoreAway))
    
    def __str__(self):
        return f"Jogo {self.id}: {self.homeTeam} {self.scoreHome} x {self.scoreAway} {self.awayTeam} | {self.pointsHome}#{self.pointsAway}"
    
    def getPoints(self, scoreHome, scoreAway):
        if scoreHome > scoreAway:
            return 3, 0
        elif scoreAway > scoreHome:
            return 0, 3
        else: 
            return 1, 1

class Team:
    def __init__(self, name, imageUrl):
        self.name = name
        self.imageUrl = imageUrl

    def __str__(self):
        return self.name
    