from flask import Flask, request, url_for, render_template, flash, redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "./uploads"
print(os.getcwd(), " is the working directory")
ALLOWED_EXTENSIONS = set(["json"])

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# TODO: ADD SUPPORT FOR DIFF KINDS OF FILES
@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == 'POST':
        print(os.getcwd(), " is the working directory")
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
            print(file.read())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return '''
    <!doctype html>
    <title>Upload new Profile</title>
    <h1>Upload new Profile</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/testwd")
def testwd():

    return "\n".join([str(__file__),     os.path.join(os.path.dirname(__file__), '..'), os.path.dirname(os.path.realpath(__file__)), os.path.abspath(os.path.dirname(__file__))])

if __name__ == "__main__":
    app.run()
