#!/usr/bin/env python3
"""
Parse base_names.txt and generate a config.yaml skeleton.

Reads the structured base_names.txt format (with ## categories and # comments)
and outputs a YAML config ready for generate_mod.py.

Usage:
    python names_to_yaml.py names/sordrenic/base_names.txt
    python names_to_yaml.py names/hravevi/base_names.txt --merge names/hravevi/config.yaml

With --merge: updates an existing config.yaml with names from base_names.txt,
preserving dialects, cultures, and other config fields.

Saves ~10-15k tokens per language by automating the format conversion.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml


def parse_base_names(path: Path) -> dict:
    """Parse a base_names.txt file into structured categories.

    Returns:
        {
            "male": {"Category Name": ["Name1", "Name2", ...]},
            "female": {"Category Name": ["Name1", ...]},
            "dynasties": ["dyn1", "dyn2", ...],
            "lowborn": ["low1", "low2", ...],
        }
    """
    result = {"male": {}, "female": {}, "dynasties": [], "lowborn": []}

    current_section = None  # male, female, dynasties, lowborn
    current_category = "Divers"

    with open(path, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Skip empty lines and separator lines
            if not stripped or stripped.startswith("===") or stripped.startswith("---"):
                continue

            upper = stripped.upper()

            # Detect main sections
            if "MASCULIN" in upper or "MALE NAME" in upper or "MALE NAMES" in upper or "PRENOMS MASCULINS" in upper:
                current_section = "male"
                current_category = "Divers"
                continue
            elif "FEMININ" in upper or "FEMALE NAME" in upper or "FEMALE NAMES" in upper or "PRENOMS FEMININS" in upper:
                current_section = "female"
                current_category = "Divers"
                continue
            elif "DYNAST" in upper:
                current_section = "dynasties"
                continue
            elif "LOWBORN" in upper or "ROTURIER" in upper:
                current_section = "lowborn"
                continue

            # Detect category headers (## Category Name)
            if stripped.startswith("##"):
                cat = stripped.lstrip("#").strip()
                # Clean up: remove trailing dashes
                cat = re.sub(r'\s*-+\s*$', '', cat)
                if cat:
                    current_category = cat
                continue

            # Detect sub-category (# Attaque Xyz- or # Attack Xyz-)
            if stripped.startswith("# ") and current_section in ("male", "female"):
                # Could be a sub-category header like "# Attaque Sig- (victoire)"
                sub = stripped[2:].strip()
                if "attaque" in sub.lower() or "attack" in sub.lower():
                    # Extract the attack name
                    match = re.search(r'(?:Attaque|Attack)\s+(\S+)', sub, re.IGNORECASE)
                    if match:
                        # Keep current category, this is just a sub-header
                        pass
                continue

            # Skip comment lines
            if stripped.startswith("#"):
                continue

            # Parse name line: "NameHere    # optional comment"
            if current_section:
                parts = stripped.split("#", 1)
                name = parts[0].strip()
                # Handle multi-name lines (space-separated)
                names = name.split()
                for n in names:
                    n = n.strip()
                    if not n or n.startswith("(") or len(n) < 2:
                        continue

                    if current_section == "male":
                        result["male"].setdefault(current_category, []).append(n)
                    elif current_section == "female":
                        result["female"].setdefault(current_category, []).append(n)
                    elif current_section == "dynasties":
                        result["dynasties"].append(n)
                    elif current_section == "lowborn":
                        result["lowborn"].append(n)

    return result


def to_yaml_config(parsed: dict, language_id: str = "CHANGE_ME_language",
                    color: str = "map_FRA") -> dict:
    """Convert parsed names to a config.yaml structure."""
    config = {
        "language_id": language_id,
        "color": color,
    }

    custom_names = {}

    if parsed["male"]:
        custom_names["male"] = {}
        for cat, names in parsed["male"].items():
            custom_names["male"][cat] = names

    if parsed["female"]:
        custom_names["female"] = {}
        for cat, names in parsed["female"].items():
            custom_names["female"][cat] = names

    if parsed["dynasties"]:
        custom_names["dynasties"] = parsed["dynasties"]

    if parsed["lowborn"]:
        custom_names["lowborn"] = parsed["lowborn"]

    config["custom_names"] = custom_names
    return config


def merge_into_existing(existing_path: Path, parsed: dict) -> dict:
    """Merge parsed names into an existing config.yaml, preserving other fields."""
    with open(existing_path, encoding="utf-8") as f:
        existing = yaml.safe_load(f)

    # Update custom_names only
    custom_names = existing.get("custom_names", {})

    if parsed["male"]:
        custom_names["male"] = {}
        for cat, names in parsed["male"].items():
            custom_names["male"][cat] = names

    if parsed["female"]:
        custom_names["female"] = {}
        for cat, names in parsed["female"].items():
            custom_names["female"][cat] = names

    if parsed["dynasties"]:
        custom_names["dynasties"] = parsed["dynasties"]

    if parsed["lowborn"]:
        custom_names["lowborn"] = parsed["lowborn"]

    existing["custom_names"] = custom_names
    return existing


def main():
    parser = argparse.ArgumentParser(
        description="Convert base_names.txt to config.yaml format."
    )
    parser.add_argument("input", help="Path to base_names.txt")
    parser.add_argument("--merge", help="Merge into existing config.yaml (preserves dialects, etc.)")
    parser.add_argument("-o", "--output", help="Output path (default: stdout)")
    parser.add_argument("--language-id", default="CHANGE_ME_language", help="Language ID for new configs")
    parser.add_argument("--color", default="map_FRA", help="Color for new configs")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    parsed = parse_base_names(input_path)

    # Stats
    n_m = sum(len(v) for v in parsed["male"].values())
    n_f = sum(len(v) for v in parsed["female"].values())
    n_d = len(parsed["dynasties"])
    n_l = len(parsed["lowborn"])
    print(f"Parsed: {n_m}M + {n_f}F + {n_d} dynasties + {n_l} lowborn", file=sys.stderr)

    if args.merge:
        merge_path = Path(args.merge)
        if not merge_path.exists():
            print(f"ERROR: Merge target not found: {merge_path}", file=sys.stderr)
            sys.exit(1)
        config = merge_into_existing(merge_path, parsed)
    else:
        config = to_yaml_config(parsed, args.language_id, args.color)

    # Output
    output = yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
