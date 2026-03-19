# Sordrenic — Decisions

## Choix d'inspiration
- **Retenu** : Provencal + Occitan + Italien + Francais du sud
  - Pourquoi : le groupe culturel est "Greco-Occitan", zone sud-ouest d'Etra, climat mediterraneen
- **Rejete** : Grec pur — trop de recouvrement avec le label "Greco-Occitan" deja couvert par le melange
- **Rejete** : Espagnol/Catalan — trop proche du reel, risque de noms reconnaissables

## Marqueurs exclusifs
- **Retenu** : -tz, -enc, -esc (terminaisons), Esc-, Rai-, Oiss- (attaques)
  - Pourquoi : -tz est LE son occitan par excellence, immediatement reconnaissable
  - Verifie contre la matrice : aucun conflit avec les 6 autres langues

## Dialectes
- **Retenu** : 4 dialectes (salt/stone/lutin/pantagrin)
  - Salt = base standard
  - Stone = e→o + durcissement (montagnard)
  - Lutin = insertion "i" liquide (elfique adouci)
  - Pantagrin = a→o, e→o (geant alourdi)
- **Rejete** : plus de dialectes (ex: maritime vs interieur pour Salt) — pas assez de cultures pour justifier

## Systeme racial (decision majeure)
- **Retenu** : Absorption locale + substrat proto-racial filtre
  - Pourquoi : plus realiste que des noms raciaux purs, cree de la profondeur narrative
  - Lutin = 35-40% sordr + 30-35% ardr + 15% proto-elf S + 15% proto-elf N
  - Pantagrins = 70-75% sordr + 25-30% proto-geant sordrenicise
- **Rejete** : filtres raciaux purs (ancien systeme) — trop artificiel
- **Rejete** : absorption 100% (aucun substrat) — perte d'identite raciale
- **Note** : ratio initial etait 85/15, augmente a 70-75/25-30 a la demande du user

## Proto-langues
- **Retenu** : Proto-elfique = blend gaelique + finnois + sanskrit
  - Pourquoi : les 3 se completent (mystere + melodie + noblesse), distincts de toutes les langues d'Etra
- **Rejete** : Grec ancien pour proto-elfique — recouvrement avec Sordrenic
- **Rejete** : Georgien pour proto-elfique — reserve au proto-geant
- **Rejete** : Japonais ancien — detonne dans un setting europeen
- **Retenu** : Proto-geant = proto-armenien
  - Pourquoi : coherent avec Hravevi (armenien pur), les Pantagrins sont la branche absorbee
- **Note** : les noms proto sont TOUJOURS filtres par la phonetique locale (-dh→-tz, -oush→-otz, etc.)

## Lutin comme culture-pont
- **Retenu** : triple mix sordrenic + ardrainic + proto-elfique
  - Pourquoi : les Lutin vivent en zone ardrainic mais parlent sordrenic, et sont dans les 2 groupes culturels
- **Rejete** : 100% sordrenic — ignore la realite geographique (entoures par Ardrainic)

## Corrections audit
- **Corrige** : -antz de 20% → 8% (7 noms remplaces par -esc, -enc, -orn, organique)
- **Corrige** : -aldo de 9% → 3% (3 noms remplaces)
- **Corrige** : Castella → Castença (confusion espagnol reel)
- **Corrige** : Brunesc → Brunotz (confusion attaque Brun- avec ardrainic)
- **Corrige** : Saldorn → Saldosc (confusion sonorire germanique)
- **Ajoute** : 20 noms organiques (10M + 8F + 2 via remplacement)
- **Ajoute** : 9 noms courts/bruts (5M + 4F)
- **Ajoute** : 8 noms communs (5M + 3F)
- **Flag mineur** : Volcain (roturier) utilise -ain (marqueur ardrainic) — a trancher

## Notes pour la suite
- dialect_variants.txt doit etre regenere avec le pool post-audit
- Les noms organiques/courts/communs n'ont pas encore de regles de transformation dialectale definies
  - Proposition : les organiques se transforment de facon irreguliere (comme les noms reels)
  - Les courts restent identiques ou varient tres peu selon le dialecte
- Quand le submod sera ecrit, verifier que les cles name_xxx ne conflictent pas avec les noms existants du mod
