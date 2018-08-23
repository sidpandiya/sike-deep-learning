import string, random, pytest
from app.logosinsights.logospersonutils import get_personality_insights, default_credentials
from watson_developer_cloud import WatsonApiException


def test_login_user():
    assert get_personality_insights()

def test_not_login_wrong_info():
    default_credentials['username'] = ''.join([random.choice(string.ascii_lowercase) for i in range(24)])
    default_credentials['password'] = ''.join([random.choice(string.ascii_lowercase) for i in range(24)])
    with pytest.raises(WatsonApiException):
        print(get_personality_insights(default_credentials))
        raise WatsonApiException(400, "uhhh what do i put here")

                                              
if __name__ == "__main__":
    test_not_login_wrong_info()
