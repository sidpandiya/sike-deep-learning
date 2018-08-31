import json, math, requests
from re import findall

import numpy as np

#from app.config import  THREAD_SENTIMENT_ROUTE, FB_CREDENTIAL_PATH, FB_POINTS_PATH, FB_ENDORSEMENTS_PATH, IDEAL_SCORE, IDEAL_MAGNITUDE, STD_DEV, MEAN
from app.logosinsights.logospersonutils import get_firebase

db = get_firebase()
db = db.database()

ML_URL = 'https://ml-dot-logos-app-915d7.appspot.com'

TEST_DIRECTORY = "test_firebase"
TEST_PROFILE_DIR = "test_profile"
TEST_ARTICLE_DIR = "test_article_info"

import json, os

ML_HOST = "https://ml-dot-logos-app-915d7.appspot.com"
THREAD_SENTIMENT_ROUTE = "thread-sentiment"
PROJECT_NAME = "logos-app-915d7"
SERVICE_JSON = "jack-comment-test-a6a33616760c.json"

ANDRES_CONFIG = {
  "apiKey": "AIzaSyBHo5Psm3_aPk2Nqu5Sg5A2rM7N-V_XAWQ",
  "authDomain": "andres-test-2fc0d.firebaseapp.com",
  "databaseURL": "https://andres-test-2fc0d.firebaseio.com/",
  "storageBucket": "andres-test-2fc0d.appspot.com",
}

ANDRES_LOGIN = {
  'username': 'a_guzman@berkeley.edu',
  'password': 'password'
}

TEMP_PROJECT_NAME = "jack-comment-test"



JACK_LOGIN = {
    "username": "jchaunceya@gmail.com",
    "password": "xxx"
}

FB_CREDENTIAL_PATH = "usercreadentials"
FB_POINTS_PATH = "userpoints"
FB_COMMENT_PATH = "postcomments"
FB_ENDORSEMENTS_PATH = "userknowsabout"
STD_DEV = 1
MEAN = 0
IDEAL_SCORE = 0
IDEAL_MAGNITUDE = 0.2

ML_URL = 'https://ml-dot-logos-app-915d7.appspot.com'


# TODO: IMPORT SIMILARITY FUNCTION
def similarity(topic_user, topic_article):
    if topic_user == "DEFAULT":
        return 0.25
    if topic_user == topic_article:
        return 1
    # TODO: ACTUALLY IMPLEMENT IT LOL
    return 0.8

class User:

    def __init__(self, userId):
        self.userId = userId
        self.get_degrees()

    def get_degrees(self):
        self.degrees = []
        # Attempt to retrieve degree information. Will fail with IndexError if not in DB
        try:
            deg_object = db.child(FB_CREDENTIAL_PATH).order_by_child("userId").equal_to(self.userId).get().val()
            for key, degree_object in deg_object.items():
                if "degree" in degree_object and "topic" in degree_object:
                    self.degrees.append((degree_object["degree"], degree_object["topic"]))

                else:
                    print("pass")

        except IndexError:
            self.degrees.append((0.5, "DEFAULT"))

    def get_TP(self):
        points = 0
        try:
            points_obj = db.child(FB_POINTS_PATH).order_by_child("userId").equal_to(self.userId).get().val()
            points = np.sum([v["points"] for k, v in points_obj.items()])
            print(points)
        except IndexError:
            # userId not found in points - doesn't have any
            print("user not found")

        self.total_points = points
        return points

    def get_RP(self, topic = ""):
        max_mult =  max([mult * similarity(user_topic, topic) for mult, user_topic in self.degrees])
        endorse_points = 1
        try:
            print(self.userId)
            endorsements = db.child(FB_ENDORSEMENTS_PATH).order_by_child("userId").get().val()
            endorsements = [i for i in endorsements.values() if i['userId'] == self.userId ]
            print(endorsements)
            for v in endorsements:
                if v["knowledge"] == topic and v["endorsementCount"] > 0:
                    endorse_points = v["endorsementCount"]
        except IndexError:
            print("No endorsements found. Setting to one...")
        print("Degree multiplier {} * endorsement points {}".format(max_mult, endorse_points))
        return max_mult * endorse_points

    def get_NP(self, topic):
        net_points = self.get_TP() + 3 * self.get_RP(topic)
        return net_points

def db_get(*args):
    val = db
    for arg in args:
        val = val.child(arg)
    val = val.get().val()
    return val

def comment_update(commentId, data):
    return db.child('postcomments').child(commentId).update(data)

def get_reply_ids(commentId):
    replies = {}
    # Returns a
    # Returns a list of reply Ids to the comment associated with commentId
    try:
        replies = db.child('commentsonpostcomments').order_by_child("commentId").equal_to(commentId).get().val()
    except IndexError:
        replies = {}

    return replies


def get_reply(replyId):
    return db.child('commentsonpostcomments').child(replyId).get().val()

def get_parent_comment_id(replyId):
    reply = get_reply(replyId)
    # If reply is not found....
    if not reply:
        raise FileNotFoundError("reply {} not found...".format(replyId))
    return reply["commentId"]

def get_comment_user(commentId):
    return db.child("postcomments").child(commentId).child("userId").get().val()

def get_unique_repliers(replier_obj, commenterId = None):

    repliers = [commenterId]

    repliers.extend([replier["userId"] for k, replier in replier_obj.items() if 'isDeleted' not in replier or not replier["isDeleted"]])

    unique_repliers = np.unique(repliers).tolist()
    return unique_repliers

def update_thread_with_comment(commentId, only_points):

    commenterId = get_comment_user(commentId)
    if not commenterId:
        print("user of comment {} not found".format(commentId))
        return None

    topic = get_topic(commentId)

    if not topic:
        topic = None

    replier_obj = get_reply_ids(commentId)
    unique_repliers = get_unique_repliers(replier_obj, commenterId)

    users = [User(userId).get_NP(topic) for userId in unique_repliers]
    if only_points:
        return np.sum(users)
    analysis = get_thread_analysis(commentId)


    score = bias_rating(analysis["sentiment"], analysis["mag_adj"])

    print("1000 * {}".format(score))
    thread_score = np.sum(users) + 1000 * score
    analysis['thread_score'] = thread_score
    comment_update(commentId, analysis)
    return thread_score

def get_topic(commentId):
    postId = db.child("postcomments").child(commentId).child("postId").get().val()
    if not postId:
        print('post of commentId {} not found'.format(commentId))
        return None

    print(db.child("posts").child(postId).child("category").get().val(), " postId")
    return db.child("posts").child(postId).child("category").get().val()

def update_thread_with_reply(replyId):
    try:
        commentId = get_parent_comment_id(replyId)
    except FileNotFoundError:
        print("commentId not found for ")
        return None
    return update_thread_with_comment(commentId)

# TODO: IMPLEMENT MORE
def create_thread(commentId):
    data = {'replyIds': get_reply_ids(commentId)}
    comment_update(commentId, data)
    data = get_thread_analysis(commentId)
    comment_update(commentId, data)


def get_replies(commentId):
    # Returns a dict of replies with key = replyId
    replyIds = get_reply_ids(commentId)
    replies = {replyId: db.child('commentsonpostcomments')
        .child(replyId).get().val() for replyId in replyIds}

    return replies

def get_comment(commentId):
    return db.child('postcomments').child(commentId).get().val()

""" Wrapper for call to ML server for sentiment analysis"""
def get_sentiment(commentId):
    return _request("GET", ML_URL, THREAD_SENTIMENT_ROUTE, data={'commentId': commentId})

def tokenize(text):
    return findall(r"[A-Za-z]+(?:\'[A-Za-z]+)?", text)

def adjust_magnitude(magnitude, num_words = 0):
    # TODO: Adjust magnitude
    return magnitude * 14 / num_words

def get_thread_analysis(commentId):
    # Calculate sentimence and magnitude of thread

    analysis = get_sentiment(commentId)

    sentiment = analysis['score']
    mag_raw = analysis['magnitude']

    mag_adj = adjust_magnitude(mag_raw, num_words=analysis["num_words"])

    data = {'sentiment': sentiment,
            'mag_raw': mag_raw,
            'mag_adj': mag_adj}

    return data

# Might want to move this function to another file that ranks threads
def get_cached_thread_analysis(commentId):
    comment = db.child("postcomments").child(commentId)
    data = {'sentiment': comment.child('sentiment').get().val(),
            'mag_raw': comment.child('mag_raw').get().val(),
            'mag_adj': comment.child('mag_adj').get().val(),
            'thread_score': comment.child('thread_score').get().val()}
    return data

def bias_rating(score, magnitude):
        euclidian_distance = math.sqrt((score - IDEAL_SCORE)**2 + (magnitude - IDEAL_MAGNITUDE)**2)
        print(euclidian_distance ** 2)
        return euclidian_distance ** 2
        return abs(2/math.sqrt(2 * math.pi * STD_DEV**2) * math.exp(-(euclidian_distance - MEAN)**2/(2 * STD_DEV**2)))


def get_comment_ids(postId):
    try:
        comments = db.child("postcomments").order_by_child("postId").equal_to(postId).get().val()
    except IndexError:
        return None
    return list(comments.keys())

def post_exists(postId):
    return db.child("posts").child(postId).get().val()
""" Generic request function
method is either 'GET' or 'POST'
"""
def _request(method, host, route, data):
    if method == "GET":
        full_path = "/".join([host, route])
        r = requests.get(full_path, data)
        print(r.text)
        return json.loads(r.text)
    else:
        pass
