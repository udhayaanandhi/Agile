pipeline {
    agent any
    stages {
        stage('Compile') {
            steps {
                bat 'javac Hello.java'
            }
        }
        stage('Run') {
            steps {
                bat 'java Hello'
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
