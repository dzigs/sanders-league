
class Owner(object):
    def __init__(self, member):
        self.first_name = member['firstName']
        self.last_name = member['lastName']
        self.display_name = member['displayName']
        self.owner_id = member['id']
        self.league_creator = member['isLeagueCreator']

        # will be dict year: team_id
        self.teams = {}
