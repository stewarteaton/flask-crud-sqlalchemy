<!-- Setting up flask for development -->
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run


<!-- Docker build command:  -->
docker image build -t recycling-partnership .
<!-- Docker run command: -->
docker run -p 8881:8881 -d recycling-partnership

