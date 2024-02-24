#!/bin/bash

# Script Name: doAll.sh
# Description: This script executes all scripts in order.
# Author: Oleksandr Karpenko, karpen04@ads.uni-passau.de
# Version: 1.1
# SPDX-License-Identifier: MIT
#
# Usage: ./doAll.sh

echo "Running smoke.sh"
bash ./smoke.sh

echo "Running solver_optimization.py"
python3 solver_optimization.py

echo "Building a report and cleaning up cahce files..."
cd ~/report
make report

echo "Report .pdf should be in the report folder. To clean cache files and delete report execute "make clean" in report folder"
cd ~/scripts

