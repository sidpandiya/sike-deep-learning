import pyrebase
import random
import datetime
import string
import json
from watson_developer_cloud import PersonalityInsightsV3
LATEST_VERSION = '2017-10-13'
from app.logosinsights.wpcreds import creds as default_credentials
from app.logosinsights.fbcreds import jack_service_creds as firebase_credentials
import app.config
import numpy as np

def get_firebase(db=False):
    fb = pyrebase.initialize_app(firebase_credentials)
    if db:
        return fb.database()
    return fb

class LogosInsightsGeneric:
    def __init__(self):
        pass

    def extract_big_five(self):
        if not hasattr(self, 'raw_profile'):
            self.load_profile_from_info()
        if 'personality_profile' not in self.raw_profile:
            self.simple_profile = [(trait['name'], round(trait['percentile'], 2)) for trait in self.raw_profile['personality']]
        else:
            self.simple_profile = [(trait['name'], round(trait['percentile'], 2)) for trait in self.raw_profile['personality_profile']['personality']]
        return self.simple_profile

    def load_profile_from_info(self):
        self.raw_profile = self.get_and_save_profile()

class LogosInsightsArticle(LogosInsightsGeneric):
    def __init__(self, content, title, url, already_inserted=None):
        super().__init__()
        if already_inserted:
            self.raw_profile = already_inserted
            self.content = already_inserted['content']
            self.title = already_inserted['title']
            self.url = already_inserted['url']
        else:
            self.content = content
            self.title = title
            self.url = url
        self.extract_big_five()

    def get_and_save_profile(self):
        info = {"contentItems": [{"content": self.content, "type": "text/plain"}]}
        db = get_firebase().database()

        try:
            exists = db.child(app.config.TEST_ARTICLE_DIR).order_by_child("title").equal_to(self.title).get().val()
        except IndexError:
            print("not found")
        else:
            print(exists)
            return exists[list(exists.keys())[0]]

        pi = get_personality_insights()
        profile = pi.profile(content=json.dumps(info), content_type="text/plain")
        temp_id = ''.join([random.choice(string.ascii_letters) for i in range(25)])

        data = {"content": self.content,
                "personality_profile": profile,
                "title": self.title,
                "url": self.url}

        update_child(app.config.TEST_ARTICLE_DIR, temp_id, data)

        return profile

    def set_similarity(self, sim):
        self.similarity = sim
        return self

    def todict(self):
        return_dict = {}
        return_dict['title'] = self.title
        return_dict['url'] = self.url
        return_dict['sim'] = round(self.similarity,2)
        return return_dict

class LogosInsightArticleCollection:
    def __init__(self, article_list):
        self.article_list = article_list

    def __len__(self):
        return len(self.article_list)

    def __getitem__(self, sliced):
        self.article_list = self.article_list[sliced]
        return self

    def set_similarities(self, similarities):
        self.article_list = [article.set_similarity(sim) for sim,article in zip(similarities,self.article_list)]
        return self

    def sort_articles(self):
        article_list = sorted(self.article_list, key=lambda x: x.similarity)
        for i in article_list:
            print(i.title, " ", i.similarity)


    def tolist(self):
        return self.article_list

    def __iter__(self):
        yield from self.article_list

class LogosInsightsUser(LogosInsightsGeneric):
    def __init__(self, user_id, info=None):
        super().__init__()
        self.user_id = user_id
        self.info = info
        self.extract_big_five()

    def get_and_save_profile(self):
        fb = get_firebase()
        db = fb.database()
        profile_if_exists = db.child(app.config.TEST_PROFILE_DIR).child(self.user_id).child(
            "personality_profile").get().val()
        if profile_if_exists:
            return profile_if_exists
        pi = get_personality_insights()
        profile = pi.profile(content=self.info, accept_language="en", content_language="en")
        update_child(app.config.TEST_PROFILE_DIR, self.user_id, {"personality_profile": profile})
        return profile


class LogosInsightUserFromText(LogosInsightsUser):
    def __init__(self, text, user_id):
        self.text
        pass

############################################################################################################################################
####### LOGOS USER SESSION #################################################################################################################
############################################################################################################################################

class LogosInsightsUserSession(LogosInsightsUser):
    def __init__(self, user_id):
        super().__init__(user_id)
        print(self.suggest_articles())
        # get own profile

    def compare_and_rank(self, articles):
        if len(articles) > 10:
            articles = articles[:10]

        def extract_vec(simple_profile):
            return np.array([item[1] for item in simple_profile])

        user_prof = extract_vec(self.simple_profile)[:, np.newaxis]
        user_prof = user_prof.reshape((1, user_prof.shape[0]))
        article_mx = np.array([extract_vec(article.simple_profile) for article in articles])
        temp = (article_mx - user_prof) ** 2
        temp = temp.sum(axis=1)

        articles.set_similarities(temp)

        articles.sort_articles()

        return [article.todict() for article in articles.tolist()]

    def suggest_articles(self):
        db = get_firebase().database()
        articles = db.child("test_articles_2").get().val()
        articles = LogosInsightArticleCollection([LogosInsightsArticle(content=v['content'], title=v['title'], url=v['url']) for v in articles.values() if 'content' in v])

        return self.compare_and_rank(articles=articles), self.simple_profile

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def get_personality_insights(creds=default_credentials):
    personality_insights = PersonalityInsightsV3(
        version=LATEST_VERSION,
        username=creds['username'],
        password=creds['password'],
        url=creds['url']
        )
    return personality_insights

class PersonalityInsightsWrapper:
    user_dir = "fit_user"
    def __init__(self, creds, username):
        self.creds = creds

        self.username = username
        self.init_user()

    def get_username(self):
        return self.username

    def init_user(self):
        db = get_firebase(db=True)
        exists = db.child(self.user_dir).child(self.username).get().val()
        if not exists:
            return db.child(self.user_dir).set({self.username: {'createdAt': datetime.datetime.utcnow().timestamp()}})
        else:
            return exists

    def insert_content(self, content, content_type="text/plain", language='en'): # 'text/plain' or 'application/json'
        db = get_firebase(db=True)
        data = {'content': content, 'contenttype': content_type, 'language': language}
        return db.child(self.user_dir).child(self.username).child("contentItems").push(data)

    def get_content_items(self):
        db = get_firebase(db=True)
        content_item_dict = db.child(self.user_dir).child(self.username).child("contentItems").get().val()
        return content_item_dict.values()
        # formats and returns content

    def get_content_json(self):
        items = self.get_content_items()
        if not items:
            raise NotImplementedError("No content on which to base profile")
        items = list(items)
        json_items = {'contentItems': items}
        return json.dumps(json_items)

    def has_existing_personality_profile(self):
        db = get_firebase(db=True)
        return db.child(self.user_dir).child(self.username).child("personalityProfile").get().val()

    def format_profile(self, profile):
        print(profile)
        profile = [(trait['name'], round(trait['percentile'], 4)) for trait in profile]
        return profile


    def get_and_save_profile(self):
        if 'iam_api_key' in self.creds:
            print("loading api version of WPI")
            pi = PersonalityInsightsV3(version=LATEST_VERSION,
                             iam_api_key=self.creds['iam_api_key'],
                             url=self.creds['url'])
        else:
            print("loading user/passf version of WPI")
            pi = PersonalityInsightsV3(version=LATEST_VERSION,
                             username=self.creds['username'],
                             password=self.creds['password'],
                             url=self.creds['url'])

        info = self.get_content_json()

        profile = pi.profile(content=info,
                             content_type="application/json",
                             content_language="en",
                             accept_language="en")

        profile = profile['personality']

        db = get_firebase(db=True)
        db.child(self.user_dir).child(self.username).set({"personalityProfile": profile, "profileCreated": datetime.datetime.utcnow().timestamp()})

        self.profile_obj = self.format_profile(profile)

        return self.profile_obj

    def analyze_from_text(self, text):
        raise NotImplementedError("Override this in subclass")

    def analyze_from_json(self):
        raise NotImplementedError("Override this in subclass")



def get_and_save_profile(info,
                user_id,
                save = True,
                content_type="application/json",
                content_language="en",
                accept_language="en"):
    fb = get_firebase()
    db = fb.database()
    profile_if_exists = db.child(app.config.TEST_PROFILE_DIR).child(user_id).child("personality_profile").get().val()
    if profile_if_exists:
        return profile_if_exists
    pi = get_personality_insights()
    profile = pi.profile(content=info,
                         content_type=content_type,
                         content_language=content_language,
                         accept_language=accept_language)
    if save:
        update_child(app.config.TEST_PROFILE_DIR, user_id, {"personality_profile": profile})
    return profile

def update_child(directory, child_name, info, field_name=None):
    """
    Note: cannot use field_name

    :param directory: self explanatory
    :param child_name: self explanatory
    :param info: `child_name` will be updated with this
    :param field_name: Optional parameter, updates single field of child
    :return: Fields that were updated in `child_name` or `child_name/field_name`
    :rtype: OrderedDict
    """
    db = get_firebase().database()
    if not db.child(directory).child(child_name).get().val():
        print(child_name, " not there!")
        if field_name:
            raise NotImplementedError(msg="`update_child` not implemented for fields in non-existing children")
        s = db.child(directory).child(child_name).set(info)
        return s
    if field_name:
        return db.child(directory).child(child_name).child(field_name).update(info)
    return db.child(directory).child(child_name).update(info)

def generate_person():
    db = get_firebase(db=True)
    traits = [ (trait, round(score, 4)) for trait,score in zip(b5, np.random.uniform(size=5))]
    name = [random.choice(string.ascii_letters) for i in range(10)]
    db.child("fit_user_people").push({"name": name, 'personalityProfile': traits, 'team': random.choice(teams)})

def get_people():
    db = get_firebase(db=True)
    return db.child("fit_user_people").get().val().values()

def avg_team(team):
    db = get_firebase(db=True)
    people = db.child("fit_user_people").order_by_child("team").equal_to(team).get().val().values()
    return np.mean([extract_from_simple(profile['personalityProfile']) for profile in people], axis=0)

def avg_big_five_distance_from_teams(user, normalize):
    profile = extract_from_simple(user['personalityProfile'])
    results = []
    for team in teams:
        team_avg = avg_team(team)
        score = np.sqrt(np.sum((profile - team_avg)**2))
        results.append((team, score))
    if normalize:

        simple_results = extract_from_simple(results)
        max_val, min_val = max(simple_results) + np.random.uniform(low=0,high=0.05,size=1)[0] , min(simple_results) + np.random.uniform(low=-0.1,high=0,size=1)[0]
        results = [(name,normalize_val(score,max_val, min_val)) for name,score in results]

    return results
def normalize_val(val, max_val, min_val):
    range_val = max_val - min_val
    return 100 * (1 - (val - min_val)/range_val)
def extract_from_simple(profile):
    return np.array([score for name,score in profile])

b5 = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Emotional range']
teams = ['Engineering', 'Sales', 'Marketing', 'Product dev', 'Hardware']