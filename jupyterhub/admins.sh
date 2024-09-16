#!/usr/bin/env bash

# Assuming ADMIN_USERS is your comma-separated environment variable
IFS=',' read -ra ADDR <<<"$ADMIN_USERS"
ADMIN_LIST=""

for i in "${!ADDR[@]}"; do
	# Append each user with three (?) tabs for indentation, followed by the email in quotes
	# Also append newline after each entry
	ADMIN_LIST+="        - \"${ADDR[$i]}\"\n"
done

# Remove trailing newline
ADMIN_LIST=${ADMIN_LIST%$'\n'}

# To display the result and verify the tabs are correctly interpreted
export ADMIN_LIST

# Assuming you're using envsubst to substitute $ADMIN_LIST into a template
# envsubst '${ADMIN_LIST}' < ./path/to/values.template.yaml > values.generated.yaml
