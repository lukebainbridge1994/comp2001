## Docker Deployment

The ProfileService is containerised and published on Docker Hub.

### Pull the image
docker pull lukeb1994/profile-service:latest

### Run the container
docker run -p 5000:5000 lukeb1994/profile-service:latest

### Service URLs
- Swagger UI: http://127.0.0.1:5000/apidocs/
- Health check: http://127.0.0.1:5000/