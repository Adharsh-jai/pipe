pipeline {
    agent any

    environment {
        IMAGE_NAME = "menu-app"
    }

    stages {

        stage('Checkout') {

            steps {

                script {

                    try {

                        git branch: 'main',
                        url: 'https://github.com/Adharsh-jai/pipe.git'

                        echo "Repository cloned successfully"

                    } catch (Exception e) {

                        echo "Checkout Failed: ${e}"

                        error("Stopping Pipeline")

                    }
                }
            }
        }

        stage('SonarQube Analysis') {

            environment {
                SCANNER_HOME = tool 'SonarScanner'
            }

            steps {

                script {

                    try {

                        withSonarQubeEnv('SonarQube') {

                            sh """
                            ${SCANNER_HOME}/bin/sonar-scanner \
                            -Dsonar.projectKey=my-project-key \
                            -Dsonar.projectName=my-project-name \
                            -Dsonar.sources=.
                            """
                        }

                        echo "SonarQube Analysis Completed"

                    } catch (Exception e) {

                        echo "SonarQube Analysis Failed: ${e}"

                        error("Stopping Pipeline")

                    }
                }
            }
        }

        stage('Quality Gate') {

            steps {

                script {

                    try {

                        waitForQualityGate abortPipeline: false

                        echo "Quality Gate Passed"

                    } catch (Exception e) {

                        echo "Quality Gate Failed: ${e}"

                        error("Stopping Pipeline")

                    }
                }
            }
        }

        stage('Build Docker Image') {

            steps {

                script {

                    try {

                        sh """
                        docker build -t ${IMAGE_NAME} .
                        """

                        echo "Docker Image Built Successfully"

                    } catch (Exception e) {

                        echo "Docker Build Failed: ${e}"

                        error("Stopping Pipeline")

                    }
                }
            }
        }
    }

    post {

        success {
            echo "Pipeline Executed Successfully"
        }

        failure {
            echo "Pipeline Failed"
        }

        always {
            echo "Pipeline Finished"
        }
    }
}
