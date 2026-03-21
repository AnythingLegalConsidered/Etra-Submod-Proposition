# Ardrainic — Ruler Titles (Monarchy)
# Inspiration: Old French medieval + Arthurian
# Base dialect: Ardrainien (standard court French)

## Design Rules
# - Titles are VOCABULARY words, not name-constructed (no systematic Attaque+Terminaison)
# - Base forms use real Old French (Empereor, Reis, Dus, Cuens) with light Ardrainic twist
# - Country/polity names use Ardrainic markers (-ain, -eval, -vain) = formal/administrative register
# - Feminine titles use Ardrainic F markers (-ore, -nore) OR authentic Old French forms
# - Dialect shifts follow the SAME rules as name dialect transforms (see config.yaml)

## Base Titles (Ardrainien = standard)

| Rank    | Country     | Ruler M    | Ruler F     |
|---------|-------------|------------|-------------|
| Empire  | Emperance   | Empereor   | Empereis    |
| Kingdom | Renoumain   | Reis       | Reinore     |
| Duchy   | Ducheval    | Dus        | Ducesse     |
| County  | Comtevain   | Cuens      | Contevore   |

### Etymology
- Empereor / Empereis: Old French direct (empereor XIIe siecle, empereis = feminine)
- Reis: Old French "reis/rois" (cas sujet XIIe). Short, royal, archaic.
- Reinore: reine + -ore (Ardrainic F marker, like Belisore, Eilenore)
- Dus: Old French real for "duc". Brut, court.
- Ducesse: Old French archaic (not modern "duchesse" — shorter, more archaic)
- Cuens: Old French "cuens" (cas sujet de comte). Immediately exotic.
- Contevore: conte (cas regime) + -ore (Ardrainic F marker)
- Country names: Emperance, Renoumain (-ain), Ducheval (-eval exclusive), Comtevain (-vain, au-vowel)

## Dialect Variants

### EMPIRE

| Dialect        | Emperor    | Empress      | Shift applied              |
|----------------|------------|--------------|----------------------------|
| Ardrainien     | Empereor   | Empereis     | base                       |
| Sittadellian   | Empereort  | Emperist     | hardening -or→-ort, -eis→-ist |
| Aullerican     | Empereour  | Emperaeis    | diphtongues ou, aei        |
| Aloisoise      | Empereoren | Empereiser   | rallongement -er/-en       |
| Caprainois     | Emperorel  | Empereil     | liquide -orel, -eil        |
| Pwasciards     | Empero     | Emperi       | truncation maritime        |
| Serenish       | Emporor    | Emporois     | e→o archaisant             |
| Berenguer      | Emperort   | Emperein     | germanique -ort, -ein      |
| Draquatin      | Emperoun   | Emperouna    | gascon -oun/-ouna          |
| Chevallois     | Empereourt | Emperoise    | chevaleresque -ourt, -oise |
| Appavin        | Emperoret  | Empereiset   | alpin diminutif -et/-eset  |

### KINGDOM

| Dialect        | King       | Queen        | Shift applied              |
|----------------|------------|--------------|----------------------------|
| Ardrainien     | Reis       | Reinore      | base                       |
| Sittadellian   | Reist      | Reinort      | hardening -t               |
| Aullerican     | Raeis      | Reinoer      | diphtongue aei, oer        |
| Aloisoise      | Reiser     | Reinoren     | rallongement -er/-en       |
| Caprainois     | Rais       | Reinorel     | adouci, liquide            |
| Pwasciards     | Re         | Reino        | truncation                 |
| Serenish       | Rois       | Reinor       | e→o (= real Old French!)   |
| Berenguer      | Rein       | Reinort      | germanique -ein            |
| Draquatin      | Rei        | Reinouna     | gascon                     |
| Chevallois     | Reault     | Reinourt     | chevaleresque -ault/-ourt  |
| Appavin        | Reit       | Reinoret     | alpin -et                  |

### DUCHY

| Dialect        | Duke       | Duchess      | Shift applied              |
|----------------|------------|--------------|----------------------------|
| Ardrainien     | Dus        | Ducesse      | base                       |
| Sittadellian   | Dust       | Ducest       | hardening -t               |
| Aullerican     | Dues       | Ducaesse     | diphtongue ue, ae          |
| Aloisoise      | Duser      | Ducessen     | rallongement               |
| Caprainois     | Duis       | Ducelle      | liquide -elle              |
| Pwasciards     | Du         | Duces        | truncation                 |
| Serenish       | Dus        | Ducosse      | e→o in -esse               |
| Berenguer      | Duz        | Ducenn       | germanique -z, -enn        |
| Draquatin      | Dous       | Ducessa      | gascon -ou, -a             |
| Chevallois     | Dault      | Ducoise      | chevaleresque -ault, -oise |
| Appavin        | Duet       | Ducesset     | alpin -et                  |

### COUNTY

| Dialect        | Count      | Countess     | Shift applied              |
|----------------|------------|--------------|----------------------------|
| Ardrainien     | Cuens      | Contevore    | base                       |
| Sittadellian   | Cuent      | Contevort    | hardening -t               |
| Aullerican     | Cuaens     | Contevoer    | diphtongue ua, oer         |
| Aloisoise      | Cuenser    | Contevoren   | rallongement               |
| Caprainois     | Cuien      | Contevorel   | liquide -ien, -orel        |
| Pwasciards     | Cuen       | Contevo      | truncation                 |
| Serenish       | Cuons      | Contevor     | e→o                        |
| Berenguer      | Cuenn      | Contevort    | germanique -enn, -ort      |
| Draquatin      | Counes     | Contevouna   | gascon -ounes, -ouna       |
| Chevallois     | Cuault     | Contevourt   | chevaleresque -ault, -ourt |
| Appavin        | Cuet       | Contevoret   | alpin -et                  |

## Dialect Shift Summary

| Dialect      | Identity                | Key phonetic shifts                        |
|--------------|-------------------------|--------------------------------------------|
| Sittadellian | Picardie/Normandie, dur | -or→-ort, -eis→-ist, final hardening       |
| Aullerican   | Normandie/Bretagne      | diphtongues ae/oe/ue, vowel stretching     |
| Aloisoise    | Lorraine/Champagne      | rallongement systematique en -er/-en       |
| Caprainois   | Loire/Anjou, doux       | adoucissement, liquides -el/-orel/-eil     |
| Pwasciards   | Poitou/Vendee, maritime | truncation brutale des finales             |
| Serenish     | Berry/Auvergne, montagne| e→o archaisant, formes conservatrices      |
| Berenguer    | Alsace, franco-germanique| -ein, -ort, -enn, -uz (contact Torrent)   |
| Draquatin    | Gascogne, gascon        | nasalisation -oun/-ouna, finales -a        |
| Chevallois   | Bourgogne, forestier    | -ault/-ourt partout, chevaleresque         |
| Appavin      | Alpes, franco-alpin     | diminutifs en -et/-eset, ex-Torrent        |
