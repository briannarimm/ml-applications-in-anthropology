#!/usr/bin/env bash
# Builds this project for Cloudflare Workers. Workers Builds runs this file.
# GitHub Pages does not use it. It copies the same files GitHub Pages publishes:
# every tracked file except hidden paths, paths that start with "_", and the Cloudflare files.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf .cloudflare-dist
OUT=.cloudflare-dist/ml-applications-in-anthropology
mkdir -p "$OUT"
git ls-files -z | while IFS= read -r -d '' f; do
  case "/$f" in
    */.*|*/_*|/wrangler.jsonc|/cloudflare/*) continue ;;
  esac
  mkdir -p "$OUT/$(dirname "$f")"
  cp "$f" "$OUT/$f"
done
echo "Copied $(find "$OUT" -type f | wc -l | tr -d ' ') files to $OUT/."
