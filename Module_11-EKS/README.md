# EKS

## Project 1

**Create AWS EKS Cluster with a Node Group**

EKS - managed container service to run an scale K8s applications.\
EKS deploys and manages the Control plane nodes in different AZs for High Availability.

Host the Worker nodes - on EC2 - you need to manage infrastructure of the worker nodes\
                      - on Nodegroup - semi-managed, creates, deletes EC2 for you, but you need to configure it\
                      - Fargate - fully managed Worker nodes

1. Create AWS EKS IAM Role

Assign role to the EKS cluster managed by AWS to allow AWS to create and manage components on our behalf.

EKS Cluster usecase with - `AmazonEKSClusterPolicy` policy.

2. Create VPC for EKS Worker Node

Worker Nodes need specific Firewall configurations for Control Plane-Worker communication because Control plane nodes are in AWS managed account and Worker nodes in my account. Best practice configuration is Public and Private subnets.

Use CloudFormation template: https://docs.aws.amazon.com/codebuild/latest/userguide/cloudformation-vpc-template.html

3. Create EKS Cluster 

4. Connect to EKS cluster with kubectl from local machine

You need a kubeconfig file in order to communicate with k8s cluster./
`aws eks update-kubeconfig --name eks-cluster-name` - adds the info to ./kube/config necessarely for kubectl to communicate with eks cluster./

5. Create Node groups and attach worker nodes k8s

Kubelet - main k8s process on Worker nodes which communicate with other AWS services, schedules and manages Pods.\
It needs permissions to perform certain actions.\
Need to create an EC2 role with `AmazonEKSWorkerNodePolicy`, `AmazonEC2ContainerRegistryReadOnly` and `AmazonEKS_CNI_Policy` - internal network in k8s.\

Create Node group and attach the role recently created to it. 

6. Configure Auto-scaling for Worker Nodes

AWS doesn't automatically autoscale our resources. We need to configure K8s Autoscaler in our K8s cluster. If Autoscaler notices that two EC2 instances are under-utilise, will take the pods and schedule them on other Nodes and terminates the two EC2s.

Create a custom policy to allow autoscaling and attach it to the Role for Node groups. https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html

`curl -o cluster-autoscaler-autodiscover.yaml https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml` - download the yaml file for Autoscaler\
`kubectl apply -f cluster-autoscaler-autodiscover.yaml` - deploy Autoscaler in EKS kube-system namespace

Autoscaler version needs to match cluster k8s version.

It saves costs but provisioning a new EC2 instance takes time.

7. Deploy an nginx app into cluster

`kubectl apply -f nginx-config.yml` - created the nginx service in k8s and also the cloud native load balancer in AWS

Requets will come on port 80 on AWS LoadBalancer, then will be forwarded to port 30204 on EC2 Node and then to port 80 of nginx service in k8s.

---

## Project 2

**Create EKS Cluster with Fargate profile**

- Serverless - AWS will create VMs on AWS account./
- 1 pod per VM\
- no support for Statefull apps or DaemonSets\

You can have both Fargate and Node groups as Worker nodes.

1. Create Role for Fargate ( EKS - Fargate Pod )

It's used to schedule pods on new VM.

2. Create Fargate profile

Pod selection rule - tell Fargate that a pod should be scheduled through Fargate.\
We need to provide our VPC becasue the Pods will have an IP address from our subnet IP range. (only private subnets)

In AWS specify namespace and match labels, ex `profile: fargate` and create `nginx-config-fargate.yaml`. 

--- 

## Project 3

**Create EKS Cluster with eksctl tool**

Simpler method than using the Console UI.

Cluster will be created with default params.\

1. Install the Homebrew tap

`brew tap weaveworks/tap`

2. Install eksctl

`brew install weaveworks/tap/eksctl`

3. Create cluster 

`eksctl create cluster --name negru-cluster --version 1.22 --region eu-east-1 --nodegroup-name negru-nodes --node-type t2.micro --nodes 2 --nodes-min 1 --nodes-max 3`

---

## Project 4

**Complete CI/CD Pipeline with EKS and private DockerHub registry**

1. Install kubectl and aws-iam-authenticator in the Jenkins container

2. Create deployment and service yaml for the Java app in Module_8-CICD_with_Jenkins

3. Create authentication of the k8s cluster with the private docker repo

`kubectl create secret docker-registry my-registry-key --docker-server=docker.io --docker-username=negru1andrei --docker-password=password`

4. Deploy configuration files with kubectl 

Before passing the yaml file to kubectl, you need to substitute all the env variables in the yaml files - can be done using `envsubst`. Install envsubst in Jenkins container.

`envsubst < kubernetes/deployment.yaml | kubectl apply -f -` - substitute all the env variables values in the yaml file and give that file to kubectl\
`envsubst < kubernetes/service.yaml | kubectl apply -f -`

--- 

## Project 5

**Complete CI/CD Pipeline with EKS and AWS ECR**

1. Create ECR repo

Each repo is 1 app which can contains multiple tags

2. Authenticate to the ECR registry

`aws ecr get-login-password | docker login --username AWS --pasword-stdin registry-URL`

3. Create credentials in Jenkins for AWS name ecr-credentials

4. Create Secret for AWS ECR

`kubectl create secret docker-registry my-registry-key-ecr --docker-server=registry-URL --docker-username=AWS --docker-password=password`

5. Use the Jenkinsfile-ECR 
