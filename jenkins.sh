#!/bin/bash
set -xe
set -o pipefail
set +x

echo "*"
echo "**************************************************************************************************"
echo "*"
echo
echo "*"
echo "* jenkins.sh System Info"
echo "*"
echo
echo "  POD NAME: $(hostname)"
echo "  CURRENT DIRECTORY: $(pwd)"
echo "  PYTHON VERSION:"
python3 -V
echo
echo
echo "  DISK USAGE: "
df
echo
echo "  ENVIRONMENT: "
echo
env
echo
echo "*"
echo "**************************************************************************************************"
echo "*"
set -x

function staticAnalysis() {
	echo 'Running static analysis... from jenkins.sh'
}


function build() {
	echo 'Building... from jenkins.sh'

	echo 'Setting up virtual environment...'
	pip3 install virtualenv
	mkdir -p venv
	cd venv
	pwd
	virtualenv venvironment -p python3
	source venvironment/bin/activate
	which python3

	echo 'Setting up server...'
	cd $WORKSPACE
	pwd
	ls

	echo 'Creating .env file...'
	touch .env
	echo "DJANGO_DEV='${DJANGO_ENV}'" >> .env
	echo "SECRET_KEY='${SECRET_KEY}'" >> .env
	cat .env

	echo 'Installting python dependencies...'
	pip3 install -r $WORKSPACE/server/requirements/dev.txt

	echo 'List of python packages...'
	pip3 freeze

	echo 'Setting up Django...'
	cd $WORKSPACE/server
	python3 manage.py makemigrations
	python3 manage.py migrate
}

function unitTests() {
	echo 'Running unit tests... from jenkins.sh'
	cat .env
	source $WORKSPACE/venv/venvironment/bin/activate
	which python3
	pip3 freeze
	cd $WORKSPACE/server
	python3 manage.py test apps
}

function integrationTests() {
	echo 'Running integration tests... from jenkins.sh'
	echo 'No integration tests at this time'
}

function debug() {
	echo 'Current directory: '
	pwd
	echo 'Directory contents: '
	ls
}


COMMAND=$1
shift

case $COMMAND in
	staticAnalysis )
		staticAnalysis
		;;
	build )
		build
		;;
	unitTests )
		unitTests
		;;
	integrationTests )
		integrationTests
		;;
	* )
		echo "Bad command"
		exit 1
		;;
esac
