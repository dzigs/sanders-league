
class Owner(object):
    def __init__(self, member, active=True):
        self.first_name = member['firstName']
        self.last_name = member['lastName']
        self.display_name = member['displayName']
        self.owner_id = member['id']
        self.league_creator = member['isLeagueCreator']
        self.active = active

        # will be dict year: team_id
        self.teams = {}

    def to_dict(self):
        return {
            'id': self.owner_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'display_name': self.display_name,
            'league_creator': self.league_creator,
            'active': self.active
        }
