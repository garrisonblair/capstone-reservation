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
	#curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	#python get-pip.py
	#pip3 install -r server/requirements/dev.txt
	#cd server
	#python3 manage.py makemigrations
	#python3 manage.py migrate
	#python3 manage.py createsuper

	echo "Currently in: "
	pwd
	echo "Contents of directory are: "
	ls
}

function unitTests() {
	echo 'Running unit tests... from jenkins.sh'
	#python3 ./manage.py test --patten="**/tests/*.py"
	cd server
	python3 manage.py test apps
}

function integrationTests() {
	echo 'Running integration tests... from jenkins.sh'
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