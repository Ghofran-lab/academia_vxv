# strategie_multilingue.md

## Objectif

Ce document définit comment l'académie étend sa méthode au-delà du français, et comment
la base de connaissances doit être organisée pour qu'une nouvelle langue puisse être
ajoutée **sans réécrire la philosophie pédagogique**.

Il existe parce que, à ce jour, la quasi-totalité des documents et du code de l'académie
sont pensés pour un seul cas : **enseigner le français à des italophones et des
anglophones** (voir `05-donnees/generation/prompts/course-generation-prompt.md` et
`03-pedagogie/plateforme/src/services/courseGenerationSchema.js`). Or `01-strategie/mission.md`
est explicite : *« L'académie n'est pas limitée à une seule langue. »*

Sans ce document, chaque nouvelle langue cible risquerait d'être ajoutée comme une
exception ad hoc, en dupliquant ou en contournant la charte, le style et les standards.

---

## Deux notions à ne jamais confondre

| Notion | Définition | Exemple |
| --- | --- | --- |
| **Langue cible** | La langue que l'apprenant est en train d'apprendre. | Le français, dans un cours de français. |
| **Langue source (audience)** | La ou les langues maternelles / de référence de l'apprenant, qui influencent ses difficultés et ses points de repère. | Un apprenant italophone ou anglophone qui apprend le français. |

Toute la documentation pédagogique doit raisonner avec **ce couple** (langue cible,
langue(s) source(s)), jamais avec une seule langue implicite.

> Règle de nommage : dans les documents et les données, on dira toujours
> *« cours de [langue cible] pour [langue source] »* — par exemple *« cours de français
> pour italophones »*, *« cours d'italien pour francophones »*.

---

## État actuel (2026-06-11)

- **Langue cible active** : français (FLE).
- **Langues sources couvertes** : italophones, anglophones (voir le champ `audience`
  dans `courseGenerationSchema.js` et `seed-courses.json`).
- Le prompt de génération (`course-generation-prompt.md`) est rédigé spécifiquement
  pour un « professeur expert en FLE... spécialisé dans l'enseignement du français aux
  apprenants italophones et anglophones ». C'est correct pour la phase actuelle, mais
  **ce prompt ne doit pas être copié tel quel** pour une nouvelle langue cible : il doit
  être généré à partir des documents transversaux + d'un document spécifique à la
  nouvelle langue.

---

## Feuille de route des langues

Ordre indicatif, à ajuster dans `01-strategie/vision.md` et lors des revues
stratégiques :

1. **Français** (langue cible active) — pour italophones et anglophones.
2. **Italien** (langue cible suivante) — pour francophones et anglophones en priorité,
   car ce sont déjà des publics connus de l'académie.
3. **Anglais** (langue cible suivante) — pour francophones et italophones.
4. **Autres langues** — à définir selon la demande (espagnol, allemand, etc. sont des
   candidats naturels au vu des publics et profils déjà identifiés dans `mission.md`).

Cet ordre maximise la réutilisation : les premiers apprenants d'italien ou d'anglais
sont probablement déjà des francophones connus de l'académie (effet de communauté), et
les agents Grammaire / Prononciation peuvent réutiliser l'analyse contrastive
français ↔ italien ↔ anglais déjà entamée côté FLE, mais dans l'autre sens.

---

## Ce qui est transversal (ne change pas avec la langue)

Ces documents s'appliquent **quelle que soit la langue cible et la langue source**. Ils
ne doivent jamais contenir d'exemple, de règle ou de son spécifique à une langue
particulière sans le présenter explicitement comme un *exemple d'illustration* :

- `03-pedagogie/charte_pedagogique.md`
- `03-pedagogie/style_pedagogique.md`
- `03-pedagogie/structure-des-cours.md`
- `03-pedagogie/standards_qualite.md`
- `03-pedagogie/niveaux_cecrl.md`
- `03-pedagogie/types_exercices.md`
- `03-pedagogie/philosophie_grammaire.md` (la *démarche* d'enseignement de la grammaire)
- `03-pedagogie/philosophie_prononciation.md` (la *démarche* d'enseignement de l'oral)

## Ce qui est spécifique à une langue (à créer au fur et à mesure)

Lorsqu'une nouvelle langue cible est ajoutée, créer un sous-dossier
`03-pedagogie/langues/<code-langue>/` (ex. `fr/`, `it/`, `en/`) contenant :

- `phonetique.md` : inventaire des sons spécifiques à la langue, difficultés connues
  pour chaque langue source, transcriptions simplifiées utilisées par l'académie.
- `grammaire-reference.md` : points grammaticaux propres à la langue cible (temps
  verbaux, accords, structures) et leur ordre de priorité par niveau CECRL.
- `erreurs-frequentes.md` : tableau d'interférences par langue source → langue cible
  (ex. *« un francophone apprenant l'italien confond souvent... »*).

Ces documents **complètent** `philosophie_grammaire.md` et
`philosophie_prononciation.md`, ils ne les remplacent jamais. En cas de conflit, les
documents transversaux ont priorité (voir `00-systeme/agent_knowledge_map.md`).

> Tant que ces dossiers n'existent pas (cas du français aujourd'hui), les contenus
> spécifiques à la langue restent directement dans les sections `common_mistakes` et
> `examples_table` des cours, comme c'est déjà le cas dans `seed-courses.json`.

---

## Le champ « audience » : un point de vigilance technique

Aujourd'hui, `courseGenerationSchema.js` définit `audience` comme une énumération fixe :
`Tous les apprenants`, `Italophones`, `Anglophones`. Cette énumération **suppose que la
langue cible est le français**. Si elle est copiée telle quelle pour un cours
d'italien, *« Anglophones »* resterait correct, mais il faudrait ajouter
*« Francophones »* — et pour un cours d'anglais, l'énumération entière devrait changer.

**Recommandation pour l'Agent Plateforme et l'Agent Gestionnaire de Connaissances** :

- ne pas multiplier les énumérations figées par langue cible ;
- remplacer à terme l'énumération fermée par une valeur libre mais contrôlée
  (ex. `learner_native_language: "fr" | "it" | "en" | "Tous les apprenants"`), avec une
  liste de langues sources maintenue dans ce document ;
- tant que cette migration n'est pas faite, tout nouveau cours dans une langue cible
  différente du français doit documenter explicitement, dans sa fiche de demande
  (`05-donnees/generation/requests/`), les valeurs `audience` attendues — voir
  `03-pedagogie/standards_qualite.md`.

---

## Convention d'identifiants

Les identifiants actuels (`R-A1-PRON-001`, `MOD-GRAM-B1`...) n'encodent pas la langue
cible, ce qui est correct tant qu'une seule langue cible existe. **Dès qu'une deuxième
langue cible est ajoutée**, les nouveaux identifiants doivent inclure un code langue
cible à deux lettres (ISO 639-1) pour éviter toute collision :

```text
R-<LANGUE_CIBLE>-<NIVEAU>-<CATEGORIE>-<NUMERO>
ex. R-IT-A1-PRON-001, R-EN-B1-GRAM-003
```

Les identifiants existants (français) ne sont pas rétroactivement renommés ; le code
`FR` peut être considéré comme implicite pour tout identifiant créé avant l'introduction
de cette convention.

---

## Agents concernés

| Agent | Usage de ce document |
| --- | --- |
| Orchestrateur | Identifier la langue cible et la/les langue(s) source(s) de la demande avant de répartir le travail. |
| Architecte Pédagogique | Vérifier si des documents spécifiques à la langue existent déjà, et dans quel ordre de priorité aborder les notions. |
| Grammaire | Savoir quelles interférences langue source → langue cible documenter en priorité. |
| Prononciation | Savoir quels contrastes phonétiques documenter en priorité selon la langue source. |
| Gestionnaire de Connaissances | Suivre la couverture multilingue (langues, paires, golden examples) et proposer les prochains documents `03-pedagogie/langues/<code>/`. |
| Plateforme | Anticiper les évolutions de schéma liées au champ `audience` et aux identifiants. |

---

## Décisions prises

- L'académie raisonne toujours en couple (langue cible, langue source), jamais en
  langue unique implicite.
- Les documents transversaux listés ci-dessus doivent rester indépendants de toute
  langue spécifique.
- L'ordre de priorité des langues cibles est : français (actif), italien, anglais,
  autres langues à définir.

## Questions ouvertes

- Faut-il migrer le champ `audience` vers un modèle ouvert avant ou après le lancement
  de la deuxième langue cible ?
- Quelles langues sources prioriser pour l'italien et l'anglais au-delà de
  francophones/italophones/anglophones (ex. hispanophones, germanophones) ?
- À partir de quel volume de contenus une langue cible justifie-t-elle un Agent
  Grammaire / Prononciation dédié plutôt que le partage des agents généralistes actuels ?
