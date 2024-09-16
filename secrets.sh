#!/bin/bash

# tag for the Juhub environment
export envtag="2.0.0"

# Course name
export course="engr131"

# Semester
export semester="spring2024"

# Usernames
export dockeruser="jagar2"
export nrpgitlabuser="jagar2"

# JupyterHub
export envcontainer="${course}jlab"
export HOSTNAME="nrp-nautilus.io"
export OAUTH_CLIENT_SECRET="VsH4/qz0Vm+4pENMFP3j6EeyHgi4s1RPQNR7Mrp4Pxg="
export OAUTH_CALLBACK_URL="https://${course}-${semester}.${HOSTNAME}/hub/oauth_callback"
export OAUTH_CLIENT_ID="e34feab7-6074-4b9d-8122-b75ae6757e4d"
export ADMIN_USERS="jca92@drexel.edu,jca318@lehigh.edu,jca318@globusid.org,jca318"

export STORAGE_CLASS="rook-cephfs-east"

export CLIENT_ID="cilogon:/client_id/37fc855bffdeb424d5eac406c9de554a"
export CLIENT_SECRET="Hoii2pOlVra6D7Ggy-gGu8mo7rlLA-6lwQ8QMjxojmagVTtkmF5ns3dBk0had7qOobJVCmE4AXijHcqwYWrF6w"
export OAUTH_CALLBACK_URL="https://engr131.nrp-nautilus.io/hub/oauth_callback"

# export DB_PVC_SIZE="25Gi"
# export POSTGRES_PORT=5432
# export POSTGRES_NAME="postgres-$course-spring2024"
# export POSTGRES_CONTAINER="$dockeruser/grade_database:latest"
# export POSTGRES_MEM_MIN="8Gi"
# export POSTGRES_MEM_MAX="12Gi"
# export POSTGRES_CPU_MIN=1
# export POSTGRES_CPU_MAX=4
# export POSTGRES_PVC="postgres-pvc-$course-$semester"
# export STORAGE_CLASS="rook-ceph-block"
# export POSTGRES_PVC_SIZE="25Gi"

# export ADMIN_SERVER_NAME="admin-$course-$semester-flask"
# export ADMIN_SERVER_REPLICAS=1
# export ADMIN_SERVER_CONTAINER="$dockeruser/admin_flask_server:2.0.5"
# export ADMIN_MEM_MIN="6Gi"
# export ADMIN_MEM_MAX="12Gi"
# export ADMIN_CPU_MIN=2
# export ADMIN_CPU_MAX=4
# export ADMIN_FLASK_SERVICE_NAME="$ADMIN_SERVER_NAME-service"
# export ADMIN_FLASK_SERVICE_PORT=5100
# export ADMIN_FLASK_HOSTNAME="${course}-${semester}-admin-grader.${HOSTNAME}"

# export STUDENT_SERVER_NAME="student-$course-$semester-flask"
# export STUDENT_SERVER_REPLICAS=1
# export STUDENT_SERVER_CONTAINER="$dockeruser/student_flask_server:4.0.0"
# export STUDENT_MEM_MIN="8Gi"
# export STUDENT_MEM_MAX="16Gi"
# export STUDENT_CPU_MIN=8
# export STUDENT_CPU_MAX=16
# export STUDENT_FLASK_SERVICE_NAME="$STUDENT_SERVER_NAME-service"
# export STUDENT_FLASK_SERVICE_PORT=5200
# export STUDENT_FLASK_HOSTNAME="${course}-${semester}-STUDENT-grader.${HOSTNAME}"

# export PGWEB_PASSWORD="--auth-pass=CappsAgar"
# export PGWEB_USER="--auth-user=engr131"
# export PGWEB_PORT=8081
# export PGWEB_MEM_MIN="6Gi"
# export PGWEB_MEM_MAX="12Gi"
# export PGWEB_CPU_MIN=2
# export PGWEB_CPU_MAX=4
