clear

TOKEN=$(cat secret.py | sed -e 's/API_TOKEN.*=.*"\(.*\)"/\1/')
ACCOUNT_ID=""
BASE="https://api.cloudflare.com/client/v4"
DATA=''
JSON=''
FILE=''

api() {
  [ -z "$1" ] && echo "Invalid Endpoint" >&2 && exit 1
  ENDPOINT=$1
  if [ -n "$FILE" ]; then
    METADATA_CONTENT=$(cat ${METADATA_FILE})
    METADATA="metadata=${METADATA_CONTENT};type=application/json"
    SCRIPT="script=@${FILE};type=application/javascript"
    curl -s -X $METHOD "${BASE}${ENDPOINT}" -H "Authorization: Bearer ${TOKEN}" -F "${METADATA}" -F "${SCRIPT}" | jq '.'
  else
    PARAMS=''
    if [ -n "$JSON" ]; then
      PARAMS="${PARAMS} -H \"Content-Type: applicadtion/json\""
    fi
    if [ -n "$DATA" ]; then
      PARAMS="${PARAMS} --data '${DATA}'"
    fi
    curl -s -X $METHOD "${BASE}${ENDPOINT}" -H "Authorization: Bearer ${TOKEN}" "$PARAMS" | jq '.'
  fi
}

# METHOD='GET'
# METHOD='POST'
METHOD='PUT'
# METHOD='PATCH'

JSON=''
DATA=''
FILE='tests/test.js'
METADATA_FILE='tests/metadata.json'
api "/accounts/${ACCOUNT_ID}/workers/scripts/tester"