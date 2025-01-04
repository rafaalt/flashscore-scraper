class Game:
    def __init__(self, id, homeTeam, awayTeam, scoreHome, scoreAway, referee, stadium, capacity, public, date, time, country, round, penaltis):
        self.id = id
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.scoreHome = int(scoreHome)
        self.scoreAway = int(scoreAway)
        self.referee = referee
        self.stadium = stadium
        self.capacity = self.convert_to_int(capacity)
        self.public = self.convert_to_int(public)
        self.date = date
        self.time = time
        self.country = country
        self.round = round
        self.penaltis = penaltis
    
    def __str__(self):
        return f'Jogo {self.id}: {self.homeTeam} {self.scoreHome} x {self.scoreAway} {self.awayTeam}\n{self.stadium} - {self.public} presentes\n{self.date} | {self.time}\n{self.round} {self.penaltis}'
        
    def convert_to_int(self, value):
        value = value.replace(' ', '')
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None

class Team:
    def __init__(self, name, imageUrl):
        self.name = name
        self.imageUrl = imageUrl

    def __str__(self):
        return self.name
    