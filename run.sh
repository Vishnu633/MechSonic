#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if .venv exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Error: Virtual environment not found at .venv"
    echo "Please create it: python3 -m venv .venv"
    echo "Then install dependencies: source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Run the script
python3 main.py
