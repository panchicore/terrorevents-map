import json

import datetime

import github_client
import twitter_client
from models import Tweet

print datetime.datetime.today()
# download tweets and save to sqllite
twitter_client.save_tweets()

# process with NLP to extract geo named entities
# process with mapbox to geocode named entities
Tweet().process_pending_tweets()

# get the geojson to be sent to gist
geojson_days = Tweet().get_geojson_since_days(days=7)
geojson_today = Tweet().get_geojson_since_days(days=1)

gist = {
  "description": "TerrorEvents tweet map. Latest update {0} [UTC+01:00], Fork it on https://github.com/panchicore/terrorevents-map".format(
    datetime.datetime.today().isoformat()
  ),
  "files": {
    "today.geojson": {
      "filename": "today.geojson",
      "content": json.dumps(geojson_today)
    },
    "7days.geojson": {
      "filename": "7days.geojson",
      "content": json.dumps(geojson_days)
    },

  }
}

# send to gist
res = github_client.gist_edit(gist)

# see results here: https://gist.github.com/panchicore/6b000c24a41fc8533b16e0553667ca61
