# Changelog — Etra: Names & Cultures

## [0.2.0] - 2026-03-20

### Names & Languages — 7 languages, ~45 dialects, 5600+ names

#### Ardrainic (111M + 104F + 26 dynasties + 32 lowborn, 10 dialects, 11 cultures)
- 111 custom male names (Thibeval, Lancelin, Galenor, Aldric, Corvain, Brisand...)
- 104 custom female names (Belisore, Alisande, Florelise, Nimue, Solene...)
- 26 dynasties including **de_Wryn** (Daqueland/Wayne reference) with 10 dialect variants
- 32 lowborn names (Bauvel, Corvais, Brivault, Lanthois...)
- 10 dialects: Sittadellian, Aullerican, Aloisoise, Caprainois, Pwasciards, Serenish, Berenguer, Draquatin, Chevallois, Appavin
- 2235 localization entries (252 base + 1983 variants)

#### Torrentian (110M + 78F + 39 dynasties + 39 lowborn, 17 dialects, 18 cultures)
- Most complex language: 17 human dialects + 4 non-human substrates
- Mini-pools and proto-languages (elvish, giant)
- 1714 localization entries

#### Sordrenic (63M + 59F + 26 dynasties + 30 lowborn, 3 dialects, 3 cultures)
- Curated Occitan/Provencal pool (max 3 names per termination, 45-50% wildcards)
- 3 dialects: Stone, Lutin, Pantagrin
- 26 dynasties including **de_Vrintz** (sordrenicized Wryn) with 3 variants (Vroncq, Vrientz, Vrenc)
- 245 localization entries

#### Moran (66M + 55F + 25 dynasties + 40 lowborn, 4 dialects, 4 cultures)
- Fantasy-Latin style (Aeternus, Caelinus, Mortivex, Ossivax...)
- Added on top of existing base mod names
- 336 localization entries

#### Vulgar Moran (67M + 51F + 31 dynasties + 45 lowborn, 7 dialects, 7 cultures)
- Corrupted Latin / Italian-influenced lingua franca (Aurelvan, Valoren, Casperian...)
- 7 dialects including **Rattolini** with exclusive pool of 13 names (Gnavio, Scherzs, Vicitz, Rosci...)
- 580 localization entries

#### Hravevi (67M + 62F + 24 dynasties + 35 lowborn, 0 dialects)
- Proto-giant / Armenian blend (standalone pool, no dialects)
- 130 localization entries

#### Armonorican (79M + 55F + 30 dynasties + 38 lowborn, 1 dialect)
- Quality-curated Breton-fantasy pool
- 253 localization entries

### Character Overrides — Pantagrins

Replaced Norse/English names with Sordrenic-Occitan names fitting the giant culture:

| Before | After |
|--------|-------|
| Alric | Aldronc |
| Anna | Gronnda |
| John | Jornac |
| Sigurd | Sigorntz |
| Magnus | Magnortz |
| Canute | Canornc |

Pantagrin dynasties translated into Occitan/Provencal/Catalan:

| Before | After | Etymology |
|--------|-------|-----------|
| Sunbreaker | Destrazol | destrar (destroy) + sol (sun) |
| Last Oath | Darnegramen | darnier (last) + sagrament (oath) |
| Stonewake | Troquevail | trocar (awaken) + vailh (stone) |
| Thunderlord | Tronsenor | tron (thunder) + senhor (lord) |
| Strongjaw | Forszgalta | forsz (strong) + galta (jaw) |

Implemented via `.pantagrin_sordrenic_dialect` localization variants — only affects Pantagrin characters.

### Character Overrides — Rattolini

Replaced inconsistent names (Latin/Norse/alien mix) with unified Italian-vermin style:

| Before | After |
|--------|-------|
| Gnavius | Gnavio |
| Vernacius | Vernaci |
| Cecile | Cecisca |
| Sheq | Scherzs |
| Vikkit | Vicitz |
| Kvos | Voserro |
| Vem | Vermic |
| Rocdit | Rosci |
| Jex | Jessaros |
| Djigren | Ginoz |
| Rikket | Rissto |
| Zrindez | Strinaci |
| Mavvis | Mavisci |

- Ratticar (founder) keeps original name
- Implemented via `.rattolini_dialect` — province names remain unchanged
- 13 exclusive names added to Rattolini pool via `extra_male`/`extra_female`

### Country & Province Overrides — Rattolini

Rat countries renamed to match new character names:

| Tag | Before | After |
|-----|--------|-------|
| A13 | Rattopaese | Rattopaese (unchanged) |
| A15 | Jex | Jessaros |
| A16 | Vikkit | Vicitz |
| A17 | Kvos | Voserro |
| A19 | Rikkek | Rissto |
| A20 | Mavvis | Mavisci |
| A21 | Zrindez | Strinaci |
| A22 | Rocdit | Rosci |
| A23 | Djigren | Ginoz |

Province renamed: Kvosthovo -> Voserrothovo

### Pipeline & Infrastructure
- **Generator fix**: correct parsing of `# DYNASTIES` section in `dialect_variants.txt` files (previously mixed with male name overrides)
- **`dev/overrides/` system**: files in `dev/overrides/` are automatically copied into the submod during build — allows adding custom files (loc overrides, cultures) without losing them on rebuild
- **Dynasty dialect variants fix**: `overrides_dyn` now correctly loaded from manual variant files

### Global Stats
- **7 languages** completed
- **~45 dialects** with automatic transformations
- **5600+ unique names** (first names + dynasties + lowborn + variants)
- **5582 localization entries** total
- **21 files** in the submod
- Compatible with Etra v0.05+

---

## [0.1.0] - 2026-03-19

### Initial Release
- Submod structure created
- 7 languages implemented with automatic generation pipeline
- Naming methodology established (2-3 syllables, attack diversity, autonomous feminine names)
- Exclusive markers per language to prevent cross-language overlap
