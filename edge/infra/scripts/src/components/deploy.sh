set -e
set -x

cd "$(dirname "$0")"

aws greengrassv2 create-deployment --cli-input-json file://deployment.json

echo "Please wait a few minutes for the deployment to complete."