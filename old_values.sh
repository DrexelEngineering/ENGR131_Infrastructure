#! /usr/bin/env bash

course="foo"
semester="bar"
dockeruser="baz"

export STUDENT_SERVER_NAME="student-$course-$semester-flask"
export STUDENT_SERVER_REPLICAS=2
export STUDENT_SERVER_CONTAINER="$dockeruser/student_flask_server:2.0.5"
export STUDENT_MEM_MIN="6Gi"
export STUDENT_MEM_MAX="12Gi"
export STUDENT_CPU_MIN=2
export STUDENT_CPU_MAX=4
export STUDENT_FLASK_SERVICE_NAME="$STUDENT_SERVER_NAME-service"
export STUDENT_FLASK_SERVICE_PORT=5100
export STUDENT_FLASK_HOSTNAME="${course}-${semester}-STUDENT-grader.${HOSTNAME}"
