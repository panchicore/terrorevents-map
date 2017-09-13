import datetime
import json

from geojson import Point, Feature, FeatureCollection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine, Boolean, Float
from sqlalchemy.orm import sessionmaker

import mapbox_client
import nlp_client
import github_client

Base = declarative_base()
engine = create_engine('sqlite:///events.db')
Session = sessionmaker(bind=engine)
session = Session()


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, index=True)
    text = Column(Text)
    user = Column(String)
    nlp = Column(Text, nullable=True)
    geocode = Column(Text, nullable=True)
    raw_tweet = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    processed = Column(Boolean, default=False)
    error_description = Column(String, nullable=True)

    @property
    def link(self):
        return "https://twitter.com/TerrorEvents/status/{}".format(self.id)

    def exists(self):
        return session.query(Tweet).filter_by(id=self.id).first() != None

    def save(self):
        session.add(self)
        session.commit()

    def purge(self):
        session.query(Tweet).delete()
        session.commit()

    def pending_to_parse(self):
        return session.query(Tweet).filter(Tweet.processed == False)

    def process_pending_tweets(self):
        tweets = Tweet().pending_to_parse()
        for t in tweets.all():

            text = t.text.replace("#", "")
            nlp_response, locations = nlp_client.get_locations(text.encode('utf-8'))
            t.nlp = json.dumps(nlp_response)

            if not locations:
                print "skipping no locations on text:", t.text.encode('utf-8')
                t.error_description = "NLP:no-location-on-text"
                t.processed = True
                session.commit()
                continue

            locations_query = ', '.join(locations)
            geocode = mapbox_client.geocode(locations_query.encode('utf-8'))
            t.geocode = json.dumps(geocode)

            if not geocode:
                print "skipping no geocode resolved", locations_query
                t.error_description = "GEO:no-geocode-response"
                t.processed = True
                session.commit()
                continue

            features = geocode.get("features")

            if not features:
                print "skipping no geocode resolved", locations_query
                t.error_description = "GEO:no-feature"
                t.processed = True
                session.commit()
                continue
            else:
                center = features[0].get("center")
                t.longitude = center[0]
                t.latitude = center[1]

            t.processed = True
            session.commit()

    @property
    def to_geojson(self):
        point = Point((self.longitude, self.latitude))
        properties = {
            "text": self.text,
            "date": str(self.date),
            "user": self.user,
            "link": self.link,
        }
        feature = Feature(geometry=point, properties=properties)
        return feature


    def get_feature_collection(self, tweets):
        features = []
        for t in tweets:
            features.append(t.to_geojson)
        return FeatureCollection(features)


    def get_geojson_since_days(self, days=1):
        today = datetime.datetime.today() - datetime.timedelta(days=days)
        tweets = session.query(Tweet).filter(Tweet.date >= today.isoformat(), Tweet.error_description == None).all()
        return Tweet().get_feature_collection(tweets)


Base.metadata.create_all(engine)

