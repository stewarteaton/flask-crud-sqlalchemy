# initialize base image (Alpine is lightweight linux distro)
FROM python:3-alpine

# define directory
WORKDIR /recycling-partnership

# copy contents into working directory
COPY requirements.txt /recycling-partnership/requirements.txt

# install python dependencies
# RUN pip3 install --upgrade setuptools
RUN pip3 install -r /recycling-partnership/requirements.txt

ADD . /recycling-partnership

EXPOSE 8881

# define command to start container
CMD ["python","app.py"]
