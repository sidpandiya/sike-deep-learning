from flask import Flask, request, url_for, render_template, flash, redirect, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
from app.logosinsights.logospersonutils import update_child, get_and_save_profile, avg_big_five_distance_from_teams
from app import LogosInsightsUser, LogosInsightsUserSession, PersonalityInsightsWrapper
import os, json, app.config, math
from app.logosinsights.ctu import get_comment, get_replies, get_thread_analysis, bias_rating, update_thread_with_comment
from app.logosinsights.wpcreds import creds as default_credentials


UPLOAD_FOLDER = "./uploads"
print(os.getcwd(), " is the working directory")
ALLOWED_EXTENSIONS = set(["json", 'txt'])

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# TODO: ADD SUPPORT FOR DIFF KINDS OF FILES
@app.route('/upload/<username>' , methods = ["GET", "POST"])
def profile_file_upload(username):
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')

            return redirect(request.url)

        if file and get_file_extension(file.filename) == "txt":
            # analyze
            text = str(file.read())

            pass

        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ob = json.loads(file.read())
            profile = get_and_save_profile(info=ob, user_id=username)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(profile)

    return '''
        <!doctype html>
        <title>Upload new Profile</title>
        <h1>Upload new Profile</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''
@app.route('/profile/<username>', methods = ["GET", "POST"])
def index(username):
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')

            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ob = json.loads(file.read())
            profile = get_and_save_profile(info=ob, user_id=username)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(profile)
            #return redirect(url_for('uploaded_file',
             #                       filename=filename))
    else:

        session = LogosInsightsUserSession(user_id=username)
        articles, profile = session.suggest_articles()
        articles = sorted(articles, key = lambda x: x['sim'])
        return render_template('myinsights.html', traits=profile, articles=articles, username=username)

    return '''
        <!doctype html>
        <title>Upload new Profile</title>
        <h1>Upload new Profile</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''

@app.route('/fit/<username>', methods = ["GET", "POST"])
def fit_user(username):
    piw = PersonalityInsightsWrapper(creds=default_credentials, username=username)
    if request.method == 'POST':
        if 'doctext' not in request.form or not request.form['doctext']:
            return render_template('base.html',
                                   username=username,
                                   msg="Please include both an employee identifier and some text.",
                                   msg_style="background-color: #ffe5e5;")


        elif request.form['doctext']:
            text = request.form['doctext']
            piw.insert_content(content=text)
            profile = {'personalityProfile': piw.get_and_save_profile()}
            analysis = avg_big_five_distance_from_teams(profile, normalize=True)
            print(analysis)
            analysis = [(name, round(score,2)) for name, score in analysis]
            analysis = list(sorted(analysis, key=lambda x: -1 * x[1]))
            profile = [(name, round(score,2)) for name, score in profile['personalityProfile']]
            return render_template('fitdemo.html', username=username, traits=profile, team_scores=analysis)

        elif len(request.form['doctext'].split(" ")) < 300:
            return render_template('fitdemo.html',
                                   username=username,
                                   msg="Please input a piece of text with more than three hundred tokens.",
                                   msg_style="background-color: #ffe5e5;")
        else:
            return render_template('fitdemo.html',
                                   username=username,
                                   msg="Please input a piece of text.",
                                   msg_style="background-color: #ffe5e5;")

    return render_template('base.html', username=username)

@app.route("/quality")
def demo_quality():
    comment2 = get_comment('TESTCOMMENT4')
    comment3 = get_comment('TESTCOMMENT5')

    print(comment2)
    print(comment3)

    replies1 = get_replies('TESTCOMMENT3').values()

    print(replies1)

    comment2['score'] = round(update_thread_with_comment('TESTCOMMENT4', only_points=True), 4)
    comment3['score'] = round(update_thread_with_comment('TESTCOMMENT5', only_points=True), 4)

    return render_template('quality.html', comment2=comment2, comment3=comment3, replies1=replies1)


@app.route("/diversity")
def demo_diversity():
    comment1 = get_comment('TESTCOMMENT1')
    comment2 = get_comment('TESTCOMMENT2')
    replies1 = get_replies('TESTCOMMENT1').values()
    print(replies1)
    replies2 = get_replies('TESTCOMMENT2').values()
    c1 = get_thread_analysis("TESTCOMMENT1")
    c2 = get_thread_analysis("TESTCOMMENT2")
    comment1['score'] = round(round(0.3 - bias_rating(c1['sentiment'], c1['mag_adj']), 4) * 100, 4)

    comment2['score'] = round(round(0.3 - bias_rating(c2['sentiment'], c2['mag_adj']), 4) * 100, 4)
    return render_template('diversity.html', comment1=comment1, comment2=comment2, replies1=replies1, replies2=replies2)

@app.route("/fit")
def team_distance_demo():
    pass


if __name__ == "__main__":
    app.run()
