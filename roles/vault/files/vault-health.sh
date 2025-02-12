#!/usr/bin/env bash

URL=${1:-"https://localhost:8200/v1/sys/health"}
STATUS_OK=${2:-200}

response=$(curl --insecure --write-out "%{http_code}" --silent --output /dev/null "$URL")

if [ "$response" -eq "$STATUS_OK" ]; then
  echo "Response OK"
  exit 0
else
  echo "Response FAILED"
  exit 1
fi
