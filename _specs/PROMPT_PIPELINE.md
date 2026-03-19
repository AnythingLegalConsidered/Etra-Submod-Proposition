# Prompt Pipeline — Creation de noms pour une langue d'Etra

Copie le bloc ci-dessous dans une nouvelle conversation Claude Code ouverte sur le repo `Etna/`.
Remplace `<LANGUE>` par le nom exact du dossier : `ardrainic`, `torrent`, `armonorican`, `sordrenic`, `moran`, `vulgar_moran`, `hravevi`.

---

```
# MISSION

Tu vas creer (ou completer/ameliorer) le systeme de noms fantasy pour la langue **<LANGUE>** du mod Etra (total conversion fantasy EU5).

On travaille etape par etape. A chaque etape, tu me presentes le resultat, j'approuve ou corrige, et on passe a la suivante. Tu ne sautes JAMAIS une etape sans mon OK.

---

# ETAPE 0 — LECTURE DU CONTEXTE

Avant toute chose, lis ces fichiers dans l'ordre. Ne genere RIEN avant d'avoir tout lu.

## Fichiers obligatoires (lis-les TOUS) :
1. `docs/PIPELINE.md` — le pipeline de reference
2. `docs/MAP_ANALYSIS.md` — analyse geographique de chaque culture (si le fichier existe)
3. `CONTEXT.md` — mapping cultures/langues, technique de modding, lacunes actuelles

## Memoire du projet (dans `.claude/projects/.../memory/`) :
4. `project_naming_method.md` — regles de naming, matrice de non-recouvrement, exemples valides/invalides
5. `project_culture_atlas.md` — atlas geographique de toutes les cultures
6. `project_dialect_plan.md` — plan des ~45 dialectes
7. `project_proto_languages.md` — proto-elfique et proto-geant (substrats raciaux)

## Fichier de la langue dans le mod original :
8. Le fichier langue du mod Etra original dans `C:\Program Files (x86)\Steam\steamapps\workshop\content\3450310\3619896881\in_game\common\languages\` — cherche le fichier qui contient cette langue

## Travail deja fait (si ca existe) :
9. TOUS les fichiers dans `names/<LANGUE>/` — STATUS.md, ADN, noms, dialectes, audit, decisions

Si un STATUS.md existe et indique une etape deja completee, reprends a l'etape suivante.
S'il n'existe pas, commence a l'etape 1.

Apres lecture, affiche un RESUME COURT :
- Langue : <nom>
- Cultures concernees : <liste>
- Races : <humain/elfe/etc>
- Etape actuelle : <X/9>
- Ce qui existe deja : <liste fichiers trouves>

---

# ETAPE 1 — FICHE D'IDENTITE

Produis une fiche pour la langue, en t'appuyant sur CONTEXT.md et l'atlas :

| Champ | Valeur |
|-------|--------|
| Langue | <nom technique> |
| Inspiration reelle | <culture(s) reelle(s)> |
| Groupe culturel | <groupe dans Etra> |
| Cultures qui la parlent | <liste avec race entre parentheses> |
| Races presentes | <humain, elfe, ratfolk, etc.> |
| Dialectes prevus | <liste, cf. dialect_plan> |
| Voisins linguistiques | <langues frontalieres> |
| Noms deja dans le mod | <X>M + <X>F + <X>dyn + <X>low (resume des noms existants) |

**Attends mon OK avant de continuer.**

---

# ETAPE 2 — PROFIL GEOGRAPHIQUE

Pour chaque culture de cette langue, donne :

| Culture | Race | Terrain | Climat | Dev. | Position | Style attendu |
|---------|------|---------|--------|------|----------|---------------|
| ... | ... | ... | ... | ... | ... | ... |

Utilise l'atlas et les cartes dans `map/` si besoin.

Impact geo sur le style des noms :
- Plaines riches → noms longs, raffines, composes
- Montagnes → noms courts, archaiques, conservateurs
- Cotes → noms rudes, tronques, marins
- Forets → noms profonds, sombres, sylvestres
- Frontiere → noms hybrides, emprunts aux voisins
- Pauvre/isole → noms simples, peu de dynasties
- Villes/commerce → noms pratiques, raccourcis, cosmopolites

**Attends mon OK avant de continuer.**

---

# ETAPE 3 — ADN PHONETIQUE

Definis l'empreinte sonore de la langue. C'est l'etape la plus importante.

### 3a. Attaques (15-25 minimum)
Liste les debuts de noms. Au moins 3 doivent etre EXCLUSIFS (aucune autre langue d'Etra ne les utilise).
Verifie la matrice de non-recouvrement dans `project_naming_method.md`.

### 3b. Terminaisons masculines (8-12)
Au moins 2 EXCLUSIVES.

### 3c. Terminaisons feminines (8-12)
Au moins 2 EXCLUSIVES. Les feminins NE SONT PAS des masculins + "e".

### 3d. Voyelles dominantes
Quelles voyelles donnent le "son" de cette langue ?

### 3e. Sons interdits
Quels sons sont RESERVES a d'autres langues et ne doivent PAS apparaitre ?
Verifie systematiquement :
- -ain/-eval, Gal-/Thib- → Ardrainic
- -tz/-enc/-esc, Esc-/Rai-/Oiss- → Sordrenic
- Ll-/Rh-/Gw-, -wyn/-wen/-ydd → Armonorican
- -us/-ius → Moran
- Wulf-/Sig-/Grim-, -wald/-mar/-mund → Torrent
- -oush/-azd, Tig-/Hov- → Hravevi

### Format de sortie
Presente sous forme de tableau clair. Je valide, puis tu sauvegardes dans :
→ `names/<LANGUE>/adn_phonetique.txt`

**Attends mon OK avant de continuer.**

---

# ETAPE 4 — GENERATION DES NOMS

Genere les noms de base. Les regles ci-dessous sont des GARDE-FOUS, pas des moules rigides.

### Garde-fous (les seules regles dures)
1. **2-3 syllabes max** — jamais 4+
2. **Pas de clusters consonantiques lourds** (-ndr-, -mpr-, -nguerr-)
3. **Feminins avec identite propre** : PAS masculin + "e"
4. **Non-recouvrement** : aucun nom ne doit pouvoir etre confondu avec une autre langue d'Etra

### Esprit du pool
Les attaques et terminaisons PEUVENT et DOIVENT se repeter — c'est ce qui donne son identite a une langue (comme J- revient dans Jean, Jacques, Julien, Jerome en francais). Ce qui compte c'est que le pool sonne VIVANT et NATUREL, pas qu'il respecte des quotas.

Le pool doit contenir de la variete naturelle, pas que des composes nobles :
- **Composes** (Attaque+Terminaison) : la majorite, c'est le coeur du systeme
- **Courts/bruts** (1-2 syllabes, noms du peuple) : Karl, Dirk, Garm, Bren
- **Organiques** (sonnent naturels, pas decomposables) : Aldric, Lothen
- **Communs** (equivalents fantasy de Jean/Pierre) : prenoms du quotidien

Adapter les proportions a la culture (montagnards = plus de courts, cour royale = plus de composes, etc.).

### Objectifs
| Categorie | Objectif |
|-----------|----------|
| Prenoms masculins | 50-70 |
| Prenoms feminins | 35-55 |
| Dynasties | 20-30 (pas que toponymiques — aussi heroiques, totems, titres) |
| Roturiers | 25-50 (pas que metiers — aussi nature, lieux, traits) |

### Presentation
Presente les noms par categorie thematique (noble, militaire, court/commun, etc.).

**Je valide ou corrige. On peut faire plusieurs tours.** Quand j'approuve, sauvegarde dans :
→ `names/<LANGUE>/base_names.txt`

---

# ETAPE 5 — AUDIT QUALITE

**ETAPE CRITIQUE — ne pas sauter.**

Analyse le pool genere a l'etape 4 et produis un rapport honnete :

### 5a. Vue d'ensemble du pool
- Combien de noms par categorie (M/F/dyn/low)
- Le pool est-il varie ? (courts + longs + organiques, pas que des composes)
- Les roturiers sont-ils varies ? (pas que des metiers)
- Les dynasties sont-elles variees ? (pas que toponymiques)

### 5b. Test de l'oreille
- Des noms qui sonnent trop mecaniques ? (Attaque+Suffix sans ame)
- Des noms trop proches entre eux ? (risque de confusion en jeu)
- Des noms qui pourraient etre confondus avec une AUTRE langue d'Etra ?

### 5c. Identites culturelles
Pour chaque sous-culture/dialecte prevu, est-ce que le pool de base couvre son style ?
Ex : si un dialecte est "maritime, rude, tronque" — est-ce qu'il y a assez de noms courts qui se pretent bien a la troncature ?
Est-ce qu'une sous-culture a besoin de noms propres que les transformations seules ne peuvent pas creer ?

### 5d. Ce qui manque (propositions libres)
Liste ce que le pool ne couvre pas encore. Exemples possibles :
- Noms composes (prenom+prenom pour la noblesse)
- Substrat vetusien / archaique pour les vieilles cultures
- Identite specifique d'une sous-culture
- Noms communs du quotidien
- Roturiers bases sur nature/lieux/traits
- Etc. — propose tout ce qui te semble pertinent

**Presente le rapport. On discute, on corrige le pool si besoin.** Quand on est satisfait :
→ Mettre a jour `names/<LANGUE>/base_names.txt` avec les corrections
→ Sauvegarder le rapport dans `names/<LANGUE>/audit.md`

---

# ETAPE 6 — SUBSTRAT RACIAL (si applicable)

Consulte `project_proto_languages.md` et `project_naming_method.md`.

- **Humains purs** : passe a l'etape 7
- **Elfes** : ajouter ~15-25% noms proto-elfiques FILTRES par la phonetique locale
- **Giantsborn** : ajouter ~15-25% noms proto-geants FILTRES par la phonetique locale
- **Ratfolk/Tieflings/Aasimar** : absorbent la culture locale. Appliquer un leger twist phonetique (sifflant/sombre/lumineux)
- **Culture-pont** (ex: Lutin) : mix de 2 langues + substrat proto

Les noms proto ne sont JAMAIS utilises purs — ils sont FILTRES par les terminaisons/consonnes locales.

**Attends mon OK.**

---

# ETAPE 7 — REGLES DIALECTALES

Pour chaque dialecte prevu (cf. `project_dialect_plan.md`), definis :
- Le **twist phonetique** (decalage voyelles, durcissement consonnes, etc.)
- Les **transformations par type de terminaison**
- 5+ **exemples** de transformation
- Le **prefixe dynastique** si applicable
- **Ce qui rend ce dialecte unique** (pas juste des transformations mecaniques — quelle est l'identite ?)

### Format de sortie (par dialecte)
```
<NOM_DIALECTE> (<culture assignee>)
Identite : <qu'est-ce qui rend cette culture specifique, en 1 phrase>
Style : <5 mots>
Voyelles : <transformations>
Consonnes : <transformations>
Terminaisons M : <A→B, C→D>
Terminaisons F : <A→B, C→D>
Prefixe dynastique : <si applicable>
Noms propres au dialecte : <noms qui n'existent que dans ce dialecte, si pertinent>
Exemples : NomBase → NomTransforme (x5 minimum)
```

### Points a verifier
- Est-ce que chaque dialecte est DISTINCT des autres a l'oreille ?
- Est-ce que la parente avec la langue mere reste perceptible ?
- Est-ce que les transformations produisent des noms PRONONÇABLES ?
- Est-ce qu'un dialecte a besoin de noms propres en plus des transformations ?
  (ex: Thaurfolk a besoin de prenoms scandinaves, pas juste des transforms du pool germanique)

**Je valide.** Quand j'approuve, sauvegarde dans :
→ `names/<LANGUE>/dialect_rules.txt`

---

# ETAPE 8 — AUDIT CROSS-LANGUE

Verifie la coherence avec les autres langues d'Etra :

### 8a. Non-recouvrement
Lis les `adn_phonetique.txt` des AUTRES langues dans `names/*/`.
Verifie qu'aucun nom genere ne pourrait etre confondu avec une autre langue.

### 8b. Cultures frontalieres
Pour les cultures a la frontiere de 2 zones linguistiques :
- Est-ce que leurs noms refletent l'influence du voisin ?
- Est-ce qu'on retrouve des emprunts logiques ?

### 8c. Sync check
Verifie que tous les noms de `base_names.txt` sont coherents avec `adn_phonetique.txt`.
Signaler tout nom qui viole les regles phonetiques definies.

**Presente le resultat. On corrige si besoin.**

---

# ETAPE 9 — SAUVEGARDE FINALE

Sauvegarde l'etat complet. Cette etape est OBLIGATOIRE, meme si on n'a pas fini toutes les etapes.

### 9a. STATUS.md
```markdown
# <Langue> — Status

## Pipeline
- [x/] Etape 1 — Identification : <resume>
- [x/] Etape 2 — Geographie : <resume>
- [x/] Etape 3 — ADN phonetique : <resume>
- [x/] Etape 4 — Generation : <X>M + <X>F + <X>dyn + <X>low
- [x/] Etape 5 — Audit qualite : <resume des problemes trouves/corriges>
- [x/] Etape 6 — Substrat racial : <N/A ou resume>
- [x/] Etape 7 — Dialectes : <X>/<Y> crees
- [x/] Etape 8 — Audit cross-langue : <resume>
- [x/] Etape 9 — Sauvegarde : fait

## Chiffres
Prenoms M: XX | Prenoms F: XX | Dynasties: XX | Roturiers: XX | Dialectes: XX/YY

## Decisions prises
- <decision> — pourquoi : <raison>

## Problemes connus / points ouverts
- <si applicable>

## Prochaine action
- <quoi faire ensuite>
```
→ `names/<LANGUE>/STATUS.md`

### 9b. decisions.md
Toutes les decisions ET les choix rejetes :
- Choix d'inspiration et pourquoi
- Noms/approches rejetees et pourquoi
- Interactions avec d'autres langues
- Corrections faites suite a l'audit
- Notes pour la suite
→ `names/<LANGUE>/decisions.md`

### 9c. audit.md (si etape 5 atteinte)
Le rapport d'audit complet + les corrections appliquees.
→ `names/<LANGUE>/audit.md`

### 9d. Progression globale
Mets a jour le tableau dans `docs/PIPELINE.md` (section "Progression par langue").

---

# REGLES TRANSVERSALES

## Process
- **Valide avec moi a CHAQUE etape** — ne passe jamais a la suite sans mon OK
- Si tu as un doute ou une question, pose-la plutot que de deviner
- Si le contexte devient lourd, propose un `/handoff`
- **Sauvegarde TOUJOURS a l'etape 9**, meme si on s'arrete en cours de route

## Creativite vs regles
- Les regles de naming sont des GARDE-FOUS, pas des moules
- Si un nom sonne bien mais ne suit pas exactement le schema Attaque+Terminaison, c'est OK
- Les noms organiques/courts/irreguliers donnent de la VIE au pool
- Propose des idees meme si elles sortent du cadre — je dirai non si ca va trop loin
- Chaque culture a une IDENTITE, pas juste des transformations phonetiques

## Fichiers
- **Langue des fichiers du mod** : anglais (commentaires, noms de variables)
- **Discussions** : en francais
- **Ne modifie PAS les fichiers du submod** (`mod/`) — ca se fait dans une etape separee
```

---

## Comment utiliser ce prompt

1. Ouvre une **nouvelle conv** Claude Code sur le repo `Etna/`
2. Colle le prompt ci-dessus en remplacant `<LANGUE>` par la langue cible
3. Claude lit tout le contexte, te dit ou on en est, et demarre a la bonne etape
4. Vous avancez etape par etape avec validation a chaque fois
5. A la fin (ou si tu t'arretes en cours), tout est sauvegarde dans `names/<LANGUE>/`

### Pour reprendre une langue deja commencee
Meme prompt. Claude lira le `STATUS.md` et reprendra a la bonne etape.

### Pour l'etape finale (ecriture dans le submod)
Ca se fait dans une conv separee une fois TOUTES les langues audites. Prompt :
```
Lis TOUS les names/*/STATUS.md et names/*/audit.md.
Verifie la coherence globale entre toutes les langues.
Puis ecris les noms dans le submod :
- mod/in_game/common/languages/02_etra_names_patch.txt (INJECT ou REPLACE)
- mod/in_game/common/cultures/02_etra_cultures_patch.txt (dialectes)
- mod/main_menu/localization/english/etra_custom_names_l_english.yml (variantes)
Mets a jour docs/CHANGELOG.md.
```
