pipeline {

    // see https://jenkins.io/doc/book/pipeline/jenkinsfile/
    // see https://jenkins.io/doc/book/pipeline/syntax/
    
    agent any

    parameters {

        booleanParam(defaultValue: false, description: 'Determines whether to skip static analysis', name: 'skipStaticAnalysis')
        booleanParam(defaultValue: false, description: 'Determines whether to skip the unit tests', name: 'skipUnitTests')
        booleanParam(defaultValue: false, description: 'Determines whether to skip the integration tests', name: 'skipIntegrationTests')
    
    }
    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '5'))

    }
    stages {
        stage('Show current environment variables') {
            steps {
                echo env.GIT_BRANCH
                echo env.PIPELINE_ID
                echo env.HOME
                echo env.PATH
                echo env.NODE_NAME
                echo env.USER
            }
        }
        stage('Static Analysis') {
            when {
                expression { params.skipStaticAnalysis == false }
            }
            steps {
                echo 'Running static analysis.. in Jenkinsfile'
                runStaticAnalysis()
            }
            post {
                failure {
                    buildFailure()
                }
                unstable {
                    buildFailure()
                }
            }
        }
        stage('Build') {
            steps {
                echo 'Building.. in Jenkinsfile'
                build()
            }
            post {
                failure {
                    buildFailure()
                }
                unstable {
                    buildFailure()
                }
            }
        }
        stage('Unit Tests') {
            when {
                expression { params.skipUnitTests == false }
            }
            steps {
                echo 'Running Unit tests in Jenkinsfile...'
                runUnitTests()
            }
            post {
                failure {
                    buildFailure()
                }
                unstable {
                    buildFailure()
                }
            }
        }
        stage('Integration Tests') {
            when {
                expression { params.skipIntegrationTests == false }
            }
            steps {
                echo 'Running integration tests in Jenkinsfile...'
                runIntegrationTests()
            }
            post {
                failure {
                    buildFailure()
                }
                unstable {
                    buildFailure()
                }
            }
        }
    }
}


def runStaticAnalysis() {
    sh './jenkins.sh staticAnalysis'
}

def build() {
    sh './jenkins.sh build'
}

def runUnitTests() {
    sh './jenkins.sh unitTests'
}

def runIntegrationTests() {
    sh './jenkins.sh integrationTests'
}

def buildFailure() {
    echo 'build failed'
}