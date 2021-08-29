clear

TOKEN=$(cat secret.py | sed -e 's/API_TOKEN\s*=\s*"\(.*\)"/\1/')
BASE="https://api.cloudflare.com/client/v4"
DATA=''
JSON=''

api() {
  PARAMS=''
  [ -z "$1" ] && echo "Invalid Endpoint" >&2 && exit 1
  ENDPOINT=$1
  if [ -n "$JSON" ]; then
    PARAMS="${PARAMS} -H \"Content-Type: applicadtion/json\""
  fi
  if [ -n "$DATA" ]; then
    PARAMS="${PARAMS} --data '${DATA}'"
  fi
  curl -s -X $METHOD "${BASE}${ENDPOINT}" -H "Authorization: Bearer ${TOKEN}" "$PARAMS" | jq '.'
}

METHOD='GET'
# METHOD='POST'
# METHOD='PUT'
# METHOD='PATCH'

JSON='yes'
DATA=''
api '/user'
