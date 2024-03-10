#!/bin/bash

export envtag="1.0.0"
export course="engr131"
export semester="spring2024"
export dockeruser="jagar2"
export nrpgitlabuser="jagar2"
export envcontainer="$coursejlab"
export OAUTH_CLIENT_SECRET="VsH4/qz0Vm+4pENMFP3j6EeyHgi4s1RPQNR7Mrp4Pxg="
export OAUTH_CALLBACK_URL="https://engr131spring2024.nrp-nautilus.io/hub/oauth_callback"
export OAUTH_CLIENT_ID="e34feab7-6074-4b9d-8122-b75ae6757e4d"
export DB_PVC_SIZE="25Gi"
export POSTGRES_PORT=5432
export POSTGRES_NAME="postgres-$course-spring2024"
export POSTGRES_CONTAINER="$dockeruser/grade_database:latest"
export POSTGRES_MEM_MIN="8Gi"
export POSTGRES_MEM_MAX="12Gi"
export POSTGRES_CPU_MIN=4
export POSTGRES_CPU_MAX=1
export POSTGRES_PVC="postgres-pvc-$course-$semester"
