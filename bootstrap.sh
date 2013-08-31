#!/bin/bash -e
# Prerequisite: git clone https://github.com/typpo/azoo-testbed.git
#

sudo apt-get install -y build-essential python-virtualenv python-pip htop

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
