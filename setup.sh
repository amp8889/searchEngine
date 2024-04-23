#!/bin/bash
# I recommend not running this if you do not have to, I didn't really have a way of testing it
# So Im not really sure if it works or not.
# Check if the script is run from the correct directory
if [ ! -f "setup.sh" ]; then
    echo "Error: Run this script from the project directory where setup.sh is located."
    exit 1
fi

# Create a Python virtual environment
python3 -m venv .venv
echo "Virtual environment created."

# Activate the virtual environment based on the OS
case "$OSTYPE" in
  darwin*)  source .venv/bin/activate ;;  # macOS
  linux*)   source .venv/bin/activate ;;  # Linux
  msys*)    source .venv/Scripts/activate ;;  # Windows
  *)
    echo "Unsupported OS: $OSTYPE"
    exit 1
    ;;
esac

echo "Virtual environment activated."

# Install required Python packages
pip install Flask scrapy scikit-learn beautifulsoup4
echo "All required packages installed."

# Instructions to deactivate virtual environment
echo "To deactivate the virtual environment, run: deactivate"
