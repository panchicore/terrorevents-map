import json
import requests

from config import GIST_ID, GIST_TOKEN


def gist_edit(files):
    """

    :param files:
    :return:
    """
    res = requests.patch(
        "https://api.github.com/gists/{0}".format(GIST_ID),
        data=json.dumps(files),
        headers={"Authorization": "Token {0}".format(GIST_TOKEN)}
    )
    return res.json()
