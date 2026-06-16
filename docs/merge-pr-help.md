# Refaire la Pull Request et résoudre le conflit du workflow

Ce guide sert si GitHub vous propose de résoudre un conflit avec des choix comme **Current change** et **Incoming change**.

## 1. Objectif

La branche à merger doit conserver le workflow corrigé qui utilise Node.js 24.

Dans `.github/workflows/weekly-content.yml`, la bonne version contient :

```yaml
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"
```

et :

```yaml
uses: actions/checkout@v5
uses: actions/setup-python@v6
```

Si une version contient encore `actions/checkout@v4` ou `actions/setup-python@v5`, ne gardez pas cette version.

## 2. Quel bouton choisir ?

GitHub ou VS Code peut afficher :

- **Accept Current Change** / **Accepter le changement actuel**
- **Accept Incoming Change** / **Accepter le changement entrant**

Ne choisissez pas uniquement selon le nom du bouton. Choisissez la version qui contient :

```text
FORCE_JAVASCRIPT_ACTIONS_TO_NODE24
checkout@v5
setup-python@v6
```

Dans le cas le plus probable, si vous mergez la branche de correction vers `main`, la bonne option est souvent :

```text
Accept Incoming Change
```

Mais vérifiez toujours le contenu avant de valider.

## 3. Version complète à garder pour le workflow

Le début du fichier `.github/workflows/weekly-content.yml` doit ressembler à ceci :

```yaml
name: Weekly AI Social Content

on:
  workflow_dispatch:
  schedule:
    - cron: "0 8 * * 1"

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"

jobs:
  generate-content:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.11"
```

## 4. Après résolution du conflit

1. Cliquez sur **Mark as resolved** ou l'équivalent.
2. Terminez la résolution du conflit.
3. Mergez la Pull Request.
4. Allez dans **Actions**.
5. Lancez **Weekly AI Social Content** avec **Run workflow** depuis la branche principale.

## 5. Si l'avertissement Node.js 20 apparaît encore

Cela signifie presque toujours que GitHub exécute encore une ancienne version du workflow.

Vérifiez que :

1. la Pull Request contenant ce fichier a bien été mergée ;
2. vous lancez le workflow depuis la branche principale ;
3. vous ne relancez pas une ancienne exécution avec **Re-run jobs**.
