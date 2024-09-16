#!/bin/bash
# replace_env.sh

while IFS='=' read -r key value; do
	# Trim leading and trailing spaces
	key=$(echo "$key" | xargs)
	value=$(echo "$value" | xargs)

	# Skip empty lines and lines starting with '#'
	if [[ -z $key || $key == \#* ]]; then
		continue
	fi

	# Check if the key is a valid identifier
	if [[ $key =~ ^[a-zA-Z_]+[a-zA-Z0-9_]*$ ]]; then
		export "$key=$value"
	else
		echo "Skipping invalid identifier: $key"
	fi
done <./.env

# Replace environment variables and create a new file
envsubst <create.sql >create_db.sql
