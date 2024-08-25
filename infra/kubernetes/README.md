1. Create our namespace
> kubectl create namespace darkness

2. Install the MongoDB Helm Operator
See: https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/install-upgrade.md#install-the-operator-using-helm
> helm install community-operator mongodb/community-operator --namespace darkness [--create-namespace]

3. Update definition

4. Deploy a Replica Set
See: https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/deploy-configure.md
> kubectl apply -f config/samples/mongodb.com_v1_mongodbcommunity_cr.yaml --namespace <my-namespace>
> kubectl apply -f ./mongodb.yaml --namespace darkness

5. Verify resources:
> kubectl get mongodbcommunity --namespace <my-namespace>

6. Get connection credentials:
> kubectl get secret <connection-string-secret-name> -n <my-namespace> \
-o json | jq -r '.data | with_entries(.value |= @base64d)'

> kubectl get secret my-connection-string -n darkness -o json | jq -r '.data | with_entries(.value |= @base64d)'

7. Use connection string in apps:
containers:
 - name: test-app
   env:
    - name: "CONNECTION_STRING"
      valueFrom:
        secretKeyRef:
          name: <metadata.name>-<auth-db>-<username>
          key: connectionString.standardSrv



kubectl expose service darkness-mongodb-svc --type=NodePort --port=27017 --namespace darkness
