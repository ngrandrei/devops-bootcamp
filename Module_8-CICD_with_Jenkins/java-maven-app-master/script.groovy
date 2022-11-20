def buildJar() {
    sh "cd ./Module_8-CICD_with_Jenkins/java-maven-app-master/"
    sh 'mvn package'
} 

def buildImage() {
    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        //note: usernamePassword() requires the credentials to be of the kind "username with password".
        sh "docker build -t negru1andrei/java-maven-app:2.0.0 ."
        sh "echo $PASS | docker login -u $USERNAME --password-stdin"
        sh "docker push negru1andrei/java-maven-app:2.0.0"
    }
} 

def deployApp() {
    echo 'deploying the application...'
} 

return this