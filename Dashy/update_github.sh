#!/bin/bash

# Change to the directory of your Git repository
cd /home/kaj/homelab

# Add all changes to the staging area
git add *

# Commit changes with a default message
git commit -m "Automated commit $(date)"

# Push changes to the default branch
git push origin main