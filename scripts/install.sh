#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
TARGET=""
INSTALL_ALL=0
FORCE=0
LIST_ONLY=0
SELECTED=""

usage() {
  printf '%s\n' \
    "Usage:" \
    "  ./scripts/install.sh --list" \
    "  ./scripts/install.sh --target PATH SKILL [SKILL ...]" \
    "  ./scripts/install.sh --target PATH --all" \
    "" \
    "Options:" \
    "  --target PATH  Agent skills directory" \
    "  --all          Install every catalogued skill" \
    "  --force        Back up and replace an existing installation" \
    "  --list         List available skill names" \
    "  -h, --help     Show this help"
}

list_skills() {
  find "$REPO_ROOT/skills" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      [ "$#" -ge 2 ] || { printf '%s\n' "Missing value for --target" >&2; exit 2; }
      TARGET=$2
      shift 2
      ;;
    --all)
      INSTALL_ALL=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --list)
      LIST_ONLY=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      printf '%s\n' "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      SELECTED="$SELECTED $1"
      shift
      ;;
  esac
done

if [ "$LIST_ONLY" -eq 1 ]; then
  list_skills
  exit 0
fi

[ -n "$TARGET" ] || { printf '%s\n' "--target is required" >&2; usage >&2; exit 2; }

if [ "$INSTALL_ALL" -eq 1 ]; then
  [ -z "$SELECTED" ] || { printf '%s\n' "Use either --all or named skills, not both" >&2; exit 2; }
  SELECTED=$(list_skills | tr '\n' ' ')
fi

[ -n "$SELECTED" ] || { printf '%s\n' "Select at least one skill or use --all" >&2; exit 2; }

for NAME in $SELECTED; do
  SOURCE="$REPO_ROOT/skills/$NAME"
  DESTINATION="$TARGET/$NAME"

  [ -f "$SOURCE/SKILL.md" ] || { printf '%s\n' "Unknown or invalid skill: $NAME" >&2; exit 1; }

  if [ -e "$DESTINATION" ] && [ "$FORCE" -ne 1 ]; then
    printf '%s\n' "Already installed: $DESTINATION (use --force to upgrade)" >&2
    exit 1
  fi
done

mkdir -p "$TARGET"

for NAME in $SELECTED; do
  SOURCE="$REPO_ROOT/skills/$NAME"
  DESTINATION="$TARGET/$NAME"

  if [ -e "$DESTINATION" ]; then
    BACKUP="$DESTINATION.backup-$(date +%Y%m%d%H%M%S)-$$"
    mv "$DESTINATION" "$BACKUP"
    printf '%s\n' "Backed up: $BACKUP"
  fi

  cp -R "$SOURCE" "$DESTINATION"
  printf '%s\n' "Installed: $NAME -> $DESTINATION"
done
