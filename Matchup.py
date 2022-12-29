class Matchup:
    def __init__(self, homeTeamName, awayTeamName):
        self.homeTeamName = homeTeamName
        self.awayTeamName = awayTeamName
    
    homeSpread = None
    awaySpread = None
    homeSpreadPercentOfMoney = None
    awaySpreadPercentOfMoney = None
    homeSpreadPercentOfBets = None
    awaySpreadPercentOfBets = None
    overTotal = None
    underTotal = None
    overPercentOfMoney = None
    underPercentOfMoney = None
    overPercentOfBets = None
    underPercentOfBets = None
    homeML = None
    awayML = None
    homeMLPercentOfMoney = None
    awayMLPercentOfMoney = None
    homeMLPercentOfBets = None
    awayMLPercentOfBets = None
    date = None
    time = None
    league = None