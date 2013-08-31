#!/bin/bash -e
# Prerequisites:
# git clone https://github.com/typpo/azoo-testbed.git
# git clone https://github.com/typpo/hcompress-unix.git
#

sudo apt-get install -y build-essential python-virtualenv python-pip python-dev csh htop

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
