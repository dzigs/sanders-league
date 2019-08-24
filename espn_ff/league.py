import json
import pandas

from espn_ff.owner import Owner
from espn_ff.team import Team
from espn_ff.game import Game
from espn_ff.utils import league_history_json


class League(object):
    def __init__(self, first_year, last_year):
        self.owners = {}
        self.teams = {}
        self.games = {}

        for year in range(last_year, first_year - 1, -1):
            json_file = league_history_json(year)
            json_dump = json.loads(json_file)[0]

            active = (year == last_year)
            for member in json_dump['members']:
                if member['id'] not in self.owners:
                    self.owners[member['id']] = Owner(member, active)

            self.teams[year] = {}
            self.games[year] = {}
            for team in json_dump['teams']:
                new_team = Team(team, year)
                self.owners[new_team.owner_id].teams[year] = new_team.team_id
                self.teams[year][new_team.team_id] = new_team

            num_games = len(json_dump['schedule'])
            for game in json_dump['schedule']:
                new_game = Game(game, year)

                if new_game.game_type == 'ladder':
                    new_game.override_ladder_games(num_games)

                if not new_game.game_type == 'bye':
                    self.teams[year][new_game.away_team_id].update_team_with_game(new_game, home=False)
                self.teams[year][new_game.home_team_id].update_team_with_game(new_game, home=True)

                self.games[year][new_game.game_id] = new_game

    def owner_records(self, only_active=True, year_range=(), game_types=['regular_season', 'playoffs']):
        # target structure - should make constant?
        d = {
            'name': [],
            'games played': [],
            'wins': [],
            'losses': [],
            'winning percentage': [],
            'points per game': [],
            'points against per game': []
        }
        for owner_id, owner in self.owners.items():
            if only_active and not owner.active:
                continue

            name = '%s %s' % (owner.first_name, owner.last_name)
            ws, ls, pf, pa = 0, 0, 0., 0.
            for year, team_id in owner.teams.items():
                if year_range and year not in range(*year_range):
                    continue

                team = self.teams[year][team_id]
                for typ in game_types:
                    ws += team.wins[typ]
                    ls += team.losses[typ]
                    pf += team.points_for[typ]
                    pa += team.points_against[typ]

            games_played = ws + ls
            if games_played == 0:
                continue

            d['name'].append(name)
            d['games played'].append(games_played)
            d['wins'].append(ws)
            d['losses'].append(ls)
            d['points per game'].append(pf / games_played)
            d['points against per game'].append(pa / games_played)
            d['winning percentage'].append(float(ws) / games_played)

        df = pandas.DataFrame(data=d)
        return df


def main():
    l = League(2009, 2018)
    df = l.owner_records()

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


if __name__ == "__main__":
    main()
