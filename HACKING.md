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

```shell
argocd login user-ukazmierczak-argo-cd.user.lab.sspcloud.fr --username admin --password <Password>
```

To upload a config map:
```shell
 kubectl apply -f argocd-cmd-params-cm.yaml
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

argocd login user-ukazmierczak-argo-cd.user.lab.sspcloud.fr --username admin --password <Password>
```