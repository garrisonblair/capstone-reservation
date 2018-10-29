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
	pycodestyle --exclude='**/migrations/**, **/__init__.py' --config='./../../setup.cfg' server
	source source $WORKSPACE/venv/venvironment/bin/activate}
    #coverage run irisvmpy/iris.py 1 1 2 3
    python -m coverage xml -o ./reports/coverage.xml
    tox -e coverage
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

	echo 'Setting up server...'
	cd $WORKSPACE
	pwd
	ls

	echo 'Creating .env file...'
	touch .env
	echo "DJANGO_DEV='${DJANGO_ENV}'" >> .env
	echo "SECRET_KEY='${SECRET_KEY}'" >> .env
	# cat .env

	echo 'Installting python dependencies...'
	pip3 install -r $WORKSPACE/server/requirements/dev.txt

	# echo 'List of python packages...'
	# pip3 freeze

	echo 'Setting up Django...'
	cd $WORKSPACE/server
	python3 manage.py makemigrations
	python3 manage.py migrate
}

function unitTests() {
	echo 'Running unit tests... from jenkins.sh'
	source $WORKSPACE/venv/venvironment/bin/activate
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
