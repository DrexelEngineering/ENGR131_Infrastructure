# Uploading the Helm Chart to the Helm Repository

```bash
NAME="programming-course-database"
```

```bash
helm package database/k8/programming_course_database --destination .deploy
```

```bash
cr upload -o DrexelEngineering -r ENGR131_Infrastructure -p .deploy -t $CR_TOKEN
```

## Installing the Helm Chart

```bash
helm install my-release https://github.com/DrexelEngineering/ENGR131_Infrastructure/releases/download/Programming-Course-Database-0.1.0/Programming-Course-Database-0.1.0.tgz -n
 m3learning
```
