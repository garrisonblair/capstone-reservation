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
echo "  JAVA VERSION:"
java -version
echo
echo "  MAVEN VERSION:"
mvn -version
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
}

function sonar() {
	echo 'Running unit tests... from jenkins.sh'
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