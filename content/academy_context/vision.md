# vision.md

## Rôle de ce document

`mission.md` répond à la question **« pourquoi l'académie existe »**.

`vision.md` répond à la question **« où va l'académie »**.

Ce document décrit l'état cible vers lequel tend l'ensemble du système — plateforme,
base de connaissances, équipe d'agents IA et génération de contenus — sur un horizon de
3 à 5 ans. Il sert de boussole pour l'Agent Orchestrateur et pour l'Agent Gestionnaire de
Connaissances lorsqu'ils doivent arbitrer entre plusieurs évolutions possibles du système.

Dans la hiérarchie documentaire (`00-systeme/agent_knowledge_map.md`), `vision.md` est le
document de plus bas rang : il n'impose jamais une règle de production de contenu (cela
reste le rôle de la charte, du style pédagogique et des standards qualité). Il sert à
trancher des questions du type *« cette nouvelle fonctionnalité / ce nouveau document
nous rapproche-t-il de la vision ? »*.

---

## L'académie dans 3 à 5 ans

### 1. Une académie multilingue, pas seulement un cours de français

L'académie aura dépassé le stade « FLE pour italophones et anglophones » pour devenir une
méthode capable d'enseigner **plusieurs langues** (français, italien, anglais, puis
d'autres) à des apprenants de **plusieurs langues maternelles**, en conservant la même
philosophie pédagogique pour toutes les combinaisons.

Le détail de cette extension (priorités, paires de langues, impact sur la documentation)
est défini dans `01-strategie/strategie_multilingue.md`.

### 2. Un système d'exploitation pédagogique (Academy OS), pas une collection de fichiers

Les quatre chantiers menés en parallèle aujourd'hui — plateforme, base de connaissances,
équipe d'agents IA, génération automatique de contenus — convergent vers **un seul
système cohérent** :

- la base de connaissances (`00-systeme/`, `01-strategie/`, `03-pedagogie/`) définit les
  règles et la philosophie ;
- l'équipe d'agents IA (`00-systeme/agents.md`) applique ces règles pour produire du
  contenu ;
- le pipeline de génération (`05-donnees/generation/`) transforme ces productions en
  données structurées ;
- la plateforme (`03-pedagogie/plateforme/`) les rend accessibles aux apprenants.

Un changement dans la base de connaissances doit pouvoir se propager jusqu'à la
plateforme sans rupture de cohérence. C'est la responsabilité conjointe de l'Agent
Gestionnaire de Connaissances et de l'Agent Plateforme.

### 3. Une académie qui apprend de sa propre production

Le workflow d'amélioration continue (`00-systeme/workflow_agentique.md`) doit devenir un
réflexe systématique : chaque cours produit, chaque erreur détectée, chaque retour
d'apprenant nourrit la base de connaissances (golden examples, erreurs fréquentes,
ajustements de style).

À terme, la qualité des cours générés automatiquement doit être **indiscernable** d'un
cours conçu par un excellent professeur particulier — et s'améliorer dans le temps sans
réécriture manuelle systématique.

### 4. Une académie qui produit massivement sans perdre l'humain

La génération automatique de contenus existe pour **démultiplier** le travail pédagogique
humain, pas pour le remplacer :

- les choix structurants (mission, charte, style, standards, intégration d'un golden
  example) restent des décisions humaines (`00-systeme/workflow_agentique.md`,
  section *Principe de validation humaine*) ;
- la production volumique (déclinaison d'un module sur toutes les leçons d'un niveau,
  génération d'exercices supplémentaires, traduction de la méthode vers une nouvelle
  langue) est déléguée aux agents.

---

## Ce qui ne changera pas (invariants)

Quelle que soit la langue enseignée ou l'échelle atteinte, ces principes restent fixes :

- la communication prime sur la théorie ;
- la grammaire et la prononciation sont au service de la communication ;
- l'apprenant est acteur, jamais simple lecteur ;
- l'erreur est une information, pas un échec ;
- l'autonomie de l'apprenant est l'objectif final de tout parcours.

Toute évolution du système (nouvelle langue, nouvel agent, nouveau format) qui
remettrait en cause un de ces invariants doit être soumise à validation humaine, même si
elle est par ailleurs cohérente avec `vision.md`.

## Ce qui va évoluer

- le nombre de langues enseignées et de paires langue cible / langue source couvertes ;
- le nombre et la spécialisation des agents (`00-systeme/agents.md` est un document
  vivant) ;
- les formats de contenus et types d'exercices (`03-pedagogie/types_exercices.md`
  s'enrichira avec l'usage) ;
- le degré d'automatisation du pipeline de génération (`05-donnees/generation/`).

---

## Indicateurs de réussite à 3-5 ans

Ces indicateurs servent de repères qualitatifs pour l'Agent Gestionnaire de Connaissances
lors de ses revues périodiques. Ils ne remplacent pas des indicateurs business chiffrés,
qui relèveront de `01-strategie/objectifs_*` lorsque ces dossiers seront créés.

- Un nouvel apprenant peut suivre un parcours complet (découverte → pratique →
  réutilisation) sans qu'aucune étape ne ressemble à une fiche de grammaire ou à une
  liste de règles.
- Un cours généré automatiquement à partir d'une fiche de demande respecte la charte, le
  style pédagogique et les standards qualité sans intervention humaine lourde.
- La méthode peut être déclinée pour une nouvelle langue cible en réutilisant les
  documents transversaux (`charte_pedagogique.md`, `style_pedagogique.md`,
  `structure-des-cours.md`, `types_exercices.md`, `niveaux_cecrl.md`) et en ne créant
  que des documents spécifiques à cette langue.
- Le dossier `03-pedagogie/examples/` contient, pour chaque langue active et chaque
  grand type de notion (grammaire, prononciation, vocabulaire), au moins un golden
  example à jour.

---

## Décisions prises

- L'académie vise une couverture multilingue progressive, pas un élargissement
  improvisé : chaque nouvelle langue suit `01-strategie/strategie_multilingue.md`.
- La cohérence documentaire prime sur la vitesse : un nouveau document ne doit jamais
  contredire un document de rang supérieur dans `00-systeme/agent_knowledge_map.md`.
- L'automatisation est un multiplicateur de qualité humaine, pas un substitut.

## Questions ouvertes

- Quel rythme cible pour l'ajout d'une nouvelle langue (ex. une langue cible
  supplémentaire tous les combien de mois) ?
- À partir de quel volume de contenus faut-il un Agent dédié par langue plutôt qu'un
  Agent Grammaire / Prononciation généraliste ?
- Comment mesurer concrètement la progression vers l'autonomie de l'apprenant (au-delà
  du niveau CECRL) ?
