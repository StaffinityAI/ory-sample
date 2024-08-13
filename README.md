
# Ory Sample

This project provides a containerized setup for `Ory Kratos with Hydra`. It leverages Docker Compose to orchestrate multiple services, including ORY Kratos for identity and user management, ORY Hydra for OAuth2 and OpenID Connect, and a sample FastAPI application, to show how to interface with kratos and hydra. The project is designed to be easily deployable and scalable for production environments.


## Table of Contents
- Overview
- Prerequisites
- Installation
- Usage
- Configuration
- Contributing
- License

### Prerequisites

Before you start, ensure you have the following installed on your machine:

- Docker: `Install Docker` #https://docs.docker.com/engine/install
- Docker Compose: `Install Docker Compose`

### Installation
To set up the project locally, follow these steps:
1. Clone the Repository: 
```
git clone https://github.com/StaffinityAI/ory-sample.git

cd ory-sample
```
2. Start the Service:
Use Docker Compose to build and start all services:
```
docker compose up --build

```
This command will:
- Pull necessary Docker images.
- Build the FastAPI service from the Dockerfile.
- Start all containers, including Postgres databases for Kratos and Hydra, and the Kratos, Hydra, and FastAPI services.

3. Verify the Setup:
After running the docker-compose up command, you should see the services starting in your terminal. You can verify that everything is running correctly by visiting the respective service URLs:
- *Kratos Admin*: http://localhost:4434
- *Kratos Public*: http://localhost:4433

- *Hydra Admin*: http://localhost:4445
- *Hydra Public*: http://localhost:4444
- *FastAPI*: http://localhost:8000


### Usage
#### Kratos
- Kratos is used for identity management. It interacts with the Postgres-Kratos database to handle user data.
- You can access the Kratos Admin API at http://localhost:4434 and the Public API at http://localhost:4433.

#### Hydra
- Hydra manages OAuth2 and OpenID Connect flows.
- The Hydra Admin API is accessible at http://localhost:4445, and the Public API at http://localhost:4444.


#### FastAPI
- The FastAPI application serves as the backend for your service(for creating APIs).
- It is accessible at http://localhost:8000.


### Configuration
#### Environment Variables
- ##### Kratos:
    - DSN: Database connection string for Kratos, defined as `postgresql://kratos_user:kratos_password@postgres-kratos/kratos_db?sslmode=disable`.
- #### Hydra:
    - DSN: Database connection string for Hydra, defined as `postgresql://hydra_user:hydra_password@postgres-hydra/hydra_db?sslmode=disable`.


#### Volumes

- Persistent data storage is managed through Docker volumes:
    - `postgres-kratos-data`: Stores data for the Kratos Postgres database.
    - `postgres-hydra-data`: Stores data for the Hydra Postgres database.



#### Networks

- The services are organized into multiple Docker networks:
    - `ory-main-net`: Connects all services together.
    - `kratos-net`: Isolates Kratos-related services.
    - `hydra-net`: Isolates Hydra-related services.

    
![Diagram](./ory_network.png)



### Contributing
We welcome contributions from the community! If you have any ideas, suggestions, or issues, please feel free to open an issue or submit a pull request.
#### How to Contribute
1. Fork the Repository
Click on the `Fork` button at the top right of this page to create your own copy of the repository.

2. Clone Your Fork
```
git clone https://github.com/StaffinityAI/ory-sample.git

cd ory-sample

```
3. Create a New Branch
```
git checkout -b feature/your-feature-name

```
4. Make Your Changes

Implement your changes and commit them to your branch.

5. Submit a Pull Request
Once your changes are ready, push your branch to your forked repository and submit a pull request.
