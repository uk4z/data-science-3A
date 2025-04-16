# Setup

Pre-requisite: having `python3` install. 

First, create a python environment: 
```shell
python3 -m venv .env
```

Then, activate your environment: 
```shell
source .env/bin/activate
```

Download all the required packages: 
```shell
pip install -r requirements.txt
```

Alternatively, you can run:
```shell
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
```

Deprectaed
```shell
argocd login user-ukazmierczak-argo-cd.user.lab.sspcloud.fr --username admin --password <Password>
```

```shell
minikube start
export KUBECONFIG=`ls ~/.kube/config`

# install ArgoCD in k8s
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Look if pods are running
kubectl get pods -n argocd
kubectl port-forward svc/argocd-server 8080:443 -n argocd

export PASSWORD=`argocd admin initial-password -n argocd`  
argocd login localhost:8080 --username admin --password PASSWORD -y
kubectl apply -f application.yaml
```
Now you can go http://localhost:8080 and see the argocd instance with the app running.