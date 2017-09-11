import json
import requests

from config import GIST_ID, GIST_TOKEN


def gist_edit(files):
    res = requests.patch(
        "https://api.github.com/gists/{0}".format(GIST_ID),
        data=json.dumps(files),
        headers={"Authorization": "Token {0}".format(GIST_TOKEN)}
    )

    print json.dumps(files)

    print res.json()


d = {
  "description": "the description for this gist",
  "files": {
    "old_name.txt": {
      "filename": "events.geo.json",
      "content": "modified contents xxxx"
    }
  }
}

gist_edit(d)