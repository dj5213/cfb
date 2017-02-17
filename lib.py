import csv
import gmaps
import json
import praw
import sys
import time
import urllib2

from constants import (
    CREDS,
    CUSTOM_STOPWORDS_LIST,
    INSTITUTION_COORDINATES_FILENAME,
    GOOGLE_MAPS_API_KEY,
    GEOCODE_API_URL
)

from getpass import getpass

from wordcloud import WordCloud, STOPWORDS


def authorized_reddit_instance(use_login=False, reddit_username='', reddit_pw=''):
    """
    Returns authenticated Reddit instance. Username/pw are
    optional - only need those if you want to view anything
    that requires auth on Reddit.
    """
    if not CREDS.get('client_id') or not CREDS.get('client_secret'):
        print "No client_id or client_secret found - please enter in constants.py to continue"
        print "EXITING"
        sys.exit()

    if use_login:
        reddit_username = raw_input("Enter your username:\n")
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


def generate_long_lat_csv(filename='School_coordinates.csv'):
    """
    This is a one-off function that generates a list of institutions and attempts
    to find their relative long/lat coordinates. Sometimes it's spot on, other times
    it just finds a random location - some spot checking required.

    To run this, you'll need to create a Google Maps API key and put it in constants.py
    """

    # Importing inline because this approach is pretty hacky. It pulls in a very active
    # comment thread and looks up all the flairs in that submission to find coordinates.
    # TODO: Lookup all official flairs to create official CSV for schools and coordinates.
    from scraper import RedditScraper
    scraper = RedditScraper(submission_id='5n37kq')
    comment_breakdown = scraper.comment_by_flair(scraper.get_comments_for_submission())
    with open(filename, 'wb') as csvfile:
        file_writer = csv.writer(csvfile, delimiter=',')
        file_writer.writerow(['School name', 'Longitude', 'Lattitude'])
        for schoolname in comment_breakdown.keys():
            try:
                print "Looking up {}".format(schoolname)
                response = urllib2.urlopen(GEOCODE_API_URL.format(
                    key=GOOGLE_MAPS_API_KEY,
                    query=urllib2.quote(schoolname)))
                response = json.loads(response.read())
                result = response['results'].pop()
                longitude = result['geometry']['location']['lng']
                lattitude = result['geometry']['location']['lat']

                print "WRITING: "
                print [schoolname, longitude, lattitude]
                file_writer.writerow([schoolname, longitude, lattitude])
                time.sleep(1)
            except Exception as e:
                print schoolname, e


def load_instituation_coords(filename=INSTITUTION_COORDINATES_FILENAME):
    """
    Takes in a filename and returns a dict where key is school and
    value is tuple of geographic coordinates.

    Example: {'Texas Longhorns': (30.2878965, -97.7482072)}
    """
    locations_map = {}
    with open(filename, 'rU') as csv_file:
        file_reader = csv.reader(csv_file, delimiter=',', quotechar='|', dialect=csv.excel_tab)
        for row in file_reader:
            if row[0] == "School name":
                continue
            locations_map[row[0]] = (float(row[2]), float(row[1]))

    return locations_map


def generate_heatmap(flair_list):
    comments_coords_list = []
    mapping_dict = load_instituation_coords()

    for institution in flair_list:
        if mapping_dict.get(institution):
            comments_coords_list.append(mapping_dict[institution])

    gmaps.configure(api_key=GOOGLE_MAPS_API_KEY)
    m = gmaps.Map()
    heatmap_layer = gmaps.Heatmap(data=comments_coords_list)
    heatmap_layer.max_intensity = 80
    heatmap_layer.point_radius = 40
    m.add_layer(heatmap_layer)

    return m
