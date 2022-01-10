#!/usr/bin/bash
##
## Even though this file is set up as a bash script, you really need
## to 'source' it in order for the python environment activation to
## work correctly.  Or you can simply activate the environment by
## hand.
##

# Update your Anaconda environment to latest version (optional)
# conda update -n base -c defaults conda

# Build Python virtual environment for Maestro
conda create -n maestro-webex-bot python~=3.9.1 -y

# Activate the environment
conda activate maestro-webex-bot

# Next, dependencies needed to project setup
pip install -r requirements.txt
