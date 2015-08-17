#!/bin/bash

for f in plots/*.json
do
  echo "Plotting" $f
  ./plotter.py -l $f
  if [ ! $? -eq 0 ]; then
    exit 1
  fi
done
