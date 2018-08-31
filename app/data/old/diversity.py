from app.logosinsights.logospersonutils import get_firebase
db = get_firebase(db=True)
data = {
'postId': "TESTPOST1",
    "post": """"The North Carolina Historical Commission voted Wednesday to keep three Confederate monuments on the grounds of the state Capitol building amid controversy about the statues’ future in the state.

The commission voted 10-1 not to remove the statues, but to add context about slavery and civil rights, according to The Associated Press. The commission also called for a monument to be built honoring African-Americans’ contributions to North Carolina.

The state commission’s vote came in response to Gov. Roy Cooper (D), who called for the three monuments to be removed from the Capitol grounds and preserved at a Civil War battlefield.

Confederate statues in the U.S. have been at the center of debate following the deadly 2017 Unite the Right rally in Charlottesville, Va., which erupted around the city’s plans to take down a statue of Confederate Gen. Robert E. Lee.

The decision came just days after protesters toppled a Confederate statue on the campus of University of North Carolina-Chapel Hill. The “Silent Sam” statue, which was erected in 1913, has been a source of contention on the campus.

According to North Carolina’s ABC11, there are more than 100 Confederate monuments, statues and memorials throughout the state. State law prohibits the removal of Confederate statues without the express permission of the state.

Beyond Silent Sam, a number of Confederate statues in North Carolina and other states have been vandalized, toppled or otherwise defaced in recent months.""",
'comment1': {
        "userId": 'test1',
        'commentId': "TESTCOMMENT1",
    'text': 'Confederate monuments = participation trophies. They\'re disgusting and should be destroyed',
'postId': "TESTPOST1",
    'reply1': {
        "userId": "TESTUSER2",
        "comments": "Shut up snowflake. nobody wants them gone except dirty liberals like you",
        "replyId": "REPLYID1",
        "commentId": "TESTCOMMENT1"
    },
    'reply2': {
        "userId": "TESTUSER3",
        "comments": "They need to go. Each and every one.",
        "replyId": "REPLYID2",
        "commentId": "TESTCOMMENT1"
    },
    'reply3': {
        "userId": "TESTUSER4",
        'text': "Of course, nothing's changed in a year at all. We haven't had another year of a piece of s**t racist in the Oval Office degrading all minorities and Republicans saying slavery is the good old days or anything... oh wait, all of those things happened. And you're still supporting enslaving black people through your dedication to traitors that enslaved black people? Disgusting.",
        'replyId': "REPLYID3",
        'commentId': "TESTCOMMENT1"
    }
    },
    'comment2': {
        "comments": "This seems to be how the issue was handled at the Texas Capitol complex in Austin. There are Civil War monuments in one section and a monument to African American history in another. It seemed pretty strange to show slaves on one monument and the people that fought to support slavery on another monument.",
        "commentId": "TESTCOMMENT2",
        'userId': "TESTUSER5",
'postId': "TESTPOST1",

'reply1': {
        "userId": "TESTUSER6",
        "comments": "Many of these monuments were erected by Union veterans in places like Ohio as a tribute to the men they opposed during the war. If former Union soldiers had such consideration/respect for a former foe that respect should endure.",
        "commentId": "TESTCOMMENT2",
        "replyId": "TESTREPLY4"
        },
'reply2': {
        "userId": "TESTUSER5",
        "comments": "The monuments honor men who fought for constitutional gov't, rule of law and defense of family and home. Slavery remained legal in the US the entire time it fought the confederates. Segregation and white supremacy were not confined to the south but were nationwide",
        "commentId": "TESTCOMMENT2",
        "replyId": "REPLYID5"
        },
'reply3': {
        "userId": "TESTUSER6",
        "comments": "Silent Sam had context: Carr was a virulent racist. In his speech that day, he recalled, “One hundred yards from where we stand, less than 90 days perhaps after my return from Appomattox, I horse-whipped a negro wench until her skirts hung in shreds, because upon the streets of this quiet village she had publicly insulted and maligned a Southern lady, and then rushed for protection to these University buildings where was stationed a garrison of 100 Federal soldiers.”",
        "commentId": "TESTCOMMENT2",
        "replyId": "REPLYID6"
        }

    }

}

def insert():
    db.child("postcontent").child("TESTPOST1").set({"content": data['post'], 'userId': "TESTUSER8"})
    comment1 = data['comment1']
    reply1 = comment1['reply1']
    reply2 = comment1['reply2']
    reply3 = comment1['reply3']
    comment2 = data['comment2']
    reply4 = comment2['reply1']
    reply5 = comment2['reply2']
    reply6 = comment2['reply3']
    db.child("postcomments").child(comment1['commentId']).set(comment1)

    db.child("commentsonpostcomments").child(reply1['replyId']).set(reply1)
    db.child("commentsonpostcomments").child(reply2['replyId']).set(reply2)
    db.child("commentsonpostcomments").child(reply3['replyId']).set(reply3)

    db.child("postcomments").child(comment2['commentId']).set(comment2)

    db.child("commentsonpostcomments").child(reply4['replyId']).set(reply4)
    db.child("commentsonpostcomments").child(reply5['replyId']).set(reply5)
    db.child("commentsonpostcomments").child(reply6['replyId']).set(reply6)

    #db.child("postcomments").child(comment1['commentId']).set(comment3)

if __name__ == "__main__":
    insert()