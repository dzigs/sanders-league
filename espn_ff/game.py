from espn_ff.constants import GAME_TYPE_MAP


class Game(object):
    def __init__(self, game, season):
        self.season_id = season
        self.game_id = game['id']
        self.week = game['matchupPeriodId']  # probably need to change for multiweeks in the future
        self.playoff_type = game['playoffTierType'] if 'away' in game else 'BYE_WEEK'
        self.winner = game['winner']
        self.away_team_id = game['away']['teamId'] if 'away' in game else None
        self.away_points = game['away']['totalPoints'] if 'away' in game else None
        self.home_team_id = game['home']['teamId']
        self.home_points = game['home']['totalPoints']
        self.game_type = GAME_TYPE_MAP[self.playoff_type]

    # TODO: This is all very hacky
    def override_ladder_games(self, num_games):
        if self.week == 16 and self.season_id > 2012 and self.game_id == (num_games - 2):
            self.game_type = 'junk'
        elif self.season_id in (2010, 2011) and \
                (self.week < 15 or (self.week == 16 and (self.game_id == (num_games - 1)))):
            self.game_type = 'junk'
        elif self.season_id == 2009 and self.week < 17:
            self.game_type = 'junk'
        elif self.season_id == 2012 and self.game_id in (num_games - 1, num_games - 2, num_games - 7):
            self.game_type = 'junk'

        self.game_type = 'ladder'
