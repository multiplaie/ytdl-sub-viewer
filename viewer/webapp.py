from flask import Flask, render_template_string
import yaml
import os

app = Flask(__name__)

@app.route("/")
def home():
    config_path = "/config/ytdl-sub-configs/subscriptions.yaml"
    if not os.path.exists(config_path):
        return f"<h1>Erreur</h1><p>Fichier non trouvé : {config_path}</p>"

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    data.pop('__preset__', None)

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
                <tr><th>Artiste</th><th>URL</th></tr>
              </thead>
              <tbody>
              {% for artist, url in artists.items() %}
                <tr>
                  <td>{{ artist }}</td>
                  <td><a href="{{ url }}" target="_blank">{{ url }}</a></td>
                </tr>
              {% endfor %}
              </tbody>
            </table>
          {% endfor %}
        {% endfor %}
    </body>
    </html>
    """, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
