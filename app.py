from flask import Flask, request, render_template, jsonify, abort
import main  # Import your existing main.py script

app = Flask(__name__)

langs = main.read_langs('langs.txt') or ['fr']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    image_url = request.form['image_url']
    images, errors = main.search_image(image_url, langs)  # Modify languages as needed
    if len(errors) != 0:
        return jsonify({"errors": [str(error) for error in errors]}), 400
    return jsonify(images)

if __name__ == '__main__':
    app.run(debug=True)
