#!/usr/bin/env python3
"""
Validate name pools for quality, diversity, and cross-language overlap.

Runs mechanical checks that would otherwise burn Claude tokens:
- Syllable count (flag 4+ syllables)
- Prefix diversity (flag if <15 unique prefixes)
- Intra-language duplicates / near-duplicates (Levenshtein)
- Cross-language overlap (shared prefixes, endings, full names)
- Feminine autonomy (flag masc+"e" patterns)
- Length distribution stats

Usage:
    python validate_names.py                         # validate all languages
    python validate_names.py names/torrent/config.yaml  # single language
    python validate_names.py --cross                 # cross-language only

Saves ~15-20k tokens per language by automating audit steps 5 + 8.
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def count_syllables(name: str) -> int:
    """Estimate syllable count using vowel groups."""
    vowels = set("aeiouyàâäéèêëïîôùûüœæ")
    name_lower = name.lower()
    count = 0
    in_vowel = False
    for ch in name_lower:
        if ch in vowels:
            if not in_vowel:
                count += 1
                in_vowel = True
        else:
            in_vowel = False
    return max(count, 1)


def levenshtein(s1: str, s2: str) -> int:
    """Compute Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            cost = 0 if c1 == c2 else 1
            curr_row.append(min(curr_row[j] + 1, prev_row[j + 1] + 1, prev_row[j] + cost))
        prev_row = curr_row
    return prev_row[-1]


def flatten_names(custom: dict | list | None) -> list[str]:
    """Flatten custom_names to flat list."""
    if custom is None:
        return []
    if isinstance(custom, list):
        return list(custom)
    names = []
    for cat_names in custom.values():
        if isinstance(cat_names, list):
            names.extend(cat_names)
    return names


def load_config(path: Path) -> dict:
    """Load YAML config."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def check_syllables(names: list[str], label: str) -> list[str]:
    """Flag names with 4+ syllables."""
    issues = []
    for name in names:
        syl = count_syllables(name)
        if syl >= 4:
            issues.append(f"  {label}: {name} ({syl} syllables)")
    return issues


def check_prefix_diversity(names: list[str], label: str, min_prefixes: int = 15) -> list[str]:
    """Check that we have enough unique prefixes (first 3 chars)."""
    issues = []
    if not names:
        return issues
    prefixes = set()
    prefix_counts = Counter()
    for name in names:
        p = name[:3].lower() if len(name) >= 3 else name.lower()
        prefixes.add(p)
        prefix_counts[p] += 1

    if len(prefixes) < min_prefixes:
        issues.append(f"  {label}: Only {len(prefixes)} unique prefixes (target: {min_prefixes}+)")

    # Flag overused prefixes (>= 5 names with same prefix)
    overused = [(p, c) for p, c in prefix_counts.most_common() if c >= 5]
    for p, c in overused:
        issues.append(f"  {label}: Prefix '{p}' used {c} times — consider diversifying")

    return issues


def check_duplicates(names: list[str], label: str) -> list[str]:
    """Find exact duplicates and near-duplicates (Levenshtein <= 2)."""
    issues = []
    seen = {}
    for name in names:
        low = name.lower()
        if low in seen:
            issues.append(f"  {label}: DUPLICATE '{name}' (same as '{seen[low]}')")
        seen[low] = name

    # Near-duplicates (only for reasonable pool sizes)
    if len(names) <= 200:
        lowers = [(n, n.lower()) for n in names]
        for i in range(len(lowers)):
            for j in range(i + 1, len(lowers)):
                n1, l1 = lowers[i]
                n2, l2 = lowers[j]
                if l1 != l2 and levenshtein(l1, l2) <= 1:
                    issues.append(f"  {label}: Near-duplicate '{n1}' <-> '{n2}' (Levenshtein=1)")

    return issues


def check_feminine_autonomy(males: list[str], females: list[str]) -> list[str]:
    """Flag feminines that are just masculine + 'e' or similar trivial suffixes."""
    issues = []
    male_set = {n.lower() for n in males}
    for f_name in females:
        f_low = f_name.lower()
        # Check: masculine + e/a/ie/ine
        for suffix in ("e", "a", "ie", "ine", "ette", "elle"):
            base = f_low[:-len(suffix)] if f_low.endswith(suffix) else None
            if base and base in male_set:
                issues.append(f"  Feminine '{f_name}' looks like masculine '{base}' + '{suffix}'")
                break
    return issues


def check_length_distribution(names: list[str], label: str) -> list[str]:
    """Report length distribution stats."""
    if not names:
        return []
    lengths = [len(n) for n in names]
    syllables = [count_syllables(n) for n in names]
    avg_len = sum(lengths) / len(lengths)
    avg_syl = sum(syllables) / len(syllables)

    syl_dist = Counter(syllables)
    dist_str = " | ".join(f"{s}syl:{c}" for s, c in sorted(syl_dist.items()))

    return [f"  {label}: {len(names)} names, avg {avg_len:.1f} chars / {avg_syl:.1f} syl - [{dist_str}]"]


# ---------------------------------------------------------------------------
# Cross-language checks
# ---------------------------------------------------------------------------

def check_cross_language(all_langs: dict[str, dict]) -> list[str]:
    """Check for overlap between languages."""
    issues = []

    # 1. Exact name collisions
    name_to_lang = {}
    for lang, data in all_langs.items():
        all_names = data["male"] + data["female"]
        for name in all_names:
            low = name.lower()
            if low in name_to_lang and name_to_lang[low] != lang:
                issues.append(f"  COLLISION: '{name}' exists in both {name_to_lang[low]} AND {lang}")
            name_to_lang[low] = lang

    # 2. Shared prefix patterns (first 4 chars, threshold >= 3 names each)
    lang_prefixes = {}
    for lang, data in all_langs.items():
        prefixes = Counter()
        for name in data["male"] + data["female"]:
            if len(name) >= 4:
                prefixes[name[:4].lower()] += 1
        lang_prefixes[lang] = {p for p, c in prefixes.items() if c >= 3}

    langs = list(all_langs.keys())
    for i in range(len(langs)):
        for j in range(i + 1, len(langs)):
            shared = lang_prefixes.get(langs[i], set()) & lang_prefixes.get(langs[j], set())
            if shared:
                issues.append(f"  SHARED PREFIXES ({langs[i]} & {langs[j]}): {', '.join(sorted(shared))}")

    # 3. Shared endings (last 4 chars, threshold >= 5 names each)
    lang_endings = {}
    for lang, data in all_langs.items():
        endings = Counter()
        for name in data["male"] + data["female"]:
            if len(name) >= 4:
                endings[name[-4:].lower()] += 1
        lang_endings[lang] = {e for e, c in endings.items() if c >= 5}

    for i in range(len(langs)):
        for j in range(i + 1, len(langs)):
            shared = lang_endings.get(langs[i], set()) & lang_endings.get(langs[j], set())
            if shared:
                issues.append(f"  SHARED ENDINGS ({langs[i]} & {langs[j]}): {', '.join(sorted(shared))}")

    return issues


# ---------------------------------------------------------------------------
# Main validation
# ---------------------------------------------------------------------------

def validate_language(config_path: Path) -> tuple[list[str], list[str]]:
    """Run all checks on a single language. Returns (issues, stats)."""
    cfg = load_config(config_path)
    lang_name = config_path.parent.name
    custom = cfg.get("custom_names", {})

    males = flatten_names(custom.get("male"))
    females = flatten_names(custom.get("female"))
    dynasties = custom.get("dynasties", [])
    lowborn = custom.get("lowborn", [])

    issues = []
    stats = []

    # Stats
    stats.extend(check_length_distribution(males, f"{lang_name}/M"))
    stats.extend(check_length_distribution(females, f"{lang_name}/F"))

    # Syllable check
    issues.extend(check_syllables(males, f"{lang_name}/M"))
    issues.extend(check_syllables(females, f"{lang_name}/F"))

    # Prefix diversity
    issues.extend(check_prefix_diversity(males, f"{lang_name}/M"))
    issues.extend(check_prefix_diversity(females, f"{lang_name}/F", min_prefixes=10))

    # Duplicates
    issues.extend(check_duplicates(males, f"{lang_name}/M"))
    issues.extend(check_duplicates(females, f"{lang_name}/F"))
    issues.extend(check_duplicates(dynasties, f"{lang_name}/Dyn"))
    issues.extend(check_duplicates(lowborn, f"{lang_name}/Low"))

    # Feminine autonomy
    issues.extend(check_feminine_autonomy(males, females))

    return issues, stats


def main():
    parser = argparse.ArgumentParser(description="Validate Etra name pools for quality and overlap.")
    parser.add_argument("configs", nargs="*", help="Path(s) to config.yaml files")
    parser.add_argument("--all", action="store_true", help="Validate all languages")
    parser.add_argument("--cross", action="store_true", help="Run cross-language checks only")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    names_dir = root / "names"

    if args.all or args.cross or not args.configs:
        configs = sorted(names_dir.glob("*/config.yaml"))
    else:
        configs = [Path(c) for c in args.configs]

    if not configs:
        print("No config.yaml files found.", file=sys.stderr)
        sys.exit(1)

    all_langs = {}
    total_issues = 0

    if not args.cross:
        print("=" * 60)
        print("VALIDATION REPORT — Etra Names")
        print("=" * 60)

        for config_path in configs:
            lang_name = config_path.parent.name
            print(f"\n--- {lang_name} ---")

            issues, stats = validate_language(config_path)

            # Print stats
            for s in stats:
                print(f"  [STATS] {s.strip()}")

            # Print issues
            if issues:
                print(f"\n  [WARN] {len(issues)} issue(s):")
                for issue in issues:
                    print(f"    {issue.strip()}")
                total_issues += len(issues)
            else:
                print("  [OK] No issues found")

            # Collect for cross-language
            cfg = load_config(config_path)
            custom = cfg.get("custom_names", {})
            all_langs[lang_name] = {
                "male": flatten_names(custom.get("male")),
                "female": flatten_names(custom.get("female")),
            }
    else:
        # Cross-only mode
        for config_path in configs:
            lang_name = config_path.parent.name
            cfg = load_config(config_path)
            custom = cfg.get("custom_names", {})
            all_langs[lang_name] = {
                "male": flatten_names(custom.get("male")),
                "female": flatten_names(custom.get("female")),
            }

    # Cross-language checks
    if len(all_langs) >= 2:
        print(f"\n{'=' * 60}")
        print("CROSS-LANGUAGE OVERLAP CHECK")
        print(f"{'=' * 60}")

        cross_issues = check_cross_language(all_langs)
        if cross_issues:
            print(f"\n  [WARN] {len(cross_issues)} cross-language issue(s):")
            for issue in cross_issues:
                print(f"    {issue.strip()}")
            total_issues += len(cross_issues)
        else:
            print("  [OK] No cross-language overlaps detected")

    # Summary
    print(f"\n{'=' * 60}")
    if total_issues:
        print(f"TOTAL: {total_issues} issue(s) found across {len(configs)} language(s)")
    else:
        print(f"ALL CLEAR: {len(configs)} language(s) validated, no issues")
    print(f"{'=' * 60}")

    sys.exit(1 if total_issues > 0 else 0)


if __name__ == "__main__":
    main()
