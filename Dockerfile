# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Poetry
RUN pip install poetry

# Copy the poetry.lock and pyproject.toml files
COPY poetry.lock pyproject.toml ./

# Install dependencies but without creating virtual environments inside the Docker container
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of your application's code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

# Define a volume for persistent storage
VOLUME /mnt/media-volume
