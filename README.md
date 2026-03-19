# Etra: Names & Cultures

A submod for [Etra: The New Age](https://steamcommunity.com/sharedfiles/filedetails/?id=3619896881), a total conversion fantasy mod for Europa Universalis V.

This submod replaces the generic placeholder names with **original fantasy names** for every culture in Etra, each with its own constructed dialect system producing regional variants.

## What it does

- **7 languages** with unique phonetic identities (exclusive prefixes, suffixes, forbidden sounds)
- **~45 dialects** — each culture gets its own dialect that transforms base names into regional variants
- **5,300+ localization entries**, **3,800+ dialect variants**
- Names designed to feel alive: a mix of composed, organic, short/common, and memorable names — not just mechanical prefix+suffix

### Languages at a glance

| Language | Inspiration | Names (M+F) | Dialects | Cultures |
|----------|------------|-------------|----------|----------|
| Ardrainic | French chivalric | 110M + 104F | 10 | Ardrainien, Sittadellian, Draquatin... |
| Torrentian | Germanic | 110M + 78F | 16 | Heuhian, Fullhorner, Naurmen, Thaurfolk... |
| Armonorican | Celtic/Welsh | 79M + 55F | 1 | Ebiam, Aggeuios |
| Sordrenic | Greco-Occitan | 73M + 59F | 3 | Salt/Stone Sordrenic, Lutin (elf), Pantagrin (giant) |
| Moran | Classical Latin | 66M + 55F | 4 | Early/High/Late/Novus Moran (undead) |
| Vulgar Moran | English/Italian | 67M + 51F | 7 | Venturian, Rovina, Rattolini (ratfolk)... |
| Hravevi | Armenian | 67M + 62F | 0 | Hravevi (giantsborn) |

## Installation

1. Subscribe to [Etra: The New Age](https://steamcommunity.com/sharedfiles/filedetails/?id=3619896881) on Steam Workshop
2. Download or clone this repo
3. Generate the mod files:
   ```bash
   pip install pyyaml
   python generate_mod.py --all
   ```
4. Deploy to your EU5 mod folder:
   ```bash
   python deploy.py
   ```
   This copies the generated files to `Documents/Paradox Interactive/Europa Universalis V/mod/etra-names-cultures/`
5. Enable the submod in the EU5 launcher

### Manual installation

If you prefer not to run the scripts, copy the contents of `output/mod/` directly to your EU5 mod folder.

## How names are built

Each language follows a **9-step pipeline** (documented in [docs/PIPELINE.md](docs/PIPELINE.md)):

1. **Identification** — map cultures, races, neighbors
2. **Geography** — terrain/climate influence on naming style (mountains = short archaic names, rich plains = long refined names, etc.)
3. **Phonetic DNA** — define exclusive attacks (prefixes), endings, forbidden sounds, vowel palette
4. **Name generation** — 50-70M, 35-55F, 20-30 dynasties, 25-50 commoner names per language
5. **Quality audit** — ear test, diversity check, cultural coverage
6. **Racial substrate** — proto-Elvish or proto-Giant filtered through local phonetics (for non-human cultures)
7. **Dialect rules** — phonetic shifts, suffix/prefix/replace transforms per culture
8. **Cross-language audit** — verify no overlap between languages
9. **Final save** — STATUS.md, decisions.md, audit.md

### Non-overlap matrix

Every language has **exclusive markers** that prevent confusion:

```
Ardrainic  : -ain/-eval, Gal-/Thib-/Lanc-
Torrentian : -wald/-mar/-mund, Wulf-/Sig-/Grim-
Armonorican: Ll-/Rh-/Gw-, -wyn/-wen/-ydd
Sordrenic  : -tz/-enc/-esc, Esc-/Rai-/Oiss-
Moran      : -us/-ius/-ox/-ex, Aeter-/Mort-/Nex-
Hravevi    : -oush/-azd/-avan, Tig-/Hov-/Art-
Vulgar Mor.: -avel/-oren/-iant, Aur-/Val-/Corv-
```

### Example: Ardrainic dialect variants

A base name like **Galenor** becomes:
- *Galenor* in Ardrainien (standard)
- *Galenoer* in Sittadellian (o→oe shift)
- *Galenaur* in Aullerican (Norman influence)
- *Gallanor* in Pwasciards (gemination)

## Project structure

```
names/                    # Creative work per language
  <language>/
    STATUS.md             # Pipeline progress & decisions
    adn_phonetique.txt    # Phonetic DNA (step 3)
    base_names.txt        # Name pool (step 4) — source of truth
    config.yaml           # Generator config (names + dialect rules)
    dialect_rules.txt     # Dialect definitions (step 7)
    audit.md              # Quality report (steps 5+8)
    decisions.md          # Design decisions & rejected alternatives
output/mod/               # Generated submod files (ready to deploy)
docs/
  PIPELINE.md             # Full 9-step methodology
  MAP_ANALYSIS.md         # Geographic analysis from in-game maps
  CHANGELOG.md            # Version history
map/                      # In-game map screenshots for reference
_specs/
  PROMPT_PIPELINE.md      # AI-assisted workflow prompt template
```

### Scripts

| Script | Purpose |
|--------|---------|
| `generate_mod.py` | Reads `config.yaml` per language, generates EU5 mod files (language blocks, culture patches, localization with dialect variants) |
| `deploy.py` | Copies `output/mod/` to the Paradox mod folder |
| `validate_names.py` | Validates name pools against quality rules (syllable count, diversity, overlap) |
| `names_to_yaml.py` | Converts `base_names.txt` to YAML config format |
| `context_digest.py` | Generates a project digest for quick status overview |

## AI-assisted workflow

This project was built with **Claude Code** as a creative partner. The methodology (phonetic DNA, non-overlap matrix, dialect systems) was designed collaboratively. The prompt template used for each language is in [_specs/PROMPT_PIPELINE.md](_specs/PROMPT_PIPELINE.md) — feel free to adapt it for your own naming projects.

## Contributing

Contributions welcome! If you want to:
- **Add names** to an existing language — edit `names/<language>/base_names.txt` and run `python generate_mod.py names/<language>/config.yaml`
- **Create a new language** — follow the pipeline in `docs/PIPELINE.md`
- **Fix dialect rules** — edit the relevant `config.yaml` dialect section
- **Report issues** — open a GitHub issue

## License

This project is licensed under the [MIT License](LICENSE).

The mod files are designed to work with [Etra: The New Age](https://steamcommunity.com/sharedfiles/filedetails/?id=3619896881) by Nuka, which has its own terms.
