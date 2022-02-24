# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /recycling-partnership
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8881
COPY . .
CMD ["python", "app.py"]