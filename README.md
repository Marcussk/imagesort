# imagesort

# Installation

- Install minikube https://minikube.sigs.k8s.io/docs/start/
- Install rabbitmq cluster https://medium.com/nerd-for-tech/deploying-rabbitmq-on-kubernetes-using-rabbitmq-cluster-operator-ef99f7a4e417 
    - minikube kubectl -- apply -f https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml
    - minikube kubectl -- get all -o wide -n rabbitmq-system
    - minikube kubectl -- apply -f reqs/rabbitmq_cluster.yaml
    - minikube kubectl -- describe RabbitmqCluster production-rabbitmqcluster
    - minikube kubectl -- get all -l app.kubernetes.io/part-of=rabbitmq
- Create minikube loadbalancer tunnel https://minikube.sigs.k8s.io/docs/handbook/accessing/
    - minikube tunnel