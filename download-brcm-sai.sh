#!/bin/bash

if [[ -z "$1" ]]; then
  echo "Usage: $0 <switch to grab SAI version from>"
  exit 1
fi

echo ' [.] Searching for BRCM version artifacts...'

BRANCH="$(ssh "$1" docker exec syncd cat /usr/lib/libsai.so.1.0 | strings | grep -m1 -oE 'SAI_[0-9]+\.[0-9]+\.[0-9]+_GA')"
VERSION="$(ssh "$1" docker exec syncd cat /usr/lib/libsai.so.1.0 | strings | grep -m1 'BRCM SAI ver:' -C 1000 | grep -m1 -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$')"

set -euo pipefail

if [[ -z "${BRANCH}" ]] || [[ -z "${VERSION}" ]]; then
        echo ' [!] Could not find BRCM version strings'
        exit 1
fi

echo " [*] Detected BRCM SAI branch ${BRANCH}, version ${VERSION}"

curl -L -O "https://packages.trafficmanager.net/public/sai/sai-broadcom/${BRANCH}/${VERSION}/xgs/libsaibcm_${VERSION}_amd64.deb"
curl -L -O "https://packages.trafficmanager.net/public/sai/sai-broadcom/${BRANCH}/${VERSION}/xgs/libsaibcm-dev_${VERSION}_amd64.deb"
