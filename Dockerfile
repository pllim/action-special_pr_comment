# Container image that runs your code
FROM quay.io/spacetelescope/astropy-actions-docker:0.1

# Copies code file action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

COPY special_day.py /special_day.py

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
