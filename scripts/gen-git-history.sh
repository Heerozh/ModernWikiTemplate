#!/bin/sh

set -eu

LIMIT=10
REPO_ROOT="."
CONTENT_DIR="content"
OUTPUT_PATH="data/git_history.json"

usage() {
  cat <<'EOF'
Usage: sh scripts/gen-git-history.sh [options]

Options:
  --limit <N>         Max commits per file (default: 10)
  --repo-root <PATH>  Repo root path (default: .)
  --content-dir <DIR> Content directory relative to repo root (default: content)
  --output <PATH>     Output JSON path relative to repo root (default: data/git_history.json)
  -h, --help          Show this help message
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --limit)
      LIMIT="$2"
      shift 2
      ;;
    --repo-root)
      REPO_ROOT="$2"
      shift 2
      ;;
    --content-dir)
      CONTENT_DIR="$2"
      shift 2
      ;;
    --output)
      OUTPUT_PATH="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

case "$LIMIT" in
  ''|*[!0-9]*)
    echo "Invalid --limit value: $LIMIT" >&2
    exit 1
    ;;
esac

CONTENT_DIR=${CONTENT_DIR%/}

cd "$REPO_ROOT"

output_dir=$(dirname "$OUTPUT_PATH")
mkdir -p "$output_dir"

if [ ! -d "$CONTENT_DIR" ]; then
  printf '{}\n' > "$OUTPUT_PATH"
  echo "Content directory not found: $CONTENT_DIR. Wrote empty history file."
  exit 0
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf '{}\n' > "$OUTPUT_PATH"
  echo "Not a git repository: $(pwd). Wrote empty history file."
  exit 0
fi

json_escape() {
  printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'
}

tmp_out=$(mktemp)
tmp_files=$(mktemp)
tmp_log=$(mktemp)
cleanup() {
  rm -f "$tmp_out" "$tmp_files" "$tmp_log"
}
trap cleanup EXIT INT TERM

find "$CONTENT_DIR" -type f -name '*.md' | LC_ALL=C sort > "$tmp_files"

printf '{\n' > "$tmp_out"

file_count=0
tracked_count=0
us=$(printf '\037')

while IFS= read -r file_path; do
  [ -z "$file_path" ] && continue

  file_count=$((file_count + 1))

  rel_path=${file_path#"$CONTENT_DIR"/}

  if [ "$file_count" -gt 1 ]; then
    printf ',\n' >> "$tmp_out"
  fi

  printf '  "%s": [\n' "$(json_escape "$rel_path")" >> "$tmp_out"

  : > "$tmp_log"
  if ! git log --follow --max-count="$LIMIT" --date=iso-strict --pretty=format:%H%x1f%h%x1f%an%x1f%ae%x1f%ad%x1f%s -- "$file_path" > "$tmp_log" 2>/dev/null; then
    :
  fi

  commit_count=0
  while IFS= read -r line || [ -n "$line" ]; do
    [ -z "$line" ] && continue

    hash=${line%%"$us"*}; rest=${line#*"$us"}
    short_hash=${rest%%"$us"*}; rest=${rest#*"$us"}
    author_name=${rest%%"$us"*}; rest=${rest#*"$us"}
    author_email=${rest%%"$us"*}; rest=${rest#*"$us"}
    author_date=${rest%%"$us"*}; subject=${rest#*"$us"}

    if [ "$commit_count" -gt 0 ]; then
      printf ',\n' >> "$tmp_out"
    fi

    printf '    {"hash":"%s","shortHash":"%s","authorName":"%s","authorEmail":"%s","authorDate":"%s","subject":"%s"}' \
      "$(json_escape "$hash")" \
      "$(json_escape "$short_hash")" \
      "$(json_escape "$author_name")" \
      "$(json_escape "$author_email")" \
      "$(json_escape "$author_date")" \
      "$(json_escape "$subject")" >> "$tmp_out"

    commit_count=$((commit_count + 1))
  done < "$tmp_log"

  if [ "$commit_count" -gt 0 ]; then
    tracked_count=$((tracked_count + 1))
  fi

  printf '\n  ]' >> "$tmp_out"
done < "$tmp_files"

printf '\n}\n' >> "$tmp_out"

mv "$tmp_out" "$OUTPUT_PATH"

echo "Git history generated: $OUTPUT_PATH"
echo "Files scanned: $file_count; files with commits: $tracked_count; limit per file: $LIMIT"