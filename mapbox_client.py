import requests

from config import MAPBOX_TOKEN


def geocode(text):
    """

    :param text:
    :return:
    """
    res = requests.get(
        "https://api.mapbox.com/geocoding/v5/mapbox.places/{0}.json?access_token={1}".format(text, MAPBOX_TOKEN)
    )

    if not res.ok:
        raise Exception("Mapbox error: {0}".format(res.content))

    return res.json()
