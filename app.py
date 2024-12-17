from flask import Flask, request, redirect, send_from_directory
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


@app.route('/images/<filename>/<foldername>')
def serve_image(filename, foldername):

    return send_from_directory(f"E:/NAMES/{foldername}", filename)   

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/upload")
def upload():
    return render_template('upload.html')


@app.route("/saveMessage", methods=["POST"])
def saveMessage():
    folder = request.form.get('folder')

    images = request.files.getlist('image')

    if not os.path.exists(f"E:/NAMES/{folder}"):
        os.makedirs(f"E:/NAMES/{folder}")

    for image in images:
        image.save(f"E:/NAMES/{folder}/{image.filename}")


    return redirect("/")     


@app.route("/show")
def show():

    with open("E:/NAMES/names.txt", "r", encoding="utf-8") as file:
        file_contents = file.read()

    file_contents = file_contents.replace("\n", "<br/>")    

    
    return f"{file_contents}"


@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/browse", methods=["POST"])
def browse():

    folder = request.form.get('folder')
    val = int(request.form.get('startPoint'))

    if not os.path.exists(f"E:/NAMES/{folder}"):
        return render_template('search.html')
    
    images = os.listdir(f"E:/NAMES/{folder}")
    
    if val+5 >= len(images):
        subImages = images[:]
        lastPage = True
    else:
        subImages = images[:5]
        lastPage = False
    print(images)

    return render_template('browse.html' ,images=images, folder=folder, subImages=subImages, page=1, lastPage=lastPage)

@app.route("/changePage", methods=["POST"])
def changePage():
    
    folder = request.form.get('folder')
    page = int(request.form.get('startPoint'))

    images = os.listdir(f"E:/NAMES/{folder}")

    print("____________fefefef_____________")
    print(images)
    if page*5 >= len(images):
        subImages = images[(page-1)*5:]
        lastPage = True
    else:
        subImages = images[(page-1)*5:page*5]
        lastPage = False
   
    return render_template('browse.html', folder=folder, subImages=subImages, page=page, lastPage=lastPage)

@app.route('/deletePage', methods=["POST"])
def deletePage():
    image = request.form.get('image')
    folder = request.form.get('folder')
   

    os.remove(f"E:/NAMES/{folder}/{image}")

    return render_template('home.html')

@app.route('/download', methods=["POST"])
def download():
    image = request.form.get('image')
    folder = request.form.get('folder')
    print(folder, "----", image)
    return send_from_directory(f"E:/NAMES/{folder}/", image)

@app.route('/temp')
def temp():
    return render_template('temp.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)