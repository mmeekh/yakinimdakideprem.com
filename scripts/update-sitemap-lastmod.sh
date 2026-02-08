#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
public_dir="${repo_root}/public"
sitemap_file="${public_dir}/sitemap.xml"

if [[ ! -f "${sitemap_file}" ]]; then
  echo "Sitemap not found: ${sitemap_file}" >&2
  exit 1
fi

tmp_file="$(mktemp)"

awk -v public_dir="${public_dir}" '
function trim(value) {
  gsub(/^[ \t\r\n]+|[ \t\r\n]+$/, "", value)
  return value
}

function loc_to_file(loc, path) {
  path = loc
  sub(/^https?:\/\/[^\/]+/, "", path)
  sub(/\?.*$/, "", path)
  sub(/#.*/, "", path)

  if (path == "" || path == "/") {
    return public_dir "/index.html"
  }
  if (path ~ /\/$/) {
    return public_dir path "index.html"
  }
  return public_dir path
}

function file_date(filepath, cmd, out) {
  cmd = "date -u -r \"" filepath "\" +%F 2>/dev/null"
  cmd | getline out
  close(cmd)
  return out
}

{
  if ($0 ~ /<loc>/) {
    loc = $0
    sub(/^.*<loc>/, "", loc)
    sub(/<\/loc>.*$/, "", loc)
    current_file = loc_to_file(trim(loc))
    current_date = file_date(current_file)
    print $0
    next
  }

  if ($0 ~ /<lastmod>/ && current_date != "") {
    indent = ""
    if (match($0, /^[ \t]*/)) {
      indent = substr($0, RSTART, RLENGTH)
    }
    print indent "<lastmod>" current_date "</lastmod>"
    next
  }

  print $0
}
' "${sitemap_file}" > "${tmp_file}"

mv "${tmp_file}" "${sitemap_file}"
echo "Updated ${sitemap_file}"
