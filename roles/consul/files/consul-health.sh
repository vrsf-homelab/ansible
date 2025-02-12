#!/usr/bin/env bash

URL=${1:-"http://127.0.0.1:8500/ui/"}
STATUS_OK=${2:-200}

response=$(curl --insecure --write-out "%{http_code}" --silent --output /dev/null "$URL")

if [ "$response" -eq "$STATUS_OK" ]; then
  echo "Response OK"
  exit 0
else
  echo "Response FAILED"
  exit 1
fi
