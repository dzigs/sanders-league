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

    def owner_head_to_head(self, owner_id1, owner_id2, game_types=['regular_season', 'playoffs']):
        owner1 = self.owners[owner_id1]
        owner2 = self.owners[owner_id2]

        games_list = []
        for year, team_id in owner1.teams.items():
            schedule_list = self.teams[year][team_id].schedule
            games_list += [(year, gid) for gid in schedule_list]

        games_list2 = []
        for year, team_id in owner2.teams.items():
            schedule_list = self.teams[year][team_id].schedule
            games_list2 += [(year, gid) for gid in schedule_list]

        set1 = set(games_list)
        set2 = set(games_list2)

        h2h_games = sorted(list(set1.intersection(set2)))

        owner1_wins, owner2_wins = 0, 0
        d = {
            'game_type': [],
            'year': [],
            'week': [],
            'winning owner': [],
            'winning points': [],
            'losing owner': [],
            'losing points': [],
        }
        for year, gid in h2h_games:
            game = self.games[year][gid]
            d['game_type'].append(game.game_type)
            d['year'].append(year)
            d['week'].append(game.week)
            winning_id = game.home_team_id if game.winner == 'HOME' else game.away_team_id
            d['winning points'].append(game.home_points if game.winner == 'HOME' else game.away_points)
            d['losing points'].append(game.away_points if game.winner == 'HOME' else game.home_points)

            if winning_id == owner1.teams[year]:
                d['winning owner'].append('%s %s' % (owner1.first_name, owner1.last_name))
                d['losing owner'].append('%s %s' % (owner2.first_name, owner2.last_name))
                if game.game_type in game_types:
                    owner1_wins += 1
            else:
                d['losing owner'].append('%s %s' % (owner1.first_name, owner1.last_name))
                d['winning owner'].append('%s %s' % (owner2.first_name, owner2.last_name))
                if game.game_type in game_types:
                    owner2_wins += 1

        print('%s %s: %i' % (owner1.first_name, owner1.last_name, owner1_wins))
        print('%s %s: %i' % (owner2.first_name, owner2.last_name, owner2_wins))

        df = pandas.DataFrame(data=d)
        return df


    def view_owner_names_and_id(self):
        for owner_id, owner in self.owners.items():
            print('%s | %s %s' % (owner_id, owner.first_name, owner.last_name))


def main():
    league = League(2009, 2018)
    df = league.owner_records()

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

    df2 = league.owner_head_to_head('{011D1B5B-E50A-47ED-805E-77BE3D70F756}', '{308ACAC2-AEAD-46F1-8B62-6473A6D14F5D}')

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df2)


if __name__ == "__main__":
    main()
