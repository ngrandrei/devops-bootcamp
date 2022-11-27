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
- it is a local volume type which can store individual key-value pairs which are passed as env variables to the app/pods or you can store a file which can be mounted inside the container (use case: config file used by the app)

**Secrets**

- same as ConfigMap, but used for sesitive data

**Volumes**

- used to persist data if a pod dies (could be local or outside of k8s cluster)

**Deployment**

- abstraction over pods
- it does not depened on previous data (also called stateless)

**StatefulSet**

- blueprint for stateful app (ex. database)
- it makes sure that data reads and writes are synchronized to avoid data inconsistencies
- it maintains a sticky identity for each of their pods
- pods are not interchangeable
- pods can't be created/deleted at the same time
- name of the pod in composed of $(statefulset name)-$(oridnal)

Scaling DB apps:
- only 1 replica can make changes
- each replica has it's own storage and those are constantly synchronized

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

## Persisting data in Kubernetes using volumes

- Persistent volume - provisioned by admin or dynamically using Storage class\
                    - not namespaced\
                    - local volume types violate the 2 principals of data persistency: - being tied to 1 specific node and not surviving in case of cluster crash
- Persistent volume claim - a request for storage by a user
- Storage class - provisions PV dynamically only when PVC claims it (kinda on demand storage)\
                - pod claims storage via PVC which requests storge from Storage class which creates a PV that meets the needs of the claim


## Project 1

**Deploy MongoDB and Mongo Express into local k8s cluster**

1. Create mongodb deployment yaml file

MongoDB needs two env variables: MONGO_INITDB_ROOT_USERNAME and MONGO_INITDB_ROOT_PASSWORD. Values for those have to be stored in a Secret config file in a base64 encoded format. To encode this, you can use `echo -n "andreinegru" | base64` to get the econded values. (-n option is used to omit echoing trailing newline)

Becasue you reference values from Secret, you have to creat the Secret prior to the deployment. 

`kubectl get pods -o wide` - show more info about the pods (like IP, node)

2. Create mongodb internal service yaml file

Service and Deployment usually lives in the same yaml file.

3. Create mongo espress deployment 

It needs ME_CONFIG_MONGODB_ADMINUSERNAME and ME_CONFIG_MONGODB_ADMINPASSWORD set as env variables in order to connect to mongo db and ME_CONFIG_MONGODB_SERVER which is the MongoDB container name, but since we use pods and services, it will be the name of the mongodb service. We can store this in a ConfigMap since is not sensitive data.

4. Create mongo express service 

This have to be created as a loadbalancer (external service) in order to access it from the browser.

Use `minikube service mongo-express-service` to assign an external IP to the Mongo Express service in order to access it via browser.

---

## Project 2

***Deploy Mosquitto message broker using ConfigMap and Secret Volume types**

1. Create Mosquitto ConfigMap with the `mosquitto.conf` file and the content of the file beginning with |

2. Create Mosquitto Secret with the `secret.file` file and the content of the file beginning with | (content must be base64 encoded)

3. Create Mosquitto deployment

Use `eclipse-mosquitto:1.6.2` image to build the container and specify wich volumes can be mounted inside the containers.\
Inside the container mount the volumes under the `volumeMounts:`.

4. Enter the mosquitto contianer and validate the files are there

Use `kubectl exec -it mosquitto-5887d7ffcb-s6nct -- /bin/sh` to get inside the container in the pod.

---

## Project 3

**Deploy a Stateful app (MongoDB) using Helm**

When you want to create a K8s cluster in Cloud is better to choose a managed one, becasue you care only about the worker nodes, use cloud native load balancer for ingress controller and use the cloud storage. Examples of Cloud providers: AWS, Azure, Google, Linode.

Helm is a package manager for K8s. It packages  YAML files and distributes them in public and private repositories.\
Helm Charts contains:
- description of Helm package in Chart.yaml
- 1 or more templates that contains yaml manifests for k8s\

Use existing oficial charts ex: MySQL or Elasticsearch

Helm Chart structure:
- top level mychart folder = name of the chart\
    - Chart.yaml = metadata about chart
    - values.yaml = values for the template files
    - charts folders = chart dependencies
    - templates folder = acutal template files

Use case - Deploy the same bundle of K8s YAML files across multiple clusters (Dev, Stage, Prod). 

1. Created K8s cluster on Linode Kubernetes Engine

To work with the cluster and execute kubectl commands egainst it you have to set env variable KUBECONFIG=kubeconfig.yaml

2. Deploy replicated MongoDB (StatefulSet using Helm Chart) and configured Data Persistence with Linode Block Storage

`helm repo add bitnami https://charts.bitnami.com/bitnami` - add the repo\
`helm search repo bitnami` - see all charts in this repo\
Charts provide default values which you can override.\

`helm install mongodbmyname --values mongo-override-chart.yaml bitnami/mongodb` - mongodbmyname is the stateful set name\
`kubectl get all` - get every resource pods, services, deployments, etc\

3. Deploy MongoExpress (Deployment and Service)

We can create our own config file, no need for a Chart.

`kubectl apply -f mongo-express-helm-project.yaml` - create mongo-express deployment

4. Deploy NGINX Ingress Controller as Loadbalancer (using Helm Chart)

`helm repo add nginx-stable https://helm.nginx.com/stable` - add repo\
`helm install my-release nginx-stable/nginx-ingress` - install the chart\
Ingress controller will be added to our cluster and also the LoadBalancer will be created in the Linode Cloud.\
LoadBalancer forward to Ingress controller which will than forward based on the ingress rules configured.

Ingress controller service will have external IP of the Linode LoadBalancer.

5. Configure Ingress rules

`kubectl apply -f mongo-express-linode-ingress.yaml` - apply ingress rules

`kubectl scale --replicas=0 statefulset/mongodbmyname` - delete all the mongodb pods => volumes in Linode will be unattached

`kubectl scale --replicas=3 statefulset/mongodbmyname` - observe the data persistance 

---

## Project 4

**Deploy web app in a k8s cluster from a private Docker registry**

When pulling from private registry you need to offer k8s explicit access.

1. SSH into minikube VM and login to the DockerHub private repo from there

`ssh minikube`\ 
`docker login --username usernamedockerhub --password passworddockerhub` - login to DockerHub repo -> .docker/config.json is created

2. Create Secret component in k8s

`docker-secret-private-repo.yaml` - Secret k8s component - key .dockerconfigjson will contain base64 encoded value of the .docker/config.json file\
To use kubectl outside of Minikube, you need first to copy the .docker/json from minikube into local machine using `scp -i $(minikube ssh-key) docker@$(minikube ip):.docker/config.json .docker/config.json`.\

`cat .docker/config.json | base64` - encode the .docker/config.json, copy the value and put into secret yaml file\
`kubectl create secret generic my-registry-key --from-file=.dockerconfigjson=.docker/config.json --type=kubernetes.io/dockerconfigjson` - creates the secret

3. Create the deployment for the app

`kubectl apply -f docker-demo-app-deployment.yaml` 

---

## Project 5

**Setup Prometheus monitoring in K8s cluster**

Stateful applications need constant management and syncing after deployment. So stateful applications, like database need to be operated. Instead of a human operator, you have an automated scripted operator. Operators are createdby official maintainers.

How it works:
- control loop mechanism
- make use of CRDs (Custom Resource Definitions - custom k8s component which extends the k8s api)

1. Install Prometheus operator using Helm 

`helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`\
`helm repo update`\
`helm install [RELEASE_NAME] prometheus-community/kube-prometheus-stack`

To access Grafana: `kubectl port-forward deployment/prometheus-grafana 3000` => can be accessed then on localhost:3000

---

## Project 6





