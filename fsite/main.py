import os
from PIL import Image
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/upload/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'orehgldgd39432lkgjdlghdl4355844bdlld'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def img_path():
    img = os.listdir(UPLOAD_FOLDER)[0]
    imgpath = os.path.join(UPLOAD_FOLDER, img)
    return imgpath


def delete():
    os.remove(img_path())


def rotate(angle):
    im = Image.open(img_path())
    im_rot = im.rotate(int(angle), expand=True)
    im_rot.save(img_path())



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/download')
def download():
    img_file_path = session.get('uploaded_img_path', None)
    path = os.listdir(UPLOAD_FOLDER)
    return render_template('download.html', user_image=img_file_path, path=path)


@app.route('/download_img')
def download_img():
    return send_file(img_path(), as_attachment=True)


@app.route('/del')
def delete_img():
    delete()
    return redirect(url_for('home'))


@app.route('/rotate/<string:angle>')
def rotate_img(angle):
    rotate(angle)
    return redirect(url_for('flip'))


@app.route('/flip')
def flip():
    img_file_path = session.get('uploaded_img_path', None)
    path = os.listdir(UPLOAD_FOLDER)
    return render_template('flip.html', user_image=img_file_path, path=path)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if not os.listdir(UPLOAD_FOLDER):
            if 'up_image' not in request.files:
                flash('No file part')
                return redirect(request.url)
            img = request.files['up_image']

            if img.filename == '':
                flash('No selected file')
                return redirect(request.url)

            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['uploaded_img_path'] = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('flip'))
        else:
            flash('Delete the old file first')
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True) # host='0.0.0.0', port=5000,