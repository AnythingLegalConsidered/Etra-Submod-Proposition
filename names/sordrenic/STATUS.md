# Sordrenic — Status

## Pipeline
- [x] Etape 1 — Identification : Provencal+Occitan+Italien+Francais sud, 4 cultures (Salt/Stone Sordrenic + Lutin elfes + Pantagrins giantsborn)
- [x] Etape 2 — Geographie : Cote sud maritime (Salt), montagnes sud (Stone), foret centrale (Lutin), montagnes (Pantagrins)
- [x] Etape 3 — ADN phonetique : -tz/-enc/-esc, Esc-/Rai-/Oiss-, voyelles a/o. 41 attaques, 30 terminaisons M (18 struct + 12 souples), 26 terminaisons F (16 struct + 10 souples)
- [x] Etape 4 — Generation initiale : 74M + 59F + 25dyn + 30low
- [x] Etape 5 — Audit qualite : -antz reduit, -aldo reduit, organiques enrichis
- [x] Etape 5b — Curation qualite : pool taille et diversifie. Coupe des doublons sonores (-enc x8, -esc x9, -orn x7 → max 3 par terminaison). Ajout 18 wildcards M + 22 wildcards F avec profils uniques. Ratio organiques/wildcards monte a ~45-50%.
- [x] Etape 6 — Substrat racial : Lutin = 35-40% sordrenic + 30-35% ardrainic + 15% proto-elf filtre sud + 15% proto-elf filtre nord. Pantagrins = 70-75% sordrenic + 25-30% proto-geant sordrenicise.
- [x] Etape 7 — Dialectes : 4/4 regles definies (salt=default, stone=dur, lutin=adouci, pantagrin=alourdi). Variants a regenerer post-curation.
- [x] Etape 8 — Audit cross-langue : aucun conflit majeur.
- [ ] Etape 9 — Regenerer dialect_variants.txt avec le pool curate
- [ ] Etape 10 — Creer generate_sordrenic.py et generer le submod

## Chiffres
Prenoms M: 63 | Prenoms F: 59 | Dynasties: 25 | Roturiers: 30 | Dialectes: 4/4 (regles)

## Fichiers
- `adn_phonetique.txt` — ADN complet + terminaisons souples + regles dialectales
- `base_names.txt` — pool curate post-curation (63M+59F+25dyn+30low)
- `config.yaml` — config YAML pour le script de generation
- `dialect_variants.txt` — table de transformation 4 dialectes (PRE-curation, a regenerer)
- `lutin_proto_elvish.txt` — 20M + 16F proto-elfiques filtres (sordrenic + ardrainic)
- `pantagrin_proto_giant.txt` — 16M + 12F proto-geants sordrenicises
- `audit.md` — rapport d'audit initial + corrections appliquees
- `decisions.md` — toutes les decisions et choix rejetes

## Decisions prises
- Inspiration provencal + occitan + italien + francais du sud
- Marqueurs exclusifs : -tz/-enc/-esc (terminaisons), Esc-/Rai-/Oiss- (attaques)
- Salt = cotier/maritime (base), Stone = montagnard/dur (e→o, consonnes durcies)
- Lutin = culture-pont triple (35-40% sordr + 30-35% ardr + 15% proto-elf S + 15% proto-elf N)
- Pantagrins = giantsborn lourds (70-75% sordrenic + 25-30% proto-geant sordrenicise)
- Proto-geant = proto-armenien (partage avec Hravevi)
- Proto-elfique = blend gaelique+finnois+sanskrit
- Noms proto JAMAIS purs — toujours filtres par la phonetique locale
- **Curation (session 4)** : max 3 noms par terminaison, 45-50% wildcards/organiques, nouveaux sons (-el, -ac, -au, -iel, -eron, -ane, -ene, -ine, -elle, -ire, -iera)
- **Nouvelles attaques** : Folc-, Rost-, Alb-, Dalm-, Sauv-, Barr-

## Problemes connus / points ouverts
- `dialect_variants.txt` est PRE-curation — doit etre regenere avec le pool curate
- Volcain (roturier) utilise -ain qui est marqueur ardrainic — flag mineur
- Pas encore de script generate_sordrenic.py
- Pas encore d'ecriture dans le submod

## Prochaine action
- Regenerer `dialect_variants.txt` avec le pool curate
- Creer `generate_sordrenic.py` (comme generate_armonorican.py)
- Generer le submod
