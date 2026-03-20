#!/usr/bin/env python3
"""
Generate EU5/Etra submod files from a YAML language config.

Usage:
    python generate_mod.py names/ardrainic/config.yaml
    python generate_mod.py names/torrent/config.yaml names/armonorican/config.yaml
    python generate_mod.py --all

Generates 3 files per language in output/<language>/:
    - 02_etra_names_patch.txt   (language REPLACE block)
    - etra_custom_names_l_english.yml (localization with dialect variants)
    - 02_etra_cultures_patch.txt (culture REPLACE blocks)

Requires: PyYAML (pip install pyyaml)
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def transform(name: str, rules: list[tuple[str, str]] | None = None, *,
              prefix_rules: list[tuple[str, str]] | None = None,
              replace_rules: list[tuple[str, str]] | None = None,
              overrides: dict[str, str] | None = None) -> str:
    """Apply transformation rules: overrides → prefix → suffix → replace."""
    if overrides and name in overrides:
        return overrides[name]
    result = name
    # 1. Prefix rules (first match, longest first)
    if prefix_rules:
        sorted_prefix = sorted(prefix_rules, key=lambda x: len(x[0]), reverse=True)
        for prefix, replacement in sorted_prefix:
            if result.startswith(prefix):
                result = replacement + result[len(prefix):]
                break
    # 2. Suffix rules (first match, longest first)
    if rules:
        sorted_rules = sorted(rules, key=lambda x: len(x[0]), reverse=True)
        for suffix, replacement in sorted_rules:
            if result.endswith(suffix):
                result = result[: -len(suffix)] + replacement
                break
    # 3. Replace rules (all applied sequentially)
    if replace_rules:
        for old, new in replace_rules:
            result = result.replace(old, new)
    return result


def to_key(name: str) -> str:
    """Convert a display name to a Paradox name_ key."""
    return "name_" + name.lower()


def to_token(name: str) -> str:
    """Convert a dynasty/lowborn name to a safe Paradox token (spaces → underscores)."""
    return name.replace(" ", "_")


def dialect_display_name(dialect_id: str) -> str:
    """Convert a dialect ID to a human-readable display name.

    Examples:
        sittadellian_dialect → Sittadellian
        ardrainic_language   → Ardrainic
        tiefling_torrent_dialect → Tiefling Torrent
    """
    name = dialect_id
    for suffix in ("_dialect", "_language"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name.replace("_", " ").title()


def load_variants_file(path: Path, column: int) -> dict:
    """Parse a whitespace-delimited variant table (e.g. sordrenic dialect_variants.txt).

    Returns {"male": {base: variant}, "female": {base: variant}, "dynasty": {base: variant}}.
    """
    male, female, dynasty = {}, {}, {}
    current = male
    with open(path, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                upper = stripped.upper()
                if "DYNAST" in upper:
                    current = dynasty
                elif "FEMININ" in upper or "FEMALE" in upper:
                    current = female
                continue
            parts = stripped.split()
            if len(parts) >= column + 1:
                base, variant = parts[0], parts[column]
                if variant != base:
                    current[base] = variant
    return {"male": male, "female": female, "dynasty": dynasty}


def load_config(path: Path) -> dict:
    """Load and validate a YAML config file."""
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    required = ["language_id", "color"]
    for key in required:
        if key not in cfg:
            print(f"ERROR: Missing required key '{key}' in {path}", file=sys.stderr)
            sys.exit(1)

    # Check for duplicate names
    custom = cfg.get("custom_names", {})
    for gender in ("male", "female"):
        names = flatten_custom_names(custom.get(gender))
        seen = set()
        for n in names:
            low = n.lower()
            if low in seen:
                print(f"WARNING: Duplicate {gender} name '{n}' in {path}", file=sys.stderr)
            seen.add(low)

    # Normalize dialect rules to list[tuple[str,str]]
    rule_keys = ("rules_m", "rules_f", "rules_dyn", "rules_low",
                 "prefix_rules_m", "prefix_rules_f",
                 "replace_rules_m", "replace_rules_f",
                 "replace_rules_dyn", "replace_rules_low")
    for dialect in cfg.get("dialects", []):
        for rule_key in rule_keys:
            if rule_key in dialect:
                dialect[rule_key] = [(r[0], r[1]) for r in dialect[rule_key]]

    # Load external variant files for dialects
    config_dir = path.parent
    for dialect in cfg.get("dialects", []):
        vf = dialect.get("variants_file")
        if vf:
            col = dialect.get("variants_column", 1)
            variants = load_variants_file(config_dir / vf, col)
            dialect.setdefault("overrides_m", {}).update(variants.get("male", {}))
            dialect.setdefault("overrides_f", {}).update(variants.get("female", {}))
            dialect.setdefault("overrides_dyn", {}).update(variants.get("dynasty", {}))

    return cfg


def flatten_custom_names(custom: dict | list | None) -> list[str]:
    """Flatten custom_names which can be a dict of categories or a flat list."""
    if custom is None:
        return []
    if isinstance(custom, list):
        return list(custom)
    # dict of category -> list
    names = []
    for _cat, cat_names in custom.items():
        if isinstance(cat_names, list):
            names.extend(cat_names)
    return names


def flatten_custom_names_with_categories(custom: dict | list | None) -> list[tuple[str, str]]:
    """Return [(category, name), ...] preserving category labels."""
    if custom is None:
        return []
    if isinstance(custom, list):
        return [("", n) for n in custom]
    result = []
    for cat, cat_names in custom.items():
        if isinstance(cat_names, list):
            for n in cat_names:
                result.append((cat, n))
    return result


# ---------------------------------------------------------------------------
# Generator: Language patch (02_etra_names_patch.txt)
# ---------------------------------------------------------------------------

def generate_language_patch(cfg: dict) -> str:
    """Generate the REPLACE:<language_id> = { ... } block."""
    lines = []
    lang_id = cfg["language_id"]
    lang_label = lang_id.replace("_language", "")

    # File header
    lines.append(f"# Etra: Names & Cultures — {lang_label} language override")
    lines.append(f"# Generated by generate_mod.py from config.yaml")
    lines.append(f"# Fully replaces the original {lang_id} definition.")
    lines.append(f"# All names are 100% custom fantasy — no original mod names kept.")
    lines.append("")
    lines.append(f"REPLACE:{lang_id} = {{")
    lines.append("")
    lines.append(f"\tcolor = {cfg['color']}")
    if cfg.get("family"):
        lines.append(f"\tfamily = {cfg['family']}")

    # --- male_names ---
    lines.append("")
    lines.append("\tmale_names = {")
    custom_m = cfg.get("custom_names", {}).get("male")
    if custom_m:
        lines.append("")
        lines.append("\t\t# === CUSTOM FANTASY MALE NAMES ===")
        cats = flatten_custom_names_with_categories(custom_m)
        current_cat = None
        row = []
        for cat, name in cats:
            if cat != current_cat:
                if row:
                    lines.append("\t\t" + " ".join(row))
                    row = []
                current_cat = cat
                if cat:
                    lines.append(f"\t\t# {cat}")
            row.append(to_key(name))
            if len(row) >= 10:
                lines.append("\t\t" + " ".join(row))
                row = []
        if row:
            lines.append("\t\t" + " ".join(row))
    lines.append("\t}")

    # --- female_names ---
    lines.append("")
    lines.append("\tfemale_names = {")
    custom_f = cfg.get("custom_names", {}).get("female")
    if custom_f:
        lines.append("")
        lines.append("\t\t# === CUSTOM FANTASY FEMALE NAMES ===")
        cats = flatten_custom_names_with_categories(custom_f)
        current_cat = None
        row = []
        for cat, name in cats:
            if cat != current_cat:
                if row:
                    lines.append("\t\t" + " ".join(row))
                    row = []
                current_cat = cat
                if cat:
                    lines.append(f"\t\t# {cat}")
            row.append(to_key(name))
            if len(row) >= 10:
                lines.append("\t\t" + " ".join(row))
                row = []
        if row:
            lines.append("\t\t" + " ".join(row))
    lines.append("\t}")

    # --- dynasty_names ---
    lines.append("")
    lines.append("\tdynasty_names = {")
    custom_dyn = cfg.get("custom_names", {}).get("dynasties", [])
    if custom_dyn:
        for i in range(0, len(custom_dyn), 5):
            chunk = [to_token(d) for d in custom_dyn[i : i + 5]]
            lines.append("\t\t" + " ".join(chunk))
    lines.append("\t}")

    # --- lowborn ---
    lines.append("")
    lines.append("\tlowborn = {")
    custom_low = cfg.get("custom_names", {}).get("lowborn", [])
    if custom_low:
        for i in range(0, len(custom_low), 8):
            chunk = [to_token(l) for l in custom_low[i : i + 8]]
            lines.append("\t\t" + " ".join(chunk))
    lines.append("\t}")

    # --- ship_names ---
    orig_ships = cfg.get("ships", [])
    if orig_ships:
        lines.append("")
        lines.append("\tship_names = {")
        for i in range(0, len(orig_ships), 8):
            chunk = orig_ships[i : i + 8]
            lines.append("\t\t" + " ".join(chunk))
        lines.append("\t}")

    # --- dynasty_template_keys ---
    dtk = cfg.get("dynasty_template_keys", [])
    if dtk:
        lines.append("")
        lines.append("\tdynasty_template_keys = {")
        for key in dtk:
            lines.append(f"\t\t{key}")
        lines.append("\t}")

    # --- patronyms and prefixes ---
    lines.append("")
    for field in (
        "patronym_prefix_son",
        "patronym_prefix_son_vowel",
        "patronym_prefix_daughter",
        "patronym_suffix_son",
        "patronym_suffix_daughter",
        "location_prefix",
        "location_prefix_vowel",
        "location_suffix",
        "first_name_conjoiner",
        "descendant_prefix",
    ):
        if field in cfg:
            lines.append(f'\t{field} = "{cfg[field]}"')

    # --- dialects ---
    dialects = cfg.get("dialects", [])
    if dialects:
        lines.append("")
        lines.append("\tdialects = {")
        # Default dialect (configurable, defaults to language_id)
        default_did = cfg.get("default_dialect_id", lang_id)
        lines.append(f"\t\t{default_did} = {{")
        lines.append("\t\t\tdefault = yes")
        lines.append("\t\t}")
        for d in dialects:
            has_extra = any(d.get(k) for k in ("extra_male", "extra_female", "extra_dynasties", "extra_lowborn"))
            if has_extra:
                lines.append(f"\t\t{d['id']} = {{")
                # Male/Female names use name_ keys
                for ntype, block_name in (("extra_male", "male_names"),
                                           ("extra_female", "female_names")):
                    extra = d.get(ntype, [])
                    if extra:
                        lines.append(f"\t\t\t{block_name} = {{")
                        row = []
                        for name in extra:
                            row.append(to_key(name))
                            if len(row) >= 10:
                                lines.append("\t\t\t\t" + " ".join(row))
                                row = []
                        if row:
                            lines.append("\t\t\t\t" + " ".join(row))
                        lines.append("\t\t\t}")
                # Dynasties use raw identifiers (no name_ prefix)
                extra_dyn = d.get("extra_dynasties", [])
                if extra_dyn:
                    lines.append("\t\t\tdynasty_names = {")
                    for i in range(0, len(extra_dyn), 5):
                        chunk = [to_token(dn) for dn in extra_dyn[i : i + 5]]
                        lines.append("\t\t\t\t" + " ".join(chunk))
                    lines.append("\t\t\t}")
                # Lowborn use raw identifiers
                extra_low = d.get("extra_lowborn", [])
                if extra_low:
                    lines.append("\t\t\tlowborn = {")
                    for i in range(0, len(extra_low), 8):
                        chunk = [to_token(lb) for lb in extra_low[i : i + 8]]
                        lines.append("\t\t\t\t" + " ".join(chunk))
                    lines.append("\t\t\t}")
                lines.append("\t\t}")
            else:
                lines.append(f"\t\t{d['id']} = {{}}")
        lines.append("\t}")

    lines.append("}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Generator: Localization YML
# ---------------------------------------------------------------------------

def generate_localization(cfg: dict) -> tuple[str, dict]:
    """Generate the localization YML with dialect variants."""
    lines = []
    # UTF-8 BOM is handled at write time
    lang_id = cfg["language_id"]
    lang_label = lang_id.replace("_language", "").upper()
    dialects = cfg.get("dialects", [])

    # File header
    lines.append(f"# Etra: Names & Cultures — {lang_label} localization")
    lines.append(f"# Generated by generate_mod.py from config.yaml")
    lines.append(f"# Base name entries + dialect variant entries for each custom name.")
    lines.append(f"# Variants are only generated when the dialect transformation differs from the base name.")
    lines.append("#")
    dialect_ids = [d['id'] for d in dialects]
    if dialect_ids:
        lines.append(f"# Dialects: {', '.join(dialect_ids)}")
    lines.append("")
    lines.append("l_english:")
    lines.append(f" # === {lang_label} DIALECT VARIANTS ===")
    stats = {"base": 0, "variants": 0}

    # --- Male names ---
    custom_m = flatten_custom_names(cfg.get("custom_names", {}).get("male"))
    if custom_m:
        lines.append("# --- MALE NAMES ---")
        for name in custom_m:
            key = to_key(name)
            lines.append(f' {key}: "{name}"')
            stats["base"] += 1
            for d in dialects:
                variant = transform(
                    name,
                    d.get("rules_m"),
                    prefix_rules=d.get("prefix_rules_m"),
                    replace_rules=d.get("replace_rules_m"),
                    overrides=d.get("overrides_m"),
                )
                if variant != name:
                    lines.append(f' {key}.{d["id"]}: "{variant}"')
                    stats["variants"] += 1
            lines.append("")

    # --- Female names ---
    custom_f = flatten_custom_names(cfg.get("custom_names", {}).get("female"))
    if custom_f:
        lines.append("# --- FEMALE NAMES ---")
        for name in custom_f:
            key = to_key(name)
            lines.append(f' {key}: "{name}"')
            stats["base"] += 1
            for d in dialects:
                variant = transform(
                    name,
                    d.get("rules_f"),
                    prefix_rules=d.get("prefix_rules_f"),
                    replace_rules=d.get("replace_rules_f"),
                    overrides=d.get("overrides_f"),
                )
                if variant != name:
                    lines.append(f' {key}.{d["id"]}: "{variant}"')
                    stats["variants"] += 1
            lines.append("")

    # --- Dynasty names localization ---
    # Always generate loc for dynasties that contain underscores (display _ as space)
    # Also generate dialect variants if rules exist
    custom_dyn = cfg.get("custom_names", {}).get("dynasties", [])
    has_dyn_rules = any(d.get("rules_dyn") or d.get("overrides_dyn") for d in dialects)
    needs_dyn_loc = custom_dyn and (has_dyn_rules or any("_" in n or " " in n for n in custom_dyn))
    if needs_dyn_loc:
        lines.append("# --- DYNASTY NAMES ---")
        for name in custom_dyn:
            token = to_token(name)
            display = name.replace("_", " ")
            lines.append(f' {token}: "{display}"')
            stats["base"] += 1
            if has_dyn_rules:
                for d in dialects:
                    variant = transform(
                        name,
                        d.get("rules_dyn"),
                        replace_rules=d.get("replace_rules_dyn"),
                        overrides=d.get("overrides_dyn"),
                    )
                    if variant != name:
                        variant_display = variant.replace("_", " ")
                        lines.append(f' {token}.{d["id"]}: "{variant_display}"')
                        stats["variants"] += 1
            lines.append("")

    # --- Lowborn names localization ---
    custom_low = cfg.get("custom_names", {}).get("lowborn", [])
    has_low_rules = any(d.get("rules_low") or d.get("overrides_low") for d in dialects)
    needs_low_loc = custom_low and (has_low_rules or any("_" in n or " " in n for n in custom_low))
    if needs_low_loc:
        lines.append("# --- LOWBORN NAMES ---")
        for name in custom_low:
            token = to_token(name)
            display = name.replace("_", " ")
            lines.append(f' {token}: "{display}"')
            stats["base"] += 1
            if has_low_rules:
                for d in dialects:
                    variant = transform(
                        name,
                        d.get("rules_low"),
                        replace_rules=d.get("replace_rules_low"),
                        overrides=d.get("overrides_low"),
                    )
                    if variant != name:
                        variant_display = variant.replace("_", " ")
                        lines.append(f' {token}.{d["id"]}: "{variant_display}"')
                        stats["variants"] += 1
            lines.append("")

    # --- Extra dynasty/lowborn loc from dialect mini-pools ---
    extra_dyn_low_seen = set()
    for d in dialects:
        for name in d.get("extra_dynasties", []) + d.get("extra_lowborn", []):
            token = to_token(name)
            if token not in extra_dyn_low_seen and ("_" in name or " " in name):
                extra_dyn_low_seen.add(token)
                display = name.replace("_", " ")
                lines.append(f' {token}: "{display}"')
                stats["base"] += 1

    # --- Extra names from dialect mini-pools (base loc only, no variants) ---
    extra_seen = set()
    for d in dialects:
        for ntype in ("extra_male", "extra_female"):
            for name in d.get(ntype, []):
                low = name.lower()
                if low not in extra_seen:
                    extra_seen.add(low)
                    key = to_key(name)
                    lines.append(f' {key}: "{name}"')
                    stats["base"] += 1

    # --- Dialect display names ---
    lines.append("")
    lines.append("# --- DIALECT DISPLAY NAMES ---")
    default_did = cfg.get("default_dialect_id", lang_id)
    all_dialect_ids = [default_did] + [d["id"] for d in dialects]
    for did in all_dialect_ids:
        display = dialect_display_name(did)
        lines.append(f' {did}: "{display}"')
        stats["base"] += 1

    return "\n".join(lines) + "\n", stats


# ---------------------------------------------------------------------------
# Generator: Culture patch
# ---------------------------------------------------------------------------

def generate_culture_patch(cfg: dict) -> str:
    """Generate REPLACE blocks for each culture."""
    cultures = cfg.get("cultures", [])
    if not cultures:
        return ""

    lang_label = cfg["language_id"].replace("_language", "")
    blocks = []
    blocks.append(f"# Etra: Names & Cultures — {lang_label} culture overrides")
    blocks.append(f"# Generated by generate_mod.py from config.yaml")
    blocks.append(f"# Each culture is reassigned to its own dialect for regional name variants.")
    blocks.append("")
    blocks.append(f"# === {lang_label.upper()} CULTURES ===")
    blocks.append("")

    for culture in cultures:
        cid = culture["id"]
        dialect = culture["dialect"]
        color = culture["color"]
        tags = culture.get("tags", [])
        groups = culture.get("groups", [])

        block_lines = []
        block_lines.append(f"REPLACE:{cid} = {{")
        block_lines.append(f"\tlanguage = {dialect}")
        block_lines.append(f"\tcolor = {color}")
        if tags:
            tags_str = " ".join(tags)
            block_lines.append(f"\ttags = {{ {tags_str} }}")
        if groups:
            block_lines.append("\tculture_groups = {")
            for g in groups:
                block_lines.append(f"\t\t{g}")
            block_lines.append("\t}")

        # Extra fields (use_patronym, etc.) — convert Python bools to Paradox yes/no
        for extra_key in ("use_patronym",):
            if extra_key in culture:
                val = culture[extra_key]
                if isinstance(val, bool):
                    val = "yes" if val else "no"
                block_lines.append(f"\t{extra_key} = {val}")

        block_lines.append("}")
        blocks.append("\n".join(block_lines))
        blocks.append("")

    return "\n".join(blocks) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_config(config_path: Path, output_root: Path) -> tuple[dict, Path]:
    """Process a single config YAML and generate all output files.

    Returns (cfg, out_dir) for downstream mod assembly.
    """
    cfg = load_config(config_path)
    lang_id = cfg["language_id"]
    lang_name = lang_id.replace("_language", "")
    out_dir = output_root / lang_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Language patch (static copy or generated)
    # All .txt files must be UTF-8 BOM for EU5
    static_file = cfg.get("static_language_file")
    if static_file:
        src = config_path.parent / static_file
        lang_filename = cfg.get("language_patch_file", src.name)
        # Re-encode static file as UTF-8 BOM
        content = src.read_text(encoding="utf-8")
        with open(out_dir / lang_filename, "w", encoding="utf-8-sig") as f:
            f.write(content)
    else:
        lang_patch = generate_language_patch(cfg)
        lang_filename = cfg.get("language_patch_file", f"02_etra_{lang_name}_language.txt")
        lang_patch_path = out_dir / lang_filename
        with open(lang_patch_path, "w", encoding="utf-8-sig") as f:
            f.write(lang_patch)

    # 2. Localization YML (UTF-8 with BOM, one file per language)
    loc_content, stats = generate_localization(cfg)
    loc_path = out_dir / f"etra_{lang_name}_names_l_english.yml"
    with open(loc_path, "w", encoding="utf-8-sig") as f:
        f.write(loc_content)

    # 3. Culture patch (UTF-8 BOM for EU5)
    culture_patch = generate_culture_patch(cfg)
    if culture_patch:
        culture_path = out_dir / "02_etra_cultures_patch.txt"
        with open(culture_path, "w", encoding="utf-8-sig") as f:
            f.write(culture_patch)

    # Stats summary
    custom = cfg.get("custom_names", {})
    n_m = len(flatten_custom_names(custom.get("male")))
    n_f = len(flatten_custom_names(custom.get("female")))
    n_dyn = len(custom.get("dynasties", []))
    n_low = len(custom.get("lowborn", []))
    n_dialects = len(cfg.get("dialects", []))
    n_cultures = len(cfg.get("cultures", []))

    print(f"=== {lang_name} ===")
    print(f"  Names:         {n_m}M + {n_f}F + {n_dyn} dynasties + {n_low} lowborn")
    print(f"  Dialects:      {n_dialects}")
    print(f"  Cultures:      {n_cultures}")
    print(f"  Loc entries:   {stats['base']} base + {stats['variants']} variants = {stats['base'] + stats['variants']} total")
    print(f"  Output:        {out_dir}")
    print()

    return cfg, out_dir


def find_all_configs(root: Path) -> list[Path]:
    """Find all config.yaml files in names/*/."""
    names_dir = root / "names"
    if not names_dir.is_dir():
        print(f"ERROR: names/ directory not found at {names_dir}", file=sys.stderr)
        sys.exit(1)
    configs = sorted(names_dir.glob("*/config.yaml"))
    if not configs:
        print("ERROR: No config.yaml found in names/*/", file=sys.stderr)
        sys.exit(1)
    return configs


def assemble_mod(output_root: Path, processed: list[tuple[dict, Path]], mod_dir: Path | None = None) -> Path:
    """Assemble a mod-ready directory from per-language outputs.

    Creates the submod structure:
        in_game/common/languages/
        in_game/common/cultures/
        main_menu/localization/english/
    """
    if mod_dir is None:
        mod_dir = output_root / "mod"

    # Clean previous assembly (preserve .git if present)
    if mod_dir.exists():
        git_dir = mod_dir / ".git"
        has_git = git_dir.exists()
        if has_git:
            # Keep .git, remove everything else
            for item in mod_dir.iterdir():
                if item.name == ".git":
                    continue
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        else:
            shutil.rmtree(mod_dir)

    lang_dir = mod_dir / "in_game" / "common" / "languages"
    cult_dir = mod_dir / "in_game" / "common" / "cultures"
    loc_dir = mod_dir / "main_menu" / "localization" / "english"

    for d in (lang_dir, cult_dir, loc_dir):
        d.mkdir(parents=True, exist_ok=True)

    for cfg, src_dir in processed:
        lang_name = cfg["language_id"].replace("_language", "")

        # Language patch
        lang_file = cfg.get("language_patch_file", f"02_etra_{lang_name}_language.txt")
        src = src_dir / lang_file
        if src.exists():
            shutil.copy2(src, lang_dir / lang_file)

        # Culture patch (unique filename per language to avoid collisions)
        cult_file = cfg.get("culture_patch_file", f"02_etra_{lang_name}_cultures.txt")
        src = src_dir / "02_etra_cultures_patch.txt"
        if src.exists():
            shutil.copy2(src, cult_dir / cult_file)

        # Localization
        loc_file = f"etra_{lang_name}_names_l_english.yml"
        src = src_dir / loc_file
        if src.exists():
            shutil.copy2(src, loc_dir / loc_file)

    # Copy manual overrides (characters, extra loc, etc.)
    overrides_dir = output_root.parent / "overrides"
    if overrides_dir.exists():
        for src_file in overrides_dir.rglob("*"):
            if src_file.is_file():
                rel = src_file.relative_to(overrides_dir)
                dest = mod_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dest)

    # Generate metadata.json
    metadata = {
        "name": "Etra: Names & Cultures",
        "id": "ianis.etra.names_cultures",
        "version": "0.1.0",
        "short_description": "Adds unique fantasy names and dialect variants for all Etra cultures.",
        "tags": ["Gameplay"],
        "supported_game_version": "1.1.*",
        "relationships": [{
            "rel_type": "dependency",
            "id": "nuka.etra",
            "display_name": "Etra: The New Age",
            "resource_type": "mod",
            "version": "0.05",
        }],
        "game_custom_data": {
            "multiplayer_synchronized": True,
            "replace_paths": [],
        },
    }
    meta_dir = mod_dir / ".metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)
    (meta_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=4), encoding="utf-8"
    )

    print(f"Mod assembled -> {mod_dir}")
    return mod_dir


def generate_status(cfg: dict, config_path: Path) -> str:
    """Generate a STATUS.md template from config data."""
    lang_id = cfg["language_id"]
    lang_name = lang_id.replace("_language", "")
    custom = cfg.get("custom_names", {})
    n_m = len(flatten_custom_names(custom.get("male")))
    n_f = len(flatten_custom_names(custom.get("female")))
    n_dyn = len(custom.get("dynasties", []))
    n_low = len(custom.get("lowborn", []))
    n_dialects = len(cfg.get("dialects", []))
    n_cultures = len(cfg.get("cultures", []))

    dialect_ids = [d["id"] for d in cfg.get("dialects", [])]

    lines = []
    lines.append(f"# {lang_name} — Status")
    lines.append("")
    lines.append("## Pipeline")
    lines.append("- [x] Etape 1 — Identification")
    lines.append("- [x] Etape 2 — Geographie")
    lines.append("- [x] Etape 3 — ADN phonetique")
    lines.append(f"- [x] Etape 4 — Generation : {n_m}M + {n_f}F + {n_dyn}dyn + {n_low}low")
    lines.append("- [ ] Etape 5 — Audit qualite")
    lines.append("- [ ] Etape 6 — Substrat racial")
    lines.append(f"- [{'x' if n_dialects else ' '}] Etape 7 — Dialectes : {n_dialects} crees")
    lines.append("- [ ] Etape 8 — Audit cross-langue")
    lines.append("- [ ] Etape 9 — Sauvegarde")
    lines.append("")
    lines.append("## Chiffres")
    lines.append(f"Prenoms M: {n_m} | Prenoms F: {n_f} | Dynasties: {n_dyn} | Roturiers: {n_low} | Dialectes: {n_dialects}")
    if n_cultures:
        lines.append(f"Cultures: {n_cultures}")
    lines.append("")
    if dialect_ids:
        lines.append("## Dialectes")
        for did in dialect_ids:
            lines.append(f"- {did}")
        lines.append("")
    lines.append("## Prochaine action")
    lines.append("- A definir")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate EU5/Etra submod files from YAML language configs."
    )
    parser.add_argument(
        "configs",
        nargs="*",
        help="Path(s) to config.yaml files",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all config.yaml files in names/*/",
    )
    parser.add_argument(
        "--output", "-o",
        default="output",
        help="Output directory (default: output/)",
    )
    parser.add_argument(
        "--mod-dir",
        default=None,
        help="Output mod directory (default: ../etra-names-cultures/ when --all)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Generate STATUS.md templates in each names/<lang>/ directory",
    )
    args = parser.parse_args()

    if not args.configs and not args.all:
        parser.print_help()
        sys.exit(1)

    output_root = Path(args.output)
    script_dir = Path(__file__).resolve().parent

    if args.all:
        configs = find_all_configs(script_dir)
    else:
        configs = [Path(c) for c in args.configs]

    processed = []
    for config_path in configs:
        if not config_path.is_file():
            print(f"ERROR: File not found: {config_path}", file=sys.stderr)
            sys.exit(1)
        result = process_config(config_path, output_root)
        processed.append(result)

        # Generate STATUS.md if requested
        if args.status:
            cfg, _ = result
            status_path = config_path.parent / "STATUS.md"
            if not status_path.exists():
                status_content = generate_status(cfg, config_path)
                status_path.write_text(status_content, encoding="utf-8")
                print(f"  STATUS.md generated: {status_path}")
            else:
                print(f"  STATUS.md already exists: {status_path} (skipped)")

    # Assemble mod-ready folder
    if args.mod_dir:
        mod_path = Path(args.mod_dir)
    else:
        mod_path = script_dir.parent / "submods" / "etra-names-cultures"
    assemble_mod(output_root, processed, mod_dir=mod_path)

    print(f"Done. {len(configs)} language(s) processed.")


if __name__ == "__main__":
    main()
