# Pipeline de Creation de Noms — Applicable a toute langue

## Vue d'ensemble

Pour chaque langue d'Etra, on suit ce pipeline en 9 etapes.
Chaque etape produit un livrable dans `names/<langue>/`.
Le prompt standard est dans `_specs/PROMPT_PIPELINE.md`.

---

## Etape 1 — Identification de la langue

**Output** : Fiche d'identite → presente au user

- Quelle langue ? Quelles cultures la parlent ?
- Quelle(s) race(s) ? (humain, elfe, ratfolk, tiefling, aasimar, giantsborn, undead)
- Quels voisins linguistiques ?
- Quels dialectes prevus ? (cf. memory/project_dialect_plan.md)
- Quels noms existent deja dans le mod original ?

---

## Etape 2 — Analyse geographique

**Output** : Profil geo par culture → presente au user

Pour chaque culture, determiner terrain, climat, dev, position.
Le profil geo determine le STYLE des noms :

| Terrain | Impact |
|---------|--------|
| Plaines riches | Noms longs, raffines, composes |
| Montagnes | Noms courts, archaiques, conservateurs |
| Cotes | Noms rudes, tronques, marins |
| Forets denses | Noms profonds, sombres, sylvestres |
| Frontiere | Noms hybrides, emprunts aux voisins |
| Pauvre/isole | Noms simples, peu de dynasties |
| Villes/commerce | Noms pratiques, raccourcis, cosmopolites |

---

## Etape 3 — ADN phonetique

**Output** : → `names/<langue>/adn_phonetique.txt`

Pour chaque langue, definir :
- **Attaques** (15-25) dont 3+ EXCLUSIVES
- **Terminaisons M** (8-12) dont 2+ EXCLUSIVES
- **Terminaisons F** (8-12) dont 2+ EXCLUSIVES
- **Voyelles caracteristiques**
- **Sons interdits** (reserves a d'autres langues)
- Verification de non-recouvrement (matrice dans memory/project_naming_method.md)

---

## Etape 4 — Generation des noms de base

**Output** : → `names/<langue>/base_names.txt`

### Objectifs
| Categorie | Objectif | Notes |
|-----------|----------|-------|
| Prenoms masculins | 50-70 | Mix noble/commun/court |
| Prenoms feminins | 40-55 | Equilibre, identite propre |
| Dynasties | 20-30 | Toponymiques + heroiques + totems + titres |
| Roturiers | 30-50 | Metiers + nature + lieux + traits |

### Garde-fous (regles dures)
1. 2-3 syllabes max
2. Pas de clusters consonantiques lourds
3. Feminins autonomes (pas masculin + "e")
4. Non-recouvrement entre langues
5. **Max 5 noms par terminaison** (marqueurs exclusifs inclus)
6. **Max 3 noms par attaque** (M+F combines)
7. **Pas de serie** : interdit d'avoir 3+ noms qui ne different que par la terminaison

### Quotas de diversite
| Type | Minimum | Description |
|------|---------|-------------|
| Organiques/standalone | **25%** | Noms pas decomposables en Attaque+Terminaison. Sonnent comme s'ils existaient depuis toujours. |
| Memorables | **10%** | Courts, surprenants, sonorite forte. Le joueur les retient apres une partie. |
| Formule classique | **max 50%** | Attaque+Terminaison standard. Le coeur identitaire de la langue, mais plus la majorite. |
| Communs/uses | **15%** | Noms raccourcis par l'usage, diminutifs, formes populaires. |

### Esprit du pool
Le pool doit sonner VIVANT et MEMORABLE. Chaque nom doit pouvoir etre le nom d'un personnage important.
Un bon pool = quand on lit la liste, on ne voit pas la formule derriere.
Les marqueurs exclusifs donnent l'identite, mais ne doivent pas dominer.

---

## Etape 5 — Audit qualite

**Output** : → `names/<langue>/audit.md`

Analyse critique du pool genere :
- **Test de l'oreille** : noms mecaniques, trop proches entre eux, confondables avec une autre langue
- **Variete** : le pool sonne-t-il vivant ? (pas que des composes nobles)
- **Identites culturelles** : chaque sous-culture est-elle couverte par le pool de base ?
- **Ce qui manque** : propositions libres (noms courts, composes, substrats, roturiers varies, etc.)

---

## Etape 6 — Substrat racial (si non-humain)

**Output** : noms supplementaires dans `base_names.txt` ou fichiers dedies

- Elfes : ~15-25% proto-elfique FILTRE par la phonetique locale
- Giantsborn : ~15-25% proto-geant FILTRE par la phonetique locale
- Ratfolk/Tieflings/Aasimar : twist phonetique leger
- Culture-pont (Lutin) : mix de 2 langues + substrat proto

Les noms proto ne sont JAMAIS purs — toujours filtres.

---

## Etape 7 — Regles dialectales

**Output** : → `names/<langue>/dialect_rules.txt`

Pour chaque dialecte :
- Twist phonetique (voyelles, consonnes, terminaisons)
- Prefixe dynastique si applicable
- Identite culturelle (pas juste des transformations mecaniques)
- Noms propres au dialecte si necessaire
- 5+ exemples de transformation

Verifier : distinct des autres dialectes ? Parente perceptible ? Prononçable ?

---

## Etape 8 — Audit cross-langue

**Output** : ajout dans `names/<langue>/audit.md`

- Non-recouvrement avec les autres langues (lire les autres `adn_phonetique.txt`)
- Cultures frontalieres : emprunts logiques ?
- Sync check : tous les noms respectent l'ADN defini ?

---

## Etape 9 — Sauvegarde finale

**Output** : mise a jour de TOUS les fichiers

- `names/<langue>/STATUS.md` — etat complet
- `names/<langue>/decisions.md` — choix + rejets + raisons
- `names/<langue>/audit.md` — rapport qualite
- `docs/PIPELINE.md` — tableau de progression

---

## Checklist rapide

```
[ ] 1. Fiche d'identite
[ ] 2. Profil geographique
[ ] 3. ADN phonetique → adn_phonetique.txt
[ ] 4. Generation des noms → base_names.txt
[ ] 5. Audit qualite → audit.md
[ ] 6. Substrat racial (si applicable)
[ ] 7. Regles dialectales → dialect_rules.txt
[ ] 8. Audit cross-langue → audit.md
[ ] 9. Sauvegarde finale → STATUS.md + decisions.md
```

---

## Fichiers par langue

```
names/<langue>/
├── STATUS.md              ← etat pipeline + decisions + prochaine action
├── adn_phonetique.txt     ← ADN sonore (etape 3)
├── base_names.txt         ← pool de noms (etape 4)
├── audit.md               ← rapport qualite + cross-langue (etapes 5+8)
├── dialect_rules.txt      ← regles dialectales (etape 7)
├── decisions.md           ← journal des decisions et rejets (etape 9)
└── [substrat].txt         ← noms proto-raciaux si applicable (etape 6)
```

---

## Progression par langue

| Langue | Etape | Status |
|--------|-------|--------|
| Ardrainic | 7/9* | 80M+59F+25dyn+32low, 10 dialectes, submod ecrit. Manque : audit qualite + audit cross |
| Torrent | **9/9** | ~224M+~148F+98dyn+43low, 13 dialectes + 4 substrats. Audit qualite + cross-langue fait. |
| Armonorican | **9/9** | 79M+59F+30dyn+38low, 2 dialectes. Audit qualite + cross-langue fait. Submod a resync post-audit. |
| Sordrenic | **9/9** | 74M+59F+25dyn+30low, 4 dialectes + substrats. Audit qualite + cross-langue fait. Variants dialectales a regenerer post-audit. |
| Moran | **9/9** | 57M+47F+25dyn+40low (nouveaux) + existants mod. 5 dialectes chronologiques. Audit qualite + cross-langue fait. |
| Vulgar Moran | 0/9 | Pas commence |
| Hravevi | **9/9** | 67M+60F+24dyn+35low, 0 dialecte. Armenien-fantasy + proto-geant brut. Audit qualite + cross-langue fait. |

*Les langues "DONE" ont ete faites avant l'ajout des etapes audit (5+8). Elles doivent passer l'audit retroactivement.
