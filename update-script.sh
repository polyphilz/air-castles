#!/bin/sh
cd worker-utils

if poetry run bw; then
  if poetry run uw; then
    echo "Successfully built and uploaded Worker Script."
  else
    echo "Exit code $?: Failed to upload Worker Script."
  fi
else
    echo "Exit code $?: Failed to build Worker Script."
fi

cd ../
