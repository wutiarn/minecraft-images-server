set -e
docker build -t quay.io/wutiarn/mci .
docker push quay.io/wutiarn/mci
