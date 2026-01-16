# ProfileService Microservice

This repository contains the ProfileService microservice developed for the AllTrails project.
The service is responsible for managing user profile data within the Trail / AllTrails application.

## Features
- View own user profile
- Update own user profile
- Delete own user profile
- Admin endpoints to manage any user profile
- Role-based access control
- Swagger (OpenAPI) documentation
- Dockerised deployment

## Technology Stack
- Python 3.11
- Flask
- Microsoft SQL Server (via pyodbc)
- Swagger (Flasgger)
- Docker

## Running with Docker

The service is available as a Docker image on Docker Hub:

docker pull lukeb1994/profile-service:latest

docker run --env-file .env -p 5000:5000 lukeb1994/profile-service:latest
