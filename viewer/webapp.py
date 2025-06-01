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

    data.pop('__preset__', None)

    return render_template_string("""
    <html>
    <head>
        <title>ytdl-sub Abonnements</title>
        <style>
            /* mêmes styles que précédemment */
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
        </style>
    </head>
    <body>
        <h1>Abonnements ytdl-sub</h1>
        {% for category, subcats in data.items() %}
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
    """, data=data)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
