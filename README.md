# Scripts for /r/cfb

This a simple script that helps process data from reddit threads and might highlight interesting data.

---

## Installation

`pip install -r requirements.txt`

You'll also need to create a reddit app [here](https://ssl.reddit.com/prefs/apps) to connect to the API. Add your `client_id` and `client_secret` in `constants.py`

If you want to create heatmaps, you'll need to install [Jupyter](http://jupyter.org/). The heatmap creation needs some map and widget data.

---

## Usage

This app lets you:

### Find comments that match a flair tag (/r/cfb)

`./scraper.py --submission_id '5n37kq' --comments_limit 1000 --filter_by flair --filter_text 'Alabama Crimson Tide'`

### Break down comments for a submission by flair
`./scraper.py --submission_id '5n37kq' --show_comments_by_flair --comments_limit 1000`

### Create wordlclouds for comments
`./scraper.py --submission_id '5n37kq' --comments_limit 1000 --filter_by flair --filter_text --create_wordcloud`

### Do keyword searching through a submission's comments
`./scraper.py --submission_id '5n37kq' --comments_limit 1000 --keyword_search 'kiffin'`

### Create interesting combinations of the above:
*Wordcloud for comments by Clemson fans*:

`./scraper.py --submission_id '5n37kq' --comments_limit 1000 --filter_by flair --filter_text 'Clemson Tigers' --create_wordcloud --wordcloud_name Clemson_wordcloud`

*Search for Crimson Tide folks saying congratulations*:

`./scraper.py --submission_id '5n37kq' --comments_limit 1000 --filter_by flair --filter_text 'Alabama Crimson Tide' --keyword_search 'Congratulations'`

### You can also create a heatmap by commentor flair

Open up a `jupyter` notebook:

```
jupyter notebook
```

Then you can either create your own setup, or open the provided `CFB Comment Heatmap.ipynb` to generate the heatmap.
