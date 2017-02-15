import praw

from constants import CREDS, CUSTOM_STOPWORDS_LIST
from getpass import getpass

from wordcloud import WordCloud, STOPWORDS


def authorized_reddit_instance():
    """
    Returns authenticated Reddit instance. Username/pw are
    optional - only need those if you want to view anything
    that requires auth on Reddit.
    """
    reddit_username = raw_input("Enter your username:\n")
    # I don't like plain-texting passwords -
    # wil request every time script runs
    reddit_pw = getpass("Enter your password:\n")

    reddit = praw.Reddit(
        client_id=CREDS.get('client_id'),
        client_secret=CREDS.get('client_secret'),
        password=reddit_pw,
        user_agent='testscript by /u/{}'.format(reddit_username),
        username=reddit_username)
    reddit_pw = None

    return reddit


def generate_wc(text=None, image_mask=None):
    """
    Basic wordcloud generator. If you use this for game threads,
    might want to add the teams to the stopwords list. Otherwise they'll
    be the biggest words (and make the cloud boring).

    If you find a good stencil outline set the `image_mask` to form the
    wordcloud as you please.

    I love wordclouds, because, words in clouds is cool.
    """
    stopwords = set(STOPWORDS)
    for word in CUSTOM_STOPWORDS_LIST:
        stopwords.add(word)
    wc = WordCloud(
        background_color="white",
        max_words=2000,
        mask=image_mask,
        stopwords=stopwords)

    return wc.generate(text)
