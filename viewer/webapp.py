from flask import Flask, render_template_string, request, redirect, url_for
from ruamel.yaml import YAML
import os

app = Flask(__name__)

yaml = YAML()
yaml.preserve_quotes = True

@app.route("/")
def home():
    config_path = "/config/ytdl-sub-configs/subscriptions.yaml"
    if not os.path.exists(config_path):
        return f"<h1>Erreur</h1><p>Fichier non trouvé : {config_path}</p>"

    with open(config_path, "r") as f:
        data = yaml.load(f)

    data_no_preset = dict(data)
    data_no_preset.pop('__preset__', None)

    return render_template_string("""
    <html>
    <head>
        <title>ytdl-sub Abonnements</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #2c3e50; }
            h2 { color: #34495e; margin-top: 30px; }
            h3 { color: #7f8c8d; margin-top: 15px; }
            table { border-collapse: collapse; width: 90%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #2980b9; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            a { color: #2980b9; text-decoration: none; }
            a:hover { text-decoration: underline; }
            button {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px 10px;
                cursor: pointer;
                border-radius: 3px;
            }
            button:hover {
                background-color: #c0392b;
            }
            form {
                margin: 0;
            }
            label {
                display: inline-block;
                width: 120px;
                margin-bottom: 10px;
            }
            input[type=text], input[type=url] {
                width: 300px;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Abonnements ytdl-sub</h1>

        <h2>Ajouter un nouvel artiste</h2>
        <form method="POST" action="/add" style="margin-bottom: 30px;">
          <label>Catégorie : <input type="text" name="category" required></label><br>
          <label>Sous-catégorie : <input type="text" name="subcategory" required></label><br>
          <label>Artiste : <input type="text" name="artist" required></label><br>
          <label>URL : <input type="url" name="url" required></label><br>
          <button type="submit">Ajouter</button>
        </form>

        {% for category, subcats in data_no_preset.items() %}
          <h2>{{ category }}</h2>
          {% for subcat, artists in subcats.items() %}
            <h3>{{ subcat }}</h3>
            <table>
              <thead>
                <tr><th>Artiste</th><th>URL</th><th>Actions</th></tr>
              </thead>
              <tbody>
              {% for artist, url in artists.items() %}
                <tr>
                  <td>{{ artist }}</td>
                  <td><a href="{{ url }}" target="_blank">{{ url }}</a></td>
                  <td>
                    <form method="POST" action="/delete" onsubmit="return confirm('Supprimer cet artiste ?');">
                      <input type="hidden" name="category" value="{{ category }}">
                      <input type="hidden" name="subcategory" value="{{ subcat }}">
                      <input type="hidden" name="artist" value="{{ artist }}">
                      <button type="submit">Supprimer</button>
                    </form>
                  </td>
                </tr>
              {% endfor %}
              </tbody>
            </table>
          {% endfor %}
        {% endfor %}
    </body>
    </html>
    """, data_no_preset=data_no_preset)

@app.route("/delete", methods=["POST"])
def delete():
    category = request.form.get("category")
    subcat = request.form.get("subcategory")
    artist = request.form.get("artist")

    config_path = "/config/ytdl-sub-configs/subscriptions.yaml"

    if not os.path.exists(config_path):
        return "Fichier non trouvé", 404

    with open(config_path, "r") as f:
        data = yaml.load(f)

    if category in data:
        if subcat in data[category]:
            if artist in data[category][subcat]:
                del data[category][subcat][artist]

                if not data[category][subcat]:
                    del data[category][subcat]

                if not data[category]:
                    del data[category]

                with open(config_path, "w") as f:
                    yaml.dump(data, f)

    return redirect(url_for("home"))

@app.route("/add", methods=["POST"])
def add():
    category = request.form.get("category")
    subcat = request.form.get("subcategory")
    artist = request.form.get("artist")
    url_ = request.form.get("url")

    config_path = "/config/ytdl-sub-configs/subscriptions.yaml"
    if not os.path.exists(config_path):
        return "Fichier non trouvé", 404

    with open(config_path, "r") as f:
        data = yaml.load(f)

    if data is None:
        data = {}

    # Préserve __preset__ si présent
    if '__preset__' not in data:
        data['__preset__'] = {}

    if category not in data:
        data[category] = {}
    if subcat not in data[category]:
        data[category][subcat] = {}

    data[category][subcat][artist] = url_

    with open(config_path, "w") as f:
        yaml.dump(data, f)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
