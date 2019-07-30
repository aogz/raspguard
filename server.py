import os
from flask import Flask, render_template, send_from_directory, request, redirect

from raspguard import settings

app = Flask(__name__)

@app.route('/')
def home():
    gif_files = os.listdir(settings.GIF_FOLDER)
    return render_template('gif-list.html', files=gif_files)

@app.route('/delete/', methods=['POST'])
def delete():
    gif_to_delete = request.form.get('filename')
    gif_files = os.listdir(settings.GIF_FOLDER)
    if gif_to_delete in gif_files:
        os.remove(os.path.join(settings.GIF_FOLDER, gif_to_delete))

    return redirect('/')

@app.route('/gif/<path:path>')
def send_gif(path):
    return send_from_directory(settings.GIF_FOLDER, path)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
