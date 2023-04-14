#!/bin/bash

# Execute using `source setup_envs.sh`

read -p "PYTHON VERSION? " VERSION # 3.6, 3.7, 3.8, etc.
python${VERSION} -m venv env
source env/bin/activate
pip install -r requirements.txt
