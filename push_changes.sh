#!/bin/bash

echo "Rebuilding Docker container..."
docker build --target final -t web:latest .

