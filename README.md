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
