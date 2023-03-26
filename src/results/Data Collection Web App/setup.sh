#!/bin/bash

echo "Begin Deployment.."

if [ -d "venv" ];
then
	source ./venv/bin/activate
else
	echo "Virtual environment does not exist. Creating one..."
	pip install -q virtualenv
	virtualenv venv
	source ./venv/bin/activate
fi

echo "Virtual Environment: venv - Activated"

echo "Installing dependencies..."
pip install -q -r requirements.txt

export DEPLOYMENT_ENV="Development"
echo "Running on ${DEPLOYMENT_ENV} server"

echo "Enter secrets to setup.sh for api authentication if not done already.."

# SECRETS
export auth_email="<your auth email>"
export auth_pass="<your private key json file path>"


python main.py
