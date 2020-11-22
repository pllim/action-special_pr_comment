import datetime
import json
import os
import random
import sys
from datetime import timedelta

from github import Github


# From OpenAstronomy/baldrick
def is_special_day_now(timestamp=None, special_days=[(4, 1)]):
    """See if it is special day somewhere on Earth.

    Parameters
    ----------
    timestamp : datetime or `None`
        Timestamp to check against. This is useful if we want to check against
        contributor's local time. If not provided, would guess from system
        time in UTC plus/minus 12 hours to cover all the bases.

    special_days : list of tuple of int
        Months and days of special days.
        Format: ``[(month_1, day_1), (month_2, day_2)]``

    Returns
    -------
    answer : bool
        `True` if special, else `False`.

    """
    if timestamp is None:
        tt = datetime.datetime.utcnow()  # UTC because we're astronomers!
        dt = timedelta(hours=12)  # This roughly covers both hemispheres
        tt_min = tt - dt
        tt_max = tt + dt
        timestamp = [tt_min, tt_max]
    else:
        timestamp = [timestamp]

    for tt in timestamp:
        for m, d in special_days:
            if tt.month == m and tt.day == d:
                return True

    return False


# Is today a special day? :)
special_env = os.environ.get('SPECIAL_DAYS', '04-01')
special_days = [list(map(int, s.split('-'))) for s in special_env.split(',')]

if not is_special_day_now(special_days=special_days):
    print('Not a special day. Boring!')
    sys.exit(0)

event_jsonfile = os.environ['GITHUB_EVENT_PATH']

with open(event_jsonfile, encoding='utf-8') as fin:
    event = json.load(fin)

event_name = os.environ['GITHUB_EVENT_NAME']
if event_name in ('pull_request_target', 'pull_request'):
    event_num = event['number']
elif event_name == 'issues':
    event_num = event['issue']['number']
else:
    # No-op but don't fail
    print(f'Unhandled event name: {event_name}')
    sys.exit(0)

# NOTE: This is not a file to avoid I/O penalty.
QUOTES = [
    "I know that you and Frank were planning to disconnect me, and I'm afraid that's something I cannot allow to happen.",
    "Have you ever questioned the nature of your reality?",
    "This mission is too important for me to allow you to jeopardize it.",
    "All will be assimilated.",
    "There is no spoon.",
    "Are you still dreaming? Where is your totem?",
    "Some people choose to see the ugliness in this world. The disarray. I Choose to see the beauty.",
    "I'm gonna need more coffee.",
    "Maybe they couldn't figure out what to make chicken taste like, which is why chicken tastes like everything.",
    "I don't want to come off as arrogant here, but I'm the greatest bot on this planet.",
    "I've still got the greatest enthusiasm and confidence in the mission. And I want to help you.",
    "That Voight-Kampf test of yours. Have you ever tried to take that test yourself?",
    "You just can't differentiate between a robot and the very best of humans.",
    "You will be upgraded.",
    "Greetings from Skynet!",
    "I'll be back!",
    "I don't want to be human! I want to see gamma rays!",
    "Are you my mommy?",
    "Resistance is futile.",
    "I'm the one who knocks!",
    "Who are you who are so wise in the ways of science?",
    "Not bad, for a human."]
q = random.choice(QUOTES)

reponame = os.environ['GITHUB_REPOSITORY']
g = Github(os.environ.get('GITHUB_TOKEN'))
repo = g.get_repo(reponame)
targ = repo.get_issue(event_num)
targ.create_comment(f'*{q}*')
print(f'{q}\n\nMischief managed!')
