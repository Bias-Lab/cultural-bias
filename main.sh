#!/bin/bash

# Llama3
echo "/bye" | ollama run llama3
export MODEL=llama3
nohup python3 main.py --mode=local &
echo "Running llama3 done"

pid=$!

wait $pid

#git add .
#git commit -m "add llama3 data"

# Gemma
echo "/bye" | ollama run gemma
export MODEL=gemma
nohup python3 main.py --mode=local &
echo "Running gemma done"

pid=$!

wait $pid

#git add .
#git commit -m "add gemma data"
