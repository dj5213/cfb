# Scripts for /r/cfb

This a simple script that helps process data from reddit threads and might highlight interesting data.

---

## Installation

`pip install -r requirements.txt`

You'll also need to create a reddit app [here](https://ssl.reddit.com/prefs/apps) to connect to the API.

---

## Usage

This app lets you:

### Find comments that match a flair tag (/r/cfb)

`./scraper.py --submission_id '5n37kq' --comments_limit 1000 --filter_by flair --filter_text 'Alabama Crimson Tide'`

### Break down for a submission by flair
`./scraper.py --submission_id '5n37kq' --show_comments_by_flair --comments_limit 1000`

### Create wordlclouds for comments
`./scraper.py --submission_id '5n37kq' --comments_limit 1000 --filter_by flair --filter_text --create_wordcloud`

### Do keyword searching through a submission's comments
`./scraper.py --submission_id '5n37kq' --comments_limit 1000 --keyword_search 'kiffin'`

