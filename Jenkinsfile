pipeline {

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
                echo 'Running code coverage.. in Jenkinsfile'
                sh  ''' source activate ${BUILD_TAG}
                        coverage run irisvmpy/iris.py 1 1 2 3
                        python -m coverage xml -o ./reports/coverage.xml
                    '''
            }
            post{
                always{
                    step([$class: 'CoberturaPublisher',
                                   autoUpdateHealth: false,
                                   autoUpdateStability: false,
                                   coberturaReportFile: 'reports/coverage.xml',
                                   failNoReports: false,
                                   failUnhealthy: false,
                                   failUnstable: false,
                                   maxNumberOfBuilds: 10,
                                   onlyStable: false,
                                   sourceEncoding: 'ASCII',
                                   zoomCoverageChart: false])
                }
            }
        }
        stage('Static Analysis') {
            when {
                expression { params.skipStaticAnalysis == false }
            }
            steps {
                echo 'Running static analysis.. in Jenkinsfile'
                 echo "PEP8 style check"
                sh  ''' source activate ${BUILD_TAG}
                        pylint --disable=C irisvmpy || true
                    '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building.. in Jenkinsfile'
                buildApplication()
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
        }
        stage('Integration Tests') {
            when {
                expression { params.skipIntegrationTests == false }
            }
            steps {
                echo 'Running integration tests in Jenkinsfile...'
                runIntegrationTests()
            }
        }
    }
    post {
        success {
            buildSuccess()
        }
        failure {
            buildFailure()
        }
        unstable {
            buildFailure()
        }
    }
}


def runStaticAnalysis() {
    sh './jenkins.sh staticAnalysis'
}

def buildApplication() {
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
    slackSend color: "#aa0a0a", message: "Build Failed: ${env.JOB_NAME} ${env.BUILD_NUMBER} ${env.GIT_BRANCH}"
}

def buildSuccess() {
    echo 'build succeeded'
    slackSend color: "#43e045", message: "Build Succeeded: ${env.JOB_NAME} ${env.BUILD_NUMBER} ${env.GIT_BRANCH}"
}