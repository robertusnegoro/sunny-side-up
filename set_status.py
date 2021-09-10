import argparse
import logging
import os
from slack_bolt import App

log_path = os.getenv('SUNNY_LOG') or '/var/log/sunny.log'
logging.basicConfig(filename=log_path, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)
app = App()

def change_profile(status_text, status_emoji):
    if len(status_text) <= 100:
        status_emoji_transform = ":%s:" % (status_emoji)
        try:
            app.client.users_profile_set(
                profile = {
                    "status_text": status_text,
                    "status_emoji": status_emoji_transform
                }
            )
            logger.info('updated with text %s, emoji %s' % (status_text, status_emoji))
            return True
        except Exception as e:
            logger.error(e)
            return False
    else:
        logger.error('status text should less than 100 char')
        return False

def change_dnd(duration):
    try:
        app.client.dnd_setSnooze(
            num_minutes = duration
        )
        logger.info('updated dnd %s' % (str(duration)))
        return True
    except Exception as e:
        logger.error(e)
        return False

def toggle_away(away):
    try:
        if away:
            away_status = 'away'
        else:
            away_status = 'auto'
            
        app.client.users_setPresence(presence = away_status)
        logger.info('updated set to %s' % (away_status))
        return True
    except Exception as e:
        logger.error(e)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--emoji", help="status emoji", default="hammer_and_wrench")
    parser.add_argument("-s", "--status", help="status text", default="")
    parser.add_argument("-d", "--dnd", help="duration DnD", type=int, default=0)
    parser.add_argument('-a', dest='away', help='away or active', action='store_true')
    args = parser.parse_args()
    arg_status_text = str(args.status)
    arg_status_emoji = str(args.emoji)
    arg_dnd = args.dnd
    arg_away = args.away

    change_profile(arg_status_text, arg_status_emoji)
    toggle_away(arg_away)
    if arg_dnd > 0:
        change_dnd(arg_dnd)