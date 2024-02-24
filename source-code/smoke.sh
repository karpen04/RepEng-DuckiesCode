#!/bin/bash

# Script Name: smoke.sh
# Description: This script checks if Python 3 is installed and prints the installed version.
# Author: Oleksandr Karpenko, karpen04@ads.uni-passau.de
# Version: 1.0
# SPDX-License-Identifier: MIT
#
# Usage: ./smoke.sh

# Check if Python is installed
if command -v python3 &>/dev/null; then
    echo "Python is installed"
    
    # Get Python version
    pythonVersion=$(python3 --version 2>&1)
    echo "Installed Python version: $pythonVersion"
else
    echo "Python is not installed"
fi
