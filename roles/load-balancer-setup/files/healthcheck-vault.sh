#!/bin/bash

if [ $# -ne 1 ]; then
  echo "WARNING: You must provide health check URL"
  exit 1
else
  CHECK_URL=$1
  CMD=$(/usr/bin/curl -k -I ${CHECK_URL} 2>/dev/null | grep "HTTP/2 200" | wc -l)

  if [ ${CMD} -eq 1 ]; then
    echo "Vault is ONLINE!"
    exit 0
  else
    echo "Vault is OFFLINE!"
    exit 1
  fi
fi
