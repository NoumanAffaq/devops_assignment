pipeline {
    agent any

    environment {
        GIT_CREDS = "git-repo-access"
    }

    stages {

        stage('SSH Connection') {
            steps {
                script {
                    withCredentials([string(credentialsId: "${GIT_CREDS}", variable: 'GIT_TOKEN')]) {
                        sshagent(credentials: ['ec2-id-devops_assignment']) {
                            // Run the uname command on the remote machine
                      sh """ssh -o StrictHostKeyChecking=no ubuntu@54.198.228.247'
                            (
                            rm -r devops_assignment &&
                            git clone -b devops_dev https://${GIT_TOKEN}@github.com/NoumanAffaq/devops_assignment.git) &&
                            cd devops_assignment &&
                            docker-compose down -v &&
                            cd .. ||
                            (cd devops_assignment &&
                            rm -r devops_assignment &&
                            git clone -b devops_dev https://${GIT_TOKEN}@github.com/NoumanAffaq/devops_assignment.git)
                            '"""

                        }
                    }
                }
            }
        }
            stage('devops_assignment') {
    steps {
        script {
            sshagent(credentials: ['ec2-id-auth_service']) {
                echo "deploying"
                // Run the uname command on the remote machine
                sh """ssh -o StrictHostKeyChecking=no ubuntu@54.198.228.247'
                    cd devops_assignment &&
                    docker-compose build && docker-compose up -d'"""
            }
        }
    }
}

        // Add more stages as needed
    }



        // Add more stages as neede
    post {
        always {
            // Clean up resources if needed
            cleanWs()
        }
    }
}