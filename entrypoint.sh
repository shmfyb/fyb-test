#!/bin/bash
if [[ "$1" == "server" ]]; then
  consul agent -server -ui -bootstrap-expect=1 -client=0.0.0.0 -data-dir=/consul/data -config-dir=/consul/conf -node server;
else
  pip3 install -r /app/requirements.txt
  python3 /app/app.py
fi