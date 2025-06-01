# ytdl-sub-full

Un conteneur Docker tout-en-un incluant :

- [ytdl-sub](https://github.com/jmbannon/ytdl-sub) pour la gestion des abonnements (YouTube, Bandcamp, SoundCloud…)
- Une webapp Flask affichant les abonnements à partir du fichier `subscriptions.yaml`

## Lancement

```bash
docker-compose up -d --build
```

## Volumes

- `./config` : contient `subscriptions.yaml`, `cookie.txt`, etc.
- `./music` : stockage des téléchargements

## Accès

- ytdl-sub GUI : http://localhost:8443
- Web viewer (subscriptions) : http://localhost:5000
