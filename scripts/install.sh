#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
TARGET=""
INSTALL_ALL=0
FORCE=0
LIST_ONLY=0
SELECTED=""
STAGING=""

usage() {
  printf '%s\n' \
    "Usage:" \
    "  ./scripts/install.sh --list" \
    "  ./scripts/install.sh --target PATH SKILL [SKILL ...]" \
    "  ./scripts/install.sh --target PATH --all" \
    "" \
    "Options:" \
    "  --target PATH  Agent skills directory" \
    "  --all          Install every packaged skill" \
    "  --force        Back up and replace an existing installation" \
    "  --list         List available skill names" \
    "  -h, --help     Show this help"
}

fail() { printf '%s\n' "$*" >&2; exit 1; }

valid_name() {
  case "$1" in
    ''|*[!a-z0-9-]*|-*|*-|*--*) return 1 ;;
  esac
  [ "${#1}" -lt 64 ]
}

select_skill() {
  valid_name "$1" || fail "Invalid skill name: $1"
  case " $SELECTED " in
    *" $1 "*) return ;;
  esac
  SELECTED="${SELECTED:+$SELECTED }$1"
}

list_skills() {
  for source in "$REPO_ROOT"/skills/*; do
    name=${source##*/}
    if valid_name "$name" && [ -d "$source" ] && [ ! -L "$source" ] && [ -f "$source/SKILL.md" ]; then
      printf '%s\n' "$name"
    fi
  done
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      [ "$#" -ge 2 ] && [ -n "$2" ] || fail "Missing value for --target"
      TARGET=$2
      shift 2
      ;;
    --all) INSTALL_ALL=1; shift ;;
    --force) FORCE=1; shift ;;
    --list) LIST_ONLY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    --)
      shift
      for name in "$@"; do select_skill "$name"; done
      break
      ;;
    -*) fail "Unknown option: $1" ;;
    *) select_skill "$1"; shift ;;
  esac
done

if [ "$LIST_ONLY" -eq 1 ]; then list_skills; exit 0; fi
[ -n "$TARGET" ] || fail "--target is required"

if [ "$INSTALL_ALL" -eq 1 ]; then
  [ -z "$SELECTED" ] || fail "Use either --all or named skills, not both"
  for name in $(list_skills); do select_skill "$name"; done
fi
[ -n "$SELECTED" ] || fail "Select at least one skill or use --all"

# Validate every selection before creating the destination or changing any skill.
for NAME in $SELECTED; do
  SOURCE="$REPO_ROOT/skills/$NAME"
  [ ! -L "$SOURCE" ] && [ -f "$SOURCE/SKILL.md" ] || fail "Unknown or invalid skill: $NAME"
  if { [ -e "$TARGET/$NAME" ] || [ -L "$TARGET/$NAME" ]; } && [ "$FORCE" -ne 1 ]; then
    fail "Already installed: $TARGET/$NAME (use --force to upgrade)"
  fi
done

mkdir -p -- "$TARGET"
TARGET=$(CDPATH= cd -- "$TARGET" && pwd -P)
for NAME in $SELECTED; do
  SOURCE=$(CDPATH= cd -- "$REPO_ROOT/skills/$NAME" && pwd -P)
  DESTINATION="$TARGET/$NAME"
  case "$DESTINATION/" in "$SOURCE/"*) fail "Destination overlaps the source skill: $DESTINATION" ;; esac
  case "$SOURCE/" in "$DESTINATION/"*) fail "Destination contains the source skill: $DESTINATION" ;; esac
done

STAGING=$(mktemp -d "$TARGET/.skills-install.XXXXXX")
trap 'if [ -n "$STAGING" ]; then rm -rf -- "$STAGING"; fi' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# Complete every copy before replacing any existing installation.
for NAME in $SELECTED; do
  cp -R "$REPO_ROOT/skills/$NAME" "$STAGING/$NAME"
done

for NAME in $SELECTED; do
  DESTINATION="$TARGET/$NAME"
  BACKUP=""
  if [ -e "$DESTINATION" ] || [ -L "$DESTINATION" ]; then
    [ "$FORCE" -eq 1 ] || fail "Destination appeared during install: $DESTINATION"
    BACKUP=$(mktemp -d "$DESTINATION.backup-$(date +%Y%m%d%H%M%S).XXXXXX")
    rmdir -- "$BACKUP"
    mv -- "$DESTINATION" "$BACKUP"
    printf '%s\n' "Backed up: $BACKUP"
  fi
  if mv -- "$STAGING/$NAME" "$DESTINATION"; then
    printf '%s\n' "Installed: $NAME -> $DESTINATION"
  else
    if [ -n "$BACKUP" ]; then mv -- "$BACKUP" "$DESTINATION"; fi
    fail "Could not install: $NAME"
  fi
done
