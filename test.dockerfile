# Stage 1: Build stage
FROM python:3.11-slim-bookworm AS builder

# Avoid bytecode baggage
ENV PYTHONDONTWRITEBYTECODE=1

# Create a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Update pip
RUN python3 -m pip install --upgrade pip --no-cache-dir

# Copy and install Python dependencies
COPY requirements.txt .

RUN python3 -m pip install -v \
    --prefer-binary \
    -r requirements.txt \
    --extra-index-url https://www.piwheels.org/simple \
    --no-cache-dir

# Stage 2: Final stage
FROM python:3.11-slim-bookworm

# Avoid bytecode baggage
ENV PYTHONDONTWRITEBYTECODE=1

# Install only the necessary runtime dependencies
RUN apt-get update -y && \
    apt-get install -y \
    --no-install-recommends \
    libopenblas-dev libopenjp2-7 libtiff6 libxcb1 libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only the necessary application code
WORKDIR /code
COPY . .

# Set the default command
CMD ["python", "run.py"]