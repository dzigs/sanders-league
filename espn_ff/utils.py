import requests
import configparser
from pathlib import Path

from espn_ff.constants import  REQUEST_HISTORY_DIR


def league_history_json(year):
    try:
        with open(project_root() + REQUEST_HISTORY_DIR + 'league_history_sched_%s.json' % year, mode='r') as json_file:
            contents = json_file.read()
    except:
        config = configparser.RawConfigParser()
        config.read(project_root() + '/localconfig.conf')
        r = requests.get(
            'https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/733954?view=mMatchupScore&view=mRoster&view=mScoreboard&view=mSettings&view=mTopPerformers&view=mTeam&view=modular&view=mNav',
            params={'seasonId': year}, cookies={'swid': config['ESPN_COOKIES']['SWID'], 'espn_s2': config['ESPN_COOKIES']['ESPN_S2']})
        with open(project_root() + REQUEST_HISTORY_DIR + 'league_history_sched_%s.json' % year, mode='w') as json_file:
            json_file.write(r.text)
            contents = r.text
    return contents


def project_root():
    return str(Path(__file__).parent.parent)
