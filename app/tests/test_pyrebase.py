import pyrebase
from app.logosinsights.logospersonutils import get_firebase
def test_get_pyrebase_instance():
    assert get_firebase().database()

def test_set_and_get():
    fb = get_firebase()
    db = fb.database()
    assert db
    v = {"foo": "bar"}
    db.child("test_firebase").set(v)
    assert db.child("test_firebase").get().val() == v
    assert not db.child("test_firebase").child("foo").remove()
    assert not db.child("test_firebase").get().val()
