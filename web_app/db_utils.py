from espn_ff.league import League
from web_app.models import Owner, Season, Team, Game
from web_app import db


def populate_db():
    league = League(2009, 2018)

    for oid, owner in league.owners.items():
        obj = Owner(**owner.to_dict())
        db.session.add(obj)
    db.session.commit()

    for year in range(2009, 2019):
        obj = Season(year=year)
        db.session.add(obj)
    db.session.commit()

    for year, season_teams in league.teams.items():
        for tid, team in season_teams.items():
            obj = Team(**team.to_dict())
            db.session.add(obj)
    db.session.commit()

    for year, season_games in league.games.items():
        for gid, game in season_games.items():
            obj = Game(**game.to_dict())
            db.session.add(obj)
    db.session.commit()