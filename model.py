class Game:
    def __init__(self, id, homeTeam, awayTeam, scoreHome, scoreAway, referee, stadium, capacity, public, date, time, country, round):
        self.id = id
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.scoreHome = int(scoreHome)
        self.scoreAway = int(scoreAway)
        self.referee = referee
        self.stadium = stadium
        self.capacity = capacity.replace(' ','')
        self.public = public.replace(' ','')
        self.date = date
        self.time = time
        self.country = country
        self.round = round
        self.pointsHome, self.pointsAway = self.getPoints(int(scoreHome), int(scoreAway))
    
    def __str__(self):
        return f'Jogo {self.id}: {self.homeTeam} {self.scoreHome} x {self.scoreAway} {self.awayTeam}\n{self.stadium} - {self.public} presentes\n{self.date} | {self.time}\n{self.round}'
    
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
    