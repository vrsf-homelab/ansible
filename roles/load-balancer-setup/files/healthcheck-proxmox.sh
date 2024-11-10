#!/bin/bash

if [ $# -ne 1 ]; then
  echo "WARNING: You must provide health check URL"
  exit 1
else
  CHECK_URL=$1
  CMD=$(/usr/bin/curl -k -I -m 1 ${CHECK_URL} 2>/dev/null | grep "HTTP/1.1 501 method 'HEAD' not available" | wc -l)

  if [ ${CMD} -eq 1 ]; then
    echo "ONLINE!"
    exit 0
  else
    echo "OFFLINE!"
    exit 1
  fi
fi
