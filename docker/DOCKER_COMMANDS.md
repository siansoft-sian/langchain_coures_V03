# Common Docker Commands

A quick reference for the [Docker](https://docs.docker.com/) commands you'll use most often. The scripts in this folder run these for you; use this sheet when you want to do something by hand.

## Check Docker

| Command | What it does |
| --- | --- |
| `docker --version` | Show the installed Docker version |
| `docker info` | Show details; fails if Docker Desktop isn't running |

## Images

| Command | What it does |
| --- | --- |
| `docker build -f docker/Dockerfile -t my-app .` | Build an image named `my-app` from the project folder |
| `docker build --no-cache -f docker/Dockerfile -t my-app .` | Rebuild every step from scratch |
| `docker images` | List images on your computer |
| `docker rmi my-app` | Delete an image |
| `docker image prune` | Delete unused (dangling) images |

## Containers

| Command | What it does |
| --- | --- |
| `docker run --rm my-app` | Run the image; remove the container when it stops |
| `docker run --rm -it my-app bash` | Open a shell inside a new container |
| `docker run --rm --env-file .env my-app` | Run with the keys from `.env` |
| `docker run --rm -p 8000:8000 my-app` | Open port 8000 (computer:container) |
| `docker run -d --name app my-app` | Run in the background with the name `app` |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers, including stopped ones |
| `docker logs -f app` | Follow the output of container `app` |
| `docker exec -it app bash` | Open a shell inside the running container `app` |
| `docker stop app` | Stop container `app` |
| `docker rm app` | Delete the stopped container `app` |

## Clean up

| Command | What it does |
| --- | --- |
| `docker system df` | Show how much disk space Docker uses |
| `docker container prune` | Delete all stopped containers |
| `docker system prune` | Delete stopped containers, unused networks and dangling images |
| `docker builder prune` | Delete the build cache |

## Tips

- The `.` at the end of `docker build` is the folder Docker copies files from (the project root).
- `--rm` keeps things tidy: the container is deleted when it stops.
- `-it` lets you type into the container. Leave it out when running from another script.
