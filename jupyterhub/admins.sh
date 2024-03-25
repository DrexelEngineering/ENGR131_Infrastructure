# Assuming ADMIN_USERS is your comma-separated environment variable
IFS=',' read -ra ADDR <<< "$ADMIN_USERS"
ADMIN_LIST=""
len=${#ADDR[@]}
last_index=$((len - 1))

for i in "${!ADDR[@]}"; do
    # Append each user with three tabs for indentation, followed by the email in quotes
    if [[ "$i" -ne "$last_index" ]]; then
        # For all but the last entry, append with a newline
        ADMIN_LIST+="        - \""${ADDR[$i]}""$'\n'
    else
        # For the last entry, append without adding a newline
        ADMIN_LIST+="        - \""${ADDR[$i]}""$''
    fi
done

# To display the result and verify the tabs are correctly interpreted
export ADMIN_LIST

# # Assuming you're using envsubst to substitute $ADMIN_LIST into a template
# envsubst '${ADMIN_LIST}' < ./path/to/values.template.yaml > values.generated.yaml
