class Matchup:
    def __init__(self, homeTeamName, awayTeamName, homeTeamAbbr, awayTeamAbbr):
        self.homeTeamName = homeTeamName
        self.awayTeamName = awayTeamName
        self.homeTeamAbbr = homeTeamAbbr
        self.awayTeamAbbr = awayTeamAbbr
    
    homeSpread = None
    awaySpread = None
    homeSpreadPercentOfMoney = None
    awaySpreadPercentOfMoney = None
    homeSpreadPercentOfBets = None
    awaySpreadPercentOfBets = None
    overTotal = None
    underTotal = None
    overTotalPercentOfMoney = None
    underTotalPercentOfMoney = None
    overTotalPercentOfBets = None
    underTotalPercentOfBets = None
    homeML = None
    awayML = None
    homeMLPercentOfMoney = None
    awayMLPercentOfMoney = None
    homeMLPercentOfBets = None
    awayMLPercentOfBets = None
    date = None
    time = None
    league = None