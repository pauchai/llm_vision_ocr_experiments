FROM nvidia/cuda:12.1-devel-ubuntu22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /huggingface_ocr

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 7861

# Start the application
CMD ["python3", "main.py"]
