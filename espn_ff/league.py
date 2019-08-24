import json

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

            for member in json_dump['members']:
                if member['id'] not in self.owners:
                    self.owners[member['id']] = Owner(member)

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

    def regular_season_record_by_owner(self):
        for owner_id, owner in self.owners.items():
            ws, ls, pf, pa = 0, 0, 0., 0.
            for year, team_id in owner.teams.items():
                team = self.teams[year][team_id]
                ws += team.wins['regular_season']
                ls += team.losses['regular_season']
            print(owner.first_name + ' ' + owner.last_name + ' ' + str(ws) + ' ' + str(ls) + ' ' + str(float(ws)/(ws + ls)))


def main():
    l = League(2009, 2018)
    l.regular_season_record_by_owner()


if __name__ == "__main__":
    main()
