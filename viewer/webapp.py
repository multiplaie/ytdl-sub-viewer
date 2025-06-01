from flask import Flask, render_template, request, redirect, url_for
from ruamel.yaml import YAML
import os
import json

app = Flask(__name__, template_folder="templates")

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

    categories = {}
    for category, subcats in data.items():
        if category == "__preset__":
            continue
        categories[category] = list(subcats.keys())

    return render_template("index.html", data=data, categories=categories, categories_json=json.dumps(categories), data_no_preset=data_no_preset)

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
    url = request.form.get("url")

    config_path = "/config/ytdl-sub-configs/subscriptions.yaml"

    if not os.path.exists(config_path):
        return "Fichier non trouvé", 404

    with open(config_path, "r") as f:
        data = yaml.load(f)

    if category not in data:
        data[category] = {}

    if subcat not in data[category]:
        data[category][subcat] = {}

    data[category][subcat][artist] = url

    with open(config_path, "w") as f:
        yaml.dump(data, f)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
