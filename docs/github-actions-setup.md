# Configurer GitHub Actions pour recevoir les contenus IA sur Telegram

Ce guide explique comment configurer le workflow `Weekly AI Social Content` depuis l'interface GitHub, sans utiliser n8n, Make ou Zapier.

## 1. Préparer les informations nécessaires

Le workflow a besoin de trois secrets GitHub :

| Secret GitHub | À quoi il sert | Où le récupérer |
| --- | --- | --- |
| `OPENAI_API_KEY` | Appeler l'IA pour générer les contenus | Plateforme OpenAI |
| `TELEGRAM_BOT_TOKEN` | Autoriser le bot Telegram à envoyer les messages | Telegram, via `@BotFather` |
| `TELEGRAM_CHAT_ID` | Indiquer dans quel chat/groupe Telegram envoyer les contenus | API Telegram `getUpdates` |

La variable `OPENAI_MODEL` est optionnelle. Si elle n'est pas configurée, le workflow utilise `gpt-4.1-mini`.


## Important : quel onglet choisir sur GitHub ?

Sur la page **Actions secrets and variables**, GitHub affiche deux onglets :

- **Secrets** : à utiliser pour les valeurs sensibles, privées ou confidentielles ;
- **Variables** : à utiliser seulement pour les valeurs non sensibles.

Pour ce projet, mettez ces trois valeurs dans l'onglet **Secrets** :

```text
OPENAI_API_KEY
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

Ne les mettez pas dans **Variables**, car une variable GitHub est visible en clair dans l'interface.

Vous êtes probablement au bon endroit si l'URL ressemble à :

```text
/settings/secrets/actions
```

Si l'URL ressemble à :

```text
/settings/variables/actions
```

alors vous êtes dans l'onglet **Variables** : cliquez simplement sur l'onglet **Secrets**, situé juste à gauche de **Variables**.

La seule valeur à mettre éventuellement dans **Variables** est :

```text
OPENAI_MODEL
```


## 2. Créer le bot Telegram

1. Ouvrez Telegram.
2. Cherchez le compte officiel `@BotFather`.
3. Envoyez la commande :

   ```text
   /newbot
   ```

4. Donnez un nom au bot, par exemple :

   ```text
   Assistant Contenu Académie
   ```

5. Donnez un identifiant qui finit par `bot`, par exemple :

   ```text
   academie_contenu_bot
   ```

6. Copiez le token donné par BotFather. Il ressemble à ceci :

   ```text
   123456789:AA...exemple...xyz
   ```

Ce token deviendra le secret GitHub `TELEGRAM_BOT_TOKEN`.

## 3. Créer le chat Telegram de réception

Vous avez deux options.

### Option A — Chat direct avec le bot

1. Ouvrez une conversation avec votre bot.
2. Envoyez-lui un message, par exemple :

   ```text
   Bonjour
   ```

### Option B — Groupe privé recommandé

1. Créez un groupe Telegram privé, par exemple `Académie - Contenus IA`.
2. Ajoutez votre bot au groupe.
3. Envoyez un message dans le groupe, par exemple :

   ```text
   Test
   ```

Le groupe privé est recommandé si vous voulez plus tard ajouter une assistante, un associé ou un community manager.

## 4. Récupérer le `TELEGRAM_CHAT_ID`

Dans votre navigateur, ouvrez cette URL en remplaçant `<TELEGRAM_BOT_TOKEN>` par le token du bot :

```text
https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates
```

Cherchez ensuite la section `chat` dans la réponse JSON.

Pour un chat direct, l'identifiant ressemble souvent à :

```json
"chat": {
  "id": 123456789,
  "type": "private"
}
```

Pour un groupe, l'identifiant est souvent négatif, par exemple :

```json
"chat": {
  "id": -1001234567890,
  "title": "Académie - Contenus IA",
  "type": "supergroup"
}
```

La valeur de `id` devient le secret GitHub `TELEGRAM_CHAT_ID`.

> Si la réponse ne contient aucun message, envoyez d'abord un nouveau message au bot ou dans le groupe, puis rechargez l'URL `getUpdates`.

## 5. Ajouter les secrets dans GitHub

Depuis votre dépôt GitHub :

1. Ouvrez l'onglet **Settings**.
2. Dans le menu de gauche, cliquez sur **Secrets and variables**.
3. Cliquez sur **Actions**.
4. Vérifiez que vous êtes bien dans l'onglet **Secrets**, pas dans **Variables**.
5. Cliquez sur **New repository secret**.
6. Ajoutez les secrets un par un :
4. Cliquez sur **New repository secret**.
5. Ajoutez les secrets un par un :

   ```text
   OPENAI_API_KEY
   TELEGRAM_BOT_TOKEN
   TELEGRAM_CHAT_ID
   ```

7. Collez la valeur correspondante pour chaque secret.
8. Cliquez sur **Add secret** après chaque ajout.
6. Collez la valeur correspondante pour chaque secret.
7. Cliquez sur **Add secret** après chaque ajout.

## 6. Ajouter le modèle OpenAI optionnel

Cette étape est optionnelle.

Depuis la même page GitHub :

1. Allez dans **Settings** → **Secrets and variables** → **Actions**.
2. Ouvrez l'onglet **Variables**.
3. Cliquez sur **New repository variable**.
4. Ajoutez :

   ```text
   OPENAI_MODEL
   ```

5. Valeur recommandée pour commencer :

   ```text
   gpt-4.1-mini
   ```

## 7. Ajouter la mission et la vision de l'académie

Créez vos fichiers Markdown dans :

```text
content/academy_context/
```

Fichiers conseillés pour commencer :

```text
content/academy_context/mission.md
content/academy_context/vision.md
```

Vous pouvez vous inspirer de :

```text
content/academy_context/mission.example.md
content/academy_context/vision.example.md
```

Le générateur ignore automatiquement les fichiers `README.md` et `*.example.md`, donc vos vrais fichiers doivent s'appeler par exemple `mission.md` et `vision.md`.

## 8. Lancer le workflow manuellement

Depuis GitHub :

1. Ouvrez l'onglet **Actions**.
2. Cliquez sur le workflow **Weekly AI Social Content**.
3. Cliquez sur **Run workflow**.
4. Gardez la branche actuelle sélectionnée.
5. Cliquez sur le bouton vert **Run workflow**.

Le workflow va ensuite :

1. installer le projet Python ;
2. lire les fichiers Markdown dans `content/academy_context/` ;
3. appeler OpenAI ;
4. générer le planning social media ;
5. envoyer le résultat sur Telegram.

## 9. Vérifier que tout fonctionne

Dans l'onglet **Actions**, ouvrez la dernière exécution du workflow.

Vous devez voir une étape :

```text
Generate weekly content and send to Telegram
```

Si tout fonctionne, vous recevrez un message Telegram intitulé :

```text
🎓 Contenus de la semaine
```

## 10. Problèmes fréquents

### Le workflow échoue avec `OPENAI_API_KEY is required`

Le secret `OPENAI_API_KEY` n'a pas été ajouté, est mal nommé ou est vide.

### Le workflow échoue avec `TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID sont requis`

Vérifiez que les deux secrets existent exactement avec ces noms :

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

### Telegram ne reçoit rien

Vérifiez que :

- vous avez envoyé au moins un message au bot ou dans le groupe ;
- le bot est bien membre du groupe ;
- le `TELEGRAM_CHAT_ID` correspond au bon chat ;
- pour un groupe, vous avez bien copié l'identifiant négatif complet.

### Les contenus sont trop génériques

Ajoutez plus de contexte dans :

```text
content/academy_context/
```

Priorité :

1. `mission.md`
2. `vision.md`
3. `offres.md`
4. `audience.md`
5. `tonalite.md`
