# academia_vxv

Outils pour constituer une base de connaissances Markdown à partir d'exercices publics de français.

## Scraper francaisfacile.com

Ce dépôt fournit un scraper Python prudent pour exporter des exercices et leurs corrections depuis des pages publiques de `francaisfacile.com` vers des fichiers `.md` utilisables par une plateforme pédagogique ou un moteur RAG.

> Important : vérifiez les conditions d'utilisation du site, respectez `robots.txt`, conservez l'attribution de la source et évitez de republier des contenus protégés sans autorisation. Le scraper vérifie `robots.txt` par défaut, limite le domaine à `francaisfacile.com` et attend 2 secondes entre deux requêtes.

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

### Exporter des URLs connues

```bash
francaisfacile-scrape \
  --url 'https://www.francaisfacile.com/exercices/exercice-francais-123.php' \
  --output-dir knowledge_base/francaisfacile
```

### Exporter depuis un fichier d'URLs

Créez un fichier `urls.txt` avec une URL par ligne, puis lancez :

```bash
francaisfacile-scrape --urls-file urls.txt --output-dir knowledge_base/francaisfacile
```

### Découvrir des exercices depuis une page d'index

```bash
francaisfacile-scrape \
  --index-url 'https://www.francaisfacile.com/exercices/' \
  --max-pages 25 \
  --delay 3 \
  --output-dir knowledge_base/francaisfacile
```

### Format généré

Chaque fichier Markdown contient :

- un bloc YAML avec `title`, `source_url`, `scraped_at` et `content_type` ;
- une section `Énoncé` ;
- une section `Questions` quand elles sont détectables ;
- une section `Correction` quand elle est présente dans la page publique ;
- une section `Source` pour conserver l'attribution.

### Options utiles

- `--delay 3` : augmente la pause entre requêtes.
- `--max-pages 50` : limite le nombre de pages exportées.
- `--user-agent 'mon-bot/1.0 (+email@example.com)'` : renseigne un user-agent identifiable.
- `--ignore-robots` : désactive la vérification `robots.txt`; à n'utiliser que si vous avez une autorisation explicite.

### Tests

```bash
pytest
```

## Génération IA de contenus social media

Le dépôt peut aussi générer un planning de contenus pour l'académie de langues et l'envoyer sur Telegram, sans passer par n8n, Make ou Zapier.

### Où déposer la mission et la vision

Ajoutez vos fichiers Markdown dans :

```text
content/academy_context/
```

Le générateur lit automatiquement tous les fichiers `*.md` de ce dossier. Vous pouvez commencer par :

- `content/academy_context/mission.md` : mission, valeurs, promesse pédagogique ;
- `content/academy_context/vision.md` : ambition, positionnement, différence ;
- `content/academy_context/offres.md` : langues, formules, cours d'essai, test de niveau ;
- `content/academy_context/audience.md` : profils d'élèves, objectifs, objections ;
- `content/academy_context/tonalite.md` : style, mots à utiliser, mots à éviter.

Des exemples sont fournis dans `content/academy_context/mission.example.md` et `content/academy_context/vision.example.md`.

### Tester le prompt sans appeler l'IA

```bash
academia-content weekly --dry-run
```

### Générer les contenus

Définissez d'abord la clé API OpenAI :

```bash
export OPENAI_API_KEY='votre-cle'
```

Puis lancez :

```bash
academia-content weekly
```

Le résultat est sauvegardé dans :

```text
content/generated/
```

### Envoyer sur Telegram

Créez un bot avec `@BotFather`, récupérez le token, puis définissez :

```bash
export TELEGRAM_BOT_TOKEN='token-du-bot'
export TELEGRAM_CHAT_ID='id-du-chat-ou-groupe'
```

Lancez ensuite :

```bash
academia-content weekly --send-telegram
```

### Déploiement GitHub Actions

Le workflow `.github/workflows/weekly-content.yml` exécute automatiquement la génération chaque lundi à 08:00 UTC et peut aussi être lancé manuellement depuis l'onglet **Actions** de GitHub.

Secrets GitHub requis :

- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Variable optionnelle :

- `OPENAI_MODEL` pour choisir le modèle utilisé.
