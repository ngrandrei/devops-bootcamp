# Kubernetes module

## Overview

- Kubernetes is the mostly used container orchestation tool.
- It offers: high availability, automatic scaling, disaster recovery and self-healing.

**Pods**

- the smallest unit of k8s
- abstraction over container 
- tipically 1 pod contains 1 container
- ephemeral 
- new IP address is assign on re-creation

**Service**

- static IP for the pods
- lifecycle of the pods and service are not connected
- load balancer between pods
- could be internal (database) or external (app accessed through browser)
- Ingress is the only entrypoint in your cluster, it forwards traffic to service

**ConfigMap**

- stores non-confidential data in key-value pairs

**Secrets**

- same as ConfigMap, but used for sesitive data

**Volumes**

- used to persist data if a pod dies (could be local or outside of k8s cluster)

**Deployment**

- abstraction over pods

**StatefulSet**

- blueprint for stateful app (ex. database)
- it makes sure that data reads and writes are synchronized to avoid data inconsistencies

---

## Kubernetes architecture

Nodes - multiple VMs or physical servers

Master node (Control plane) - manages Worker Nodes and pods in the cluster, it needs to be replicated across different machines

Worker node - containerized apps run on this. It needs much more compute resources than the Master node

Every Worker node needs 3 processes to be installed:\
    - container runtime (cri-o, docker, containerd - very lightweight)\
    - kubelet - agent that makes sure containers are running in pods, talks to server to get resources available\
    - kube-proxy - network proxy with intelligent forwarding of requests to the pods

Every Master node has 4 processes:\
    - API Server - single entrypoint to the cluster (kubectl talks to API Server) and is the gatekeeper for authtentication, validating the requests\
    - Scheduler - just decides on which Node the new pod should be scheduled. It takes into considerations resourcerequirements, hardware/software/policy constraints, data locality\
    - Controller manager - Detects state changes, like crashing of Pods and tries to recover the cluster state as soon as possible. It talks to the scheduler\
    - etcd - store for all cluster data\

As the cluster grows, you have to add more Worker and Master nodes.

Minikube - running as a docker container or as a VM to create a cluster (including all processes from Worker and Master nodes on one server)

## CLI commands

install hyperkit and minikube
brew update
brew install hyperkit
brew install minikube
kubectl
minikube

create minikube cluster
minikube start --vm-driver=hyperkit
kubectl get nodes
minikube status
kubectl version

delete cluster and restart in debug mode
minikube delete
minikube start --vm-driver=hyperkit --v=7 --alsologtostderr
minikube status

kubectl commands
kubectl get nodes
kubectl get pod
kubectl get services
kubectl create deployment nginx-depl --image=nginx
kubectl get deployment
kubectl get replicaset
kubectl edit deployment nginx-depl

debugging
kubectl logs {pod-name}
kubectl exec -it {pod-name} -- bin/bash

create mongo deployment
kubectl create deployment mongo-depl --image=mongo
kubectl logs mongo-depl-{pod-name}
kubectl describe pod mongo-depl-{pod-name}

delete deplyoment
kubectl delete deployment mongo-depl
kubectl delete deployment nginx-depl

create or edit config file
vim nginx-deployment.yaml
kubectl apply -f nginx-deployment.yaml
kubectl get pod
kubectl get deployment

delete with config
kubectl delete -f nginx-deployment.yaml
#Metrics
kubectl top The kubectl top command returns current CPU and memory usage for a cluster’s pods or nodes, or for a particular pod or node if specified.

## Project 1

**Deploy MongoDB and Mongo Express into local k8s cluster**

1. Create mongodb deployment yaml file

MongoDB needs two env variables: MONGO_INITDB_ROOT_USERNAME and MONGO_INITDB_ROOT_PASSWORD. Values for those have to be stored in a Secret config file in a base64 encoded format. To encode this, you can use `echo -n "andreinegru" | base64` to get the econded values. 

Becasue you reference values from Secret, you have to creat the Secret prior to the deployment. 

`kubectl get pods -o wide` - show more info about the pods (like IP, node)

2. Create mongodb internal service yaml file

Service and Deployment usually lives in the same yaml file.

3. Create mongo espress deployment 

It needs ME_CONFIG_MONGODB_ADMINUSERNAME and ME_CONFIG_MONGODB_ADMINPASSWORD set as env variables in order to connect to mongo db and ME_CONFIG_MONGODB_SERVER which is the MongoDB container name, but since we use pods and services, it will be the name of the mongodb service. We can store this in a ConfigMap since is not sensitive data.

4. Create mongo express service 

This have to be created as a loadbalancer (external service) in order to access it from the browser.





