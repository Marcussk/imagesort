- Install minikube https://minikube.sigs.k8s.io/docs/start/
- Install rabbitmq cluster https://medium.com/nerd-for-tech/deploying-rabbitmq-on-kubernetes-using-rabbitmq-cluster-operator-ef99f7a4e417 
    - minikube kubectl -- apply -f https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml
    - minikube kubectl -- get all -o wide -n rabbitmq-system
    - minikube kubectl -- apply -f reqs/rabbitmq_cluster.yaml
    - minikube kubectl -- describe RabbitmqCluster production-rabbitmqcluster
    - minikube kubectl -- get all -l app.kubernetes.io/part-of=rabbitmq
- Create minikube loadbalancer tunnel https://minikube.sigs.k8s.io/docs/handbook/accessing/
    - minikube tunnel

Connection not working: https://stackoverflow.com/questions/40563469/connecting-to-rabbitmq-docker-container-from-service-in-another-container

Running local image in kube deployment: https://medium.com/swlh/how-to-run-locally-built-docker-images-in-kubernetes-b28fbc32cc1d


minikube image load imagesort-dumper

Uploading file to container: docker cp red.png 18f3612b15ab:/usr/src/app/images/red.png

Adding default rabbit users https://stackoverflow.com/questions/30747469/how-to-add-initial-users-when-starting-a-rabbitmq-docker-container

examples https://fenga.medium.com/an-asynchronous-rabbitmq-client-in-python-274a310858a1