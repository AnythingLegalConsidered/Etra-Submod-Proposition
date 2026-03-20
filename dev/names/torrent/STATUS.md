# Torrentian — Status

## Pipeline
- [x] Etape 1 — Identification : Germanique, 17 cultures (humains + tieflings + ratfolk + aasimar + elfes)
- [x] Etape 2 — Geographie : Nord maritime a montagnes sud, heartland central
- [x] Etape 3 — ADN phonetique : Wulf-/Sig-/Grim-/Skor-/Thar-, -wald/-mar/-mund/-varn/-gust
- [x] Etape 4 — Generation : ~108M + ~78F base + mini-pools + 98dyn + 43low
- [x] Etape 5 — Audit qualite : Sig-/Grim-/Drak- surutilises (corriges), Ros-→Rost-, Aldwin→Aldven, +8F organiques pour ratio. 2e pass : Grimmorn→Friedgust (Grim- 5→4), Velkmar→Velkvarn (confusion Volkmar)
- [x] Etape 6 — Substrat racial : Erlfolk 8M+6F proto-elfique germanise. Tieflings/Ratfolk/Himmelskind absorbent dialecte local.
- [x] Etape 7 — Dialectes : 13/13 humains formalises dans dialect_rules.txt (+ 4 non-humains = substrat)
- [x] Etape 8 — Audit cross-langue : OK. Attaques partagees (Arn-/Ger-/Ald-/Brun-) differenciees par terminaisons. 2e pass : Baldrik→Baldgar (confusion Aldric ardrainic)
- [x] Etape 9 — Sauvegarde : fait

## Chiffres
Prenoms M: ~108 base + 93 mini-pools + 15 vetusien + 8 proto-elfique = ~224
Prenoms F: ~78 base + 54 mini-pools + 10 vetusien + 6 proto-elfique = ~148
Dynasties: ~98 (von/van/zu/af/de/aun/-ski/-i/-bek)
Roturiers: 43
Dialectes: 13 humains + 4 non-humains (substrat)

## Decisions prises
- Structure Attaque+Terminaison 2 morphemes + variantes organiques/courts/3-morph — pourquoi : eviter pool trop mecanique
- 20 attaques classiques + 10 fantasy (Skor-, Thar-, Drak-, etc.) — pourquoi : touche originale tout en gardant le feel germanique
- Attaques feminines exclusives (Rost-, Sol-, Lind-, Heil-, Isen-, Minn-, Aud-) — pourquoi : feminins avec identite propre
- Prefixes dynastiques par dialecte (von/van/zu/af/-ski/-i/-bek/aun) — pourquoi : chaque culture reconnaissable a la dynastie
- Appavin deplace vers ardrainic — pourquoi : geographiquement plus francophone, style franco-alpin
- Ros- → Rost- — pourquoi : conflit avec ardrainic qui utilise Ros-
- Aldwin → Aldven — pourquoi : -win trop proche de -wyn armonorican
- Grimmorn → Friedgust — pourquoi : Grim- a 5 utilisations M (max 4)
- Velkmar → Velkvarn — pourquoi : trop proche de Volkmar a l'oreille
- Baldrik → Baldgar — pourquoi : cross-langue, -rik trop proche de -ric (Aldric ardrainic)
- PAS de prenoms composes fantasy — pourquoi : incoherent avec la couche archaique des noms inventes
- Non-humains = systeme substrat (pas de dialecte propre) — pourquoi : coherent avec project_proto_languages.md
- Mini-pools pour Borrikan/Tyelkian/Chesmeker/Thaurfolk/Stedeling — pourquoi : cultures trop distinctes pour de simples transforms
- Substrat vetusien partage — pourquoi : lier les 4 cultures d'habitants originels

## Problemes connus / points ouverts
- Sorlkol et Bonwesforian n'ont que des transforms simples (pas de mini-pool) — acceptable pour des petites cultures
- Influence Freeholder (vulgar moran) sur Sorlkol sud pas encore modelisee (vulgar_moran pas fait)
- Influence Hravevi sur Chesmeker est pas encore modelisee (hravevi pas fait)
- Le fichier adn_phonetique.txt n'a pas ete cree comme fichier separe (info dans memory + base_names.txt)

## Prochaine action
- Creer adn_phonetique.txt si necessaire pour coherence avec les autres langues
- Ecriture dans le submod (conversion name_xxx, localisation, cultures patch) — a faire quand toutes les langues seront audites
