# Use slim version of Python for smaller image size.
FROM python:3.12-slim

# Set working directory inside container.
WORKDIR /app

# Copy project dependencies.
COPY pyproject.toml poetry.lock /app/

# Install Poetry for managing packages and dependencies. Setting the venv to False is important to not mess up the
# application startup.
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy everything from prject to the working directory.
COPY . /app

# This ensures stdout and stderr to be unbuffered, and sent to your containers logs or terminal.
ENV PYTHONUNBUFFERED 1

# Start the server, run the application, specify the host and port numbers.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100"]