#!/usr/bin/env python3
"""
Build and deploy the Etra Names & Cultures submod.

Runs generate_mod.py --all, then copies etra-names-cultures/ to the Paradox mod folder.

Usage:
    python deploy.py              # build + deploy
    python deploy.py --build-only # build only (no copy)
    python deploy.py --deploy-only # copy only (skip build)
    python deploy.py --dry-run    # show what would be copied

Saves time and tokens by eliminating manual copy steps.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


# Default Paradox mod folder
DEFAULT_PARADOX_DIR = Path(
    r"C:\Users\Dharma\Documents\Paradox Interactive\Europa Universalis V\mod\etra-names-cultures"
)


def build(root: Path) -> bool:
    """Run generate_mod.py --all."""
    script = root / "generate_mod.py"
    if not script.exists():
        print(f"ERROR: generate_mod.py not found at {script}", file=sys.stderr)
        return False

    print("Building mod files...")
    result = subprocess.run(
        [sys.executable, str(script), "--all"],
        cwd=str(root),
        capture_output=False,
    )
    return result.returncode == 0


def deploy(source: Path, paradox_dir: Path, dry_run: bool = False) -> bool:
    """Copy etra-names-cultures/ contents to the Paradox mod folder."""
    if not source.exists():
        print(f"ERROR: Build output not found at {source}", file=sys.stderr)
        print("  Run 'python deploy.py' (with build) or 'python generate_mod.py --all' first.", file=sys.stderr)
        return False

    # Collect all files to copy (skip .git/)
    files = [f for f in source.rglob("*") if f.is_file() and ".git" not in f.parts]

    if not files:
        print(f"WARNING: No files found in {source}", file=sys.stderr)
        return False

    print(f"\nDeploying {len(files)} files to {paradox_dir}")

    if dry_run:
        print("\n[DRY RUN] Would copy:")
        for f in files:
            rel = f.relative_to(source)
            dest = paradox_dir / rel
            print(f"  {rel} -> {dest}")
        return True

    # Create target dir if needed
    paradox_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for f in files:
        rel = f.relative_to(source)
        dest = paradox_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        copied += 1

    print(f"  Copied {copied} files")
    return True


def main():
    parser = argparse.ArgumentParser(description="Build and deploy Etra Names & Cultures submod.")
    parser.add_argument("--build-only", action="store_true", help="Build only, don't deploy")
    parser.add_argument("--deploy-only", action="store_true", help="Deploy only, skip build")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deployed")
    parser.add_argument("--paradox-dir", type=Path, default=DEFAULT_PARADOX_DIR, help="Target Paradox mod directory")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    mod_source = root.parent / "submods" / "etra-names-cultures"

    if not args.deploy_only:
        if not build(root):
            print("\nBuild FAILED", file=sys.stderr)
            sys.exit(1)
        print("\nBuild OK")

    if not args.build_only:
        if not deploy(mod_source, args.paradox_dir, args.dry_run):
            print("\nDeploy FAILED", file=sys.stderr)
            sys.exit(1)
        print("\nDeploy OK")

    if not args.build_only and not args.dry_run:
        print(f"\nMod ready at: {args.paradox_dir}")
        print("Launch EU5 and check in-game!")


if __name__ == "__main__":
    main()
