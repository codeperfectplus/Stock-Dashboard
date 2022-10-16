#!/bin/bash
cd /app

nohup python3 dash_server.py &
tail -100f nohup.out
