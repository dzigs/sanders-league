
class Team(object):
    def __init__(self, team, season):
        self.season_id = season
        self.team_id = team['id']
        self.abbrev = team['abbrev']
        self.owner_id = team['primaryOwner']
        self.location = team['location']
        self.nickname = team['nickname']
        self.playoff_seed = team['playoffSeed']
        self.season_finish = team['rankCalculatedFinal']

        # list of game_ids
        self.schedule = []

        # aggregated stats broken down by game category, probably want to make this less hard-codey
        self.wins = {
            'regular_season': 0,
            'playoffs': 0,
            'ladder': 0,
            'junk': 0,
        }
        self.losses = {
            'regular_season': 0,
            'playoffs': 0,
            'ladder': 0,
            'junk': 0,
        }
        self.points_for = {
            'regular_season': 0.,
            'playoffs': 0.,
            'ladder': 0.,
            'junk': 0.,
            'bye': 0.,
        }
        self.points_against = {
            'regular_season': 0.,
            'playoffs': 0.,
            'ladder': 0.,
            'junk': 0.,
        }

    def update_team_with_game(self, game, home=True):
        if game.game_type == 'bye':
            self.points_for[game.game_type] += game.home_points
        else:
            self.points_for[game.game_type] += game.home_points if home else game.away_points
            self.points_against[game.game_type] += game.away_points if home else game.home_points
            if (home and game.winner == 'HOME') or (not home and game.winner == 'AWAY'):
                self.wins[game.game_type] += 1
            else:
                self.losses[game.game_type] += 1

        self.schedule.append(game.game_id)
