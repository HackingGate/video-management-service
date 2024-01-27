# Video Management Service

## Description

This Video Management Service is a web-based application developed in Flask. It allows users to upload videos, which are then converted to HLS (HTTP Live Streaming) format for efficient streaming.

## Running the application in Docker

### Prerequisites

- Docker

### Configuration

```bash
export UPLOAD_FOLDER=/path/to/your/upload/folder
```

Build the Docker image

```bash
make build
```

Run the Docker container

```bash
make up
```

## Development on local environment

### Prerequisites

- Python 3.12
- Poetry
- FFmpeg

Install dependencies

```bash
poerty install
```

Run the application

```bash
poetry run python app.py
```
