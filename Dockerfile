# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies in a single layer to reduce build time and image size
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry

# Copy only the files needed for installing dependencies first to leverage Docker's cache
COPY poetry.lock pyproject.toml ./

# Install dependencies but without creating virtual environments inside the Docker container
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

# Copy the rest of your application's code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define a volume for persistent storage
VOLUME /mnt/media-volume

# Run the app
CMD ["python", "app.py"]
