import pyrebase, random, string
from app.logosinsights.logospersonutils import get_firebase, update_child

TEST_DIRECTORY = "test_firebase"
TEST_ID = ''.join([random.choice(string.ascii_lowercase) for i in range(24)])

def test_get_pyrebase_instance():
    assert get_firebase().database()

def test_set_and_get():
    fb = get_firebase()
    db = fb.database()
    assert db
    v = {"foo": "bar"}
    db.child(TEST_DIRECTORY).set(v)
    assert db.child(TEST_DIRECTORY).get().val() == v
    assert not db.child(TEST_DIRECTORY).child("foo").remove()
    assert not db.child(TEST_DIRECTORY).get().val()

def test_update_child():
    fb = get_firebase()
    db = fb.database()
    data = {TEST_ID: {"foo": "bar"}}
    db.child(TEST_DIRECTORY).set(data)
    assert db.child(TEST_DIRECTORY).get().val() == data
    newdata = {TEST_ID: {"bar": "foo"}}
    assert update_child(directory=TEST_DIRECTORY, child_name=TEST_ID, info=newdata[TEST_ID] ) == newdata[TEST_ID]

    assert not db.child(TEST_DIRECTORY).child(TEST_ID).remove()
    assert not db.child(TEST_DIRECTORY).get().val()