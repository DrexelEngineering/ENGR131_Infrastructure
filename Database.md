# Building the Postgres Database to Store Grades

## Creating a persistant volume claim

To store the data you need to apply a persistant volume claim. This is done by creating a file called `postgres-pv-claim.yaml` with the following content:

export NAMESPACE="engr131spring"

export NAMESPACE="m3learning"


```bash
echo "Creating the volume..." &&

kubectl apply -f database/k8/persistent-volume-claim.yml -n $NAMESPACE
```

export DB_PVC_SIZE="25Gi"

## Adding Secrets

You want to add some secrets which can be used by the database

```bash
echo "Creating the secrets..." &&
kubectl apply -f database/k8/secret.yml -n $NAMESPACE
```

## Creating the Database

You can apply the database by running the following command:

```bash
echo "Creating the postgres deployment and service..." &&
kubectl apply -f database/k8/postgres-deployment.yml -n $NAMESPACE &&
kubectl apply -f database/k8/postgres-service.yml -n $NAMESPACE &&
POD_NAME=$(kubectl get pod -l service=postgres -o jsonpath="{.items[0].metadata.name}") -n $NAMESPACE
```

#### To check the status of the database

```bash
kubectl get pods
kubectl exec $POD_NAME --stdin --tty -- psql -U sample -d grades -n #NAMESPACE
```

## Creating the Database Schema

You can apply the database schema by running the SQL from the files to apply the tables

TODO: Add the SQL to apply the tables


## Start the Flask Servers

We will start 3 Flask servers. One for students, and one for the admins. 

```bash
kubectl apply -f database/k8/student-flask-deployment.yml -n $NAMESPACE &&
kubectl apply -f database/k8/student-flask-service.yml -n $NAMESPACE &&
kubectl apply -f database/k8/admin-flask-deployment.yml -n $NAMESPACE &&
kubectl apply -f database/k8/admin-flask-service.yml -n $NAMESPACE &&
kubectl apply -f database/k8/admin-server-ingress.yml -n $NAMESPACE &&
kubectl apply -f database/k8/student-server-ingress.yml -n $NAMESPACE
```

## Adding Student Information to the Database

You can add student information to the database by running the following command:

```bash
# creates the cookie
curl -s -o /dev/null -c cookie.txt -X POST -d "username=admin&password=diffuser"  https://engr131-admin-grader.nrp-nautilus.io/login &&
# uploads the student names
curl -b cookie.txt -X POST -F "file=@./.test_files/student-names.csv" -F "password=diffuser" https://engr131-admin-grader.nrp-nautilus.io/upload_students
```

## Test adding an Assignment

You can add an assignment to the database by running the following command:

```bash
curl -b cookie.txt -X POST -F "file=@/home/ferroelectric/K8_autograder_database/.test_files/results.json" -F "password=diffuser" -F "assignment_id=Homework_999" -F "assignment_name=Test Homework Assignment" https://engr131-admin-grader.nrp-nautilus.io/upload_assignment
```

## Add student lab sections to the database

``` bash
curl -b cookie.txt -X POST -F "file=@/home/ferroelectric/K8_autograder_database/.test_files/test/ENGR131-070.csv" -F "password=diffuser" -F "lab_section=070" -F "day_of_week=f" -F "start_time=15:00:00" https://engr131-admin-grader.nrp-nautilus.io/upload_lab_section
```

