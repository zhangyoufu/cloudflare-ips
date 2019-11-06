#!/bin/bash
set -ex
set -o pipefail

for FILENAME in ips-v4 ips-v6; do
    curl --silent --show-error "https://www.cloudflare.com/${FILENAME}" | .github/sort.py >"${FILENAME}"
done

if [ -n "$(git status --porcelain)" ]; then
    git config --global user.name 'GitHub Actions'
    git config --global user.email "$(whoami)@$(hostname --fqdn)"
    git add --all
    git commit --all --message 'IP ranges updated'
    git push "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git" HEAD:master
fi
