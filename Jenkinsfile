pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/username/mini-ci-project.git'
            }
        }
        stage('Compile') {
            steps {
                sh 'javac Hello.java'
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts: '*.class'
            echo 'Build Successful - Artifact Archived'
        }
        failure {
            echo 'Build Failed'
        }
    }
}
