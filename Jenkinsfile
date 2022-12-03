@Library('caelum@108f81811f363bfda4a3fd6110a5c190e56b2fa0') _

pipeline{
    agent{
        docker{
            image '169.254.149.20:6001/arch_python_git_ghost_opencv_baw:v1.27.0'
        }
    }
    stages{
        stage('setup'){
            steps{script{baw.setup()}}
        }
        stage('test'){
            failFast true
            parallel{
                stage('doc'){
                    steps{
                        script{baw.doctest()}
                    }
                }
                stage('fast'){
                    steps{
                        script{baw.fast()}
                    }
                }
                stage('long'){
                    steps{
                        script{baw.longrun()}
                    }
                }
            }
        }
        stage('quality'){
            failFast true
            parallel{
                stage('lint'){
                    steps{
                        script{baw.lint()}
                    }
                }
                stage('format'){
                    steps{
                        script{baw.format()}
                    }
                }
            }
        }
        stage('generate'){
            steps{
                sh 'baw --docken generate all'
            }
            post{
                always{script{publish.generated()}}
            }
        }
        stage('all'){
            steps{
                sh 'baw --docken test all -n32'
                //script{baw.all()}
            }
        }
        stage('release'){
            steps{
                script{publish.release()}
            }
        }
    }
}
