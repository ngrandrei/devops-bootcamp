# Jenkins module

## Project 1

**Install Jenkins on an EC2 as a Docker container**

I used a t2.large which has 2vCPU and 8 GiB Memory.
Security group inbound rules - allow for SSH on port 22 and HTTP on 8080. Default outbound rules are to allow everything.


1. Connect to the instance using ssh agent
`ssh -i "~/Downloads/key.pem" ubuntu@publiciphere`

2. Install Docker
`sudo apt update`
`sudo apt install docker.io`

`sudo groupadd docker` create a group called docker in case it's not created atomatically in installing docker.
`sudo usermod -aG docker ${USER}` add your user (ubuntu in this case) to that group in order to execute docker commands without sudo.

    and exit and reconnect to the EC2 through ssh

3. Start the Jenkins container

```
docker run -p 8080:8080 -p 50000:50000 -d \
-v jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11
```

port 8080 - accessing the Jenkins UI through browser
port 50000 - where the communication between Jenkins master and worker nodes happens

4. Initialize Jenkins

You can now connect to Jenkins UI using the public ip of the instance and the port 8080.

`docker container exec -it 213528dbf6e2 bash` - used to open the terminal inside container
`cat /var/jenkins_home/secrets/initialAdminPassword` - to retreive the admin password that you need in the Jenkins UI
