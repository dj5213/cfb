#!/usr/bin/env python
import argparse
import os
import sys

from collections import Counter
from lib import authorized_reddit_instance, generate_wc, generate_heatmap
from os import path

from constants import EMPTY_LIST_VALUES

os.path.join(os.path.dirname(__file__))


class RedditScraper(object):
    def __init__(self, submission_id='5n37kq', use_login=False):
        self.reddit = authorized_reddit_instance(use_login)
        self.submission_id = submission_id

    def get_comments_for_submission(self, limit=None, more_comments_limit=32):
        # Only showing top level comments right now
        submission = self.reddit.submission(id=self.submission_id)

        submission.comments.replace_more(limit=more_comments_limit, threshold=2)
        comments = submission.comments.list()

        return comments[:limit]

    def generate_comment_wordcloud(self, comments_list=[], file_name='wordcloud'):
        wc_text = ' '.join([comment.body for comment in comments_list])
        wc = generate_wc(wc_text)
        wc.to_file(path.join(
            path.dirname(__file__),
            "{}.png".format(file_name)))

    def filter_comments(self, comments_list, filter_by, comment_filter):
        filtered_list = []
        for comment in comments_list:
            if filter_by == 'flair' and comment.author_flair_text == comment_filter:
                filtered_list.append(comment)
        return filtered_list

    def keyword_search(self, comments_list, keyword):
        results_list = []
        for comment in comments_list:
            if keyword.lower() in comment.body.lower():
                results_list.append(comment)
        return results_list

    def comment_by_flair(self, comments_list):
        count = Counter()
        for flair in self._breakup_flair_pairs(comments_list):
            count[flair.strip()] += 1
        return count

    def create_heatmap_from_submission(self):
        """
        This outputs a heatmap generated from the flairs for each comment in
        a submission. Right now it only works using a Jupyter notebook.

        TODO: add CLI integration to open Jupyter with heatmap generator running
        """
        # Adding in more_comments limit of 50 to increase datapoints
        comments_list = self.get_comments_for_submission(more_comments_limit=50)
        flair_list = self._breakup_flair_pairs(comments_list)

        return generate_heatmap(flair_list)

    def _breakup_flair_pairs(self, comments_list):
        flair_list = [comment.author_flair_text for comment in comments_list
                      if comment.author_flair_text is not None]

        flattened_flair_list = []
        for flair in flair_list:
            flattened_flair_list.extend(flair.split('/'))
        flattened_flair_list = [
            flair.strip() for flair in flattened_flair_list if flair not in EMPTY_LIST_VALUES]
        return flattened_flair_list


def setup_args():
    parser = argparse.ArgumentParser(description='CLI controls for CFB scraper')

    # Required: submission ID
    parser.add_argument(
        '--submission_id',
        metavar='id',
        type=str,
        help='Submission id for thread of interest',
        required=True)

    parser.add_argument(
        '--show_all_comments',
        action='store_true',
        help='Show all returned comments then exit')
    parser.add_argument(
        '--show_comments_by_flair',
        action='store_true',
        help='Show breakdown of comments by flair then exit')
    parser.add_argument(
        '--comments_limit',
        metavar='limit',
        type=int,
        help='Limit number of comments returned',
        required=False)

    # Optional: generate a wordcloud
    parser.add_argument('--create_wordcloud', action='store_true')
    parser.add_argument(
        '--wordcloud_name',
        metavar='name',
        type=str,
        help='Give your wordcloud a name. DO NOT INCLUDE FILE EXTENSION',
        required=False)

    parser.add_argument(
        '--keyword_search',
        type=str,
        metavar='keyword',
        help='Search comments in submission for keyword',
        required=False)

    # Filter_comments - right now only filter by flair
    parser.add_argument(
        '--filter_by',
        choices=["flair"],
        type=str,
        help='Filter comments by a set param',
        required=False)

    parser.add_argument(
        '--filter_text',
        type=str,
        help='Text to use for filter',
        required=False)

    parser.add_argument('--login', action='store_true')

    args = parser.parse_args()

    if (args.filter_by and args.filter_text is None or
            args.filter_text and args.filter_by is None):
        parser.error("--filter_by requires --filter_by value and --filter_text.")
    return args


def main():
    args = setup_args()

    scraper = RedditScraper(args.submission_id, True if args.login else False)
    comments_list = scraper.get_comments_for_submission(args.comments_limit)

    if args.show_all_comments:
        print [comment.body for comment in comments_list]
        sys.exit()

    if args.show_comments_by_flair:
        print "TOP 5 MOST COMMON:\n"
        print scraper.comment_by_flair(comments_list).most_common(5)
        print "\nCOMPLETE LIST:\n"
        print scraper.comment_by_flair(comments_list)
        sys.exit()

    if args.filter_by:
        comments_list = scraper.filter_comments(
            comments_list,
            args.filter_by,
            args.filter_text)

    if args.keyword_search:
        comments_list = scraper.keyword_search(comments_list, args.keyword_search)

    if args.create_wordcloud:
        scraper.generate_comment_wordcloud(comments_list, args.wordcloud_name)

    print [comment.__dict__ for comment in comments_list]


if __name__ == "__main__":
    sys.exit(main())
