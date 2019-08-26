from web_app import db


class Owner(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    display_name = db.Column(db.String(32))
    league_creator = db.Column(db.Boolean)
    active = db.Column(db.Boolean)

    teams = db.relationship('Team', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f'<Owner {self.display_name}>'


class Season(db.Model):
    year = db.Column(db.Integer, primary_key=True)

    teams = db.relationship('Team', backref='season', lazy='dynamic')
    games = db.relationship('Game', backref='season', lazy='dynamic')

    def __repr__(self):
        return f'<Season {self.year}>'


class Team(db.Model):
    year = db.Column(db.Integer, db.ForeignKey('season.year'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String(64), db.ForeignKey('owner.id'))
    abbrev = db.Column(db.String(4))
    location = db.Column(db.String(16))
    nickname = db.Column(db.String(16))
    playoff_seed = db.Column(db.Integer)
    season_rank = db.Column(db.Integer)

    def __repr__(self):
        return f'<Team {self.nickname}>'


class Game(db.Model):
    year = db.Column(db.Integer, db.ForeignKey('season.year'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_points = db.Column(db.Float)
    home_points = db.Column(db.Float)
    game_type = db.Column(db.String(32))
    week = db.Column(db.Integer)
    winner = db.Column(db.String(16))

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['year', 'away_team_id'],
            ['team.year', 'team.id']
        ),
        db.ForeignKeyConstraint(
            ['year', 'home_team_id'],
            ['team.year', 'team.id']
        )
    )

    away_team = db.relationship('Team', foreign_keys=[year, away_team_id], backref="away_games", viewonly=True)
    home_team = db.relationship('Team', foreign_keys=[year, home_team_id], backref="home_games", viewonly=True)

    def __repr__(self):
        return f'<Game {self.year}, {self.id}>'
