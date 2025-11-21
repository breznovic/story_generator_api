# Story Generator Project

This project consists of two parts:

- **Frontend** - the user interface, available at: https://github.com/breznovic/story-generator  
- **Backend** - the API for data handling, available at: https://github.com/breznovic/story_generator_api  

The project is containerized using Docker and Docker Compose.

## Prerequisites

Before starting, ensure you have the following installed:
- Docker
- Docker Compose

## Setup and Running the Project

### Clone the Repositories

Open your terminal and run the following commands to clone both repositories:

git clone https://github.com/breznovic/story-generator.git   frontend
git clone https://github.com/breznovic/story_generator_api.git   backend

#### Navigate to the Project Directory
Create and move into the project directory:

mkdir story-generator-project
cd story-generator-project

#### Then place both cloned repositories in this directory so the structure looks like:

```
story-generator-project/
├── frontend/
└── backend/
```
#### Create docker-compose.yml
Create a docker-compose.yml file in the project root with the following content:

```
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: always
```

#### Build and Run the Containers
In the root directory of the project (where the docker-compose.yml file is located), run:

```
docker-compose up --build
This command will:
```

#### Build the Docker images for the frontend and backend

Start the containers

Access the Application
After a successful launch:

Frontend will be available at: http://localhost:3000

Backend will be available at: http://localhost:8000
