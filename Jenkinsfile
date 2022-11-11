@Library('caelum@85c38e9f32f013f2e9d194fd133b8623c758e7b3') _

pipeline {
    agent {
        docker {
            image '169.254.149.20:6001/arch_python_baw_ghost_opencv:0.15.1'
            args  '-v $WORKSPACE:/var/workdir'
        }
    }

    parameters {
        string(name: 'BRANCH', defaultValue: 'master')
        booleanParam(name: 'RELEASE', defaultValue: false)
    }

    stages{
        stage('sync'){
            steps{
                sh 'baw sync all'
                sh 'baw sh "pip install ."'
            }
        }
        stage('doctest'){
            steps{
                sh 'baw test docs -n1'
            }
        }
        stage('fast'){
            steps{
                sh 'baw test fast -n5'
            }
        }
        stage('long'){
            steps{
                sh 'baw test long -n8'
            }
        }
        stage('lint'){
            steps{
                sh 'baw lint'
            }
        }
        stage('generate'){
            steps{
                sh 'baw test skip --generate'
            }
        }
        stage('all'){
            steps{
                sh 'baw test all -n32 --cov --junit_xml=report.xml'
                junit '**/report.xml'
            }
            post{
                failure{script{publish.resource_generated()}}
            }
        }
        stage('release'){
            when {
                expression { return params.RELEASE }
            }
            steps{
                sh 'baw install && baw release && baw publish'
                // TODO: GIT COMMIT?
            }
        }
    }
}
