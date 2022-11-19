# Jenkins module

## Project 1

**Install Jenkins on an EC2 as a Docker container**

I used a t2.large which has 2vCPU and 8 GiB Memory.
Security group inbound rules - allow for SSH on port 22 and HTTP on 8080. Default outbound rules are to allow everything.


1. Connect to the instance using ssh agent
`ssh -i "~/Downloads/key.pem" ubuntu@publiciphere`

2. Install Docker
`sudo apt update`\
`sudo apt install docker.io`\

`sudo groupadd docker` create a group called docker in case it's not created atomatically in installing docker\
`sudo usermod -aG docker ${USER}` add your user (ubuntu in this case) to that group in order to execute docker commands without sudo\

    and exit and reconnect to the EC2 through ssh

3. Start the Jenkins container

```
docker run -p 8080:8080 -p 50000:50000 -d \
-v jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11
```

port 8080 - accessing the Jenkins UI through browser\
port 50000 - where the communication between Jenkins master and worker nodes happens\

4. Initialize Jenkins

You can now connect to Jenkins UI using the public ip of the instance and the port 8080.

`docker container exec -it 213528dbf6e2 bash` - used to open the terminal inside container\
`cat /var/jenkins_home/secrets/initialAdminPassword` - to retreive the admin password that you need in the Jenkins UI\

--- 

## Project 2

**CI Pipeline to build and push to a private repo a java maven app**

1. Install Maven either in the Jenkins UI or directly in the container

Note: 
- job’s infor is stored in `/var/jenkins_home/jobs/my-job/builds`
- cloned repo is stored in `/var/jenkins_home/workspace/my-job`

2. Specify Git repo and execute shell scripts:
`cd ./Module_8-CICD_with_Jenkins/java-maven-app-master && mvn test` - run tests\
`cd ./Module_8-CICD_with_Jenkins/java-maven-app-master && mvn package ` - build artifact\ 

The jar file is stored under `/var/jenkins_home/workspace/my-freestyle-job/Module_8-CICD_with_Jenkins/java-maven-app-master/target` with the name\
`java-maven-app-1.1.0-SNAPSHOT.jar` because that's the name specified in pom.xml\

3. Make Docker available in Jenkins 

This is done by mounting docker runtime from host to the jenkins container.\
`docker run -d -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):/usr/bin/docker jenkins/jenkins:lts`\  --> does not work as expected, I had to install docker manually inside container.\

Use this command instead: `docker run -p 8080:8080 -p 50000:50000 -d -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts`\
Enter inside container as root and run `curl https://get.docker.com/ > dockerinstall && chmod 777 dockerinstall && ./dockerinstall`\
then exit the jenkins container and change docker.sock privilege to read and write for all users with :
`sudo chmod 666 /var/run/docker.sock`. Now you have docker inside Jenkins.\

4. Build the docker image and publish it to DockerHub

First create a repo for your Image on Docker Hub, then you have to add credentials to Jenkins in order to access your DockerHub.\
Go to Dashboard -> Manage Jenkins -> Manage Credentials -> Jenkins -> Global credentials -> Add Credentials (left sidebar)\
Create credentials to access your Docker Hub account.\

Create the Dockerfile in `java-maven-app-master` directory.\





