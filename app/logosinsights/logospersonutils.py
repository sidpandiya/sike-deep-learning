import os, pyrebase
from watson_developer_cloud import PersonalityInsightsV3
LATEST_VERSION = '2017-10-13'
from app.logosinsights.wpcreds import creds as default_credentials
from app.logosinsights.fbcreds import jack_service_creds as firebase_credentials

def get_firebase():
    return pyrebase.initialize_app(firebase_credentials)

def get_personality_insights(creds=default_credentials):
    personality_insights = PersonalityInsightsV3(
        version=LATEST_VERSION,
        username=creds['username'],
        password=creds['password'],
        url=creds['url']
        )
    return personality_insights


"""
    def profile(self,
                content,
                content_type='application/json',
                content_language=None,
                accept='application/json',
                accept_language=None,
                raw_scores=None,
                csv_headers=None,
                consumption_preferences=None,
                **kwargs):
"""

def get_profile(info,
                user_id,
                content_type="application/json",
                content_language="en",
                accept_language="en"):

    pi = get_personality_insights()
    profile = pi.profile(content=info,
               content_type=content_type,
               content_language="en",
               accept_language="en")

