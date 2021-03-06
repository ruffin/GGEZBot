import praw
import traceback
import random
import re
import pickle
from praw.helpers import comment_stream

USERNAME = input('Username: ')
PASSWORD = input('Password: ')
USERAGENT = "GG EZ v1.1.1 (by /u/ChaosTheDude)"

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

FOOTER = "\n\n---\n^I ^am ^a ^bot ^made ^by ^/u/ChaosTheDude. ^Beep ^boop. ^| ^[GitHub](https://github.com/ChaosTheDude/GG-EZ-Bot)"

RESPONSES = ['Ah shucks... you guys are the best!',
             'C\'mon, Mom! One more game before you tuck me in. Oops mistell.',
             'For glory and honor! Huzzah comrades!',
             'Gee whiz! That was fun. Good playing!',
             'Good game! Best of luck to you all!',
             'Great game, everyone!',
             'I feel very, very small... please hold me...',
             'It was an honor to play with you all. Thank you.',
             'It\'s past my bedtime. Please don\'t tell my mommy.',
             'I\'m trying to be a nicer person. It\'s hard, but I am trying, guys.',
             'I\'m wrestling with some insecurity issues in my life but thank you all for playing with me.',
             'Mommy says people my age shouldn\'t suck their thumbs.',
             'Well played. I salute you all.']

processed = set()

save_file = "save.p"

try:
    with open(save_file, 'rb') as handle:
        processed = pickle.load(handle)
except EOFError:
    print("Empty save file.")


def process_comment(c):
    text = c.body.lower()
    if re.search(r'\b(gg\s*ez)\b', text):
        print(c.body)
        response = random.choice(RESPONSES)
        print("\n" + response + "\n---\n")
        c.reply(response + FOOTER)


def dump_ids():
    with open(save_file, 'wb') as handle:
        pickle.dump(processed, handle)


while True:
    try:
        for comment in comment_stream(r, 'overwatch'):
            if comment.id not in processed:
                processed.add(comment.id)
                process_comment(comment)
                dump_ids()
    except:
        traceback.print_exc()
