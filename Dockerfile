FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libsndfile1-dev \
    libllvm14 \
    llvm-14 \
    && rm -rf /var/lib/apt/lists/*

# Set LLVM environment
ENV LLVM_CONFIG=/usr/lib/llvm-14/bin/llvm-config
ENV PATH="/usr/lib/llvm-14/bin:$PATH"

# Install Python dependencies
COPY requirements/prod.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install torch torchaudio
RUN pip install -r prod.txt

# Copy application
COPY . .

# Build
RUN pip install pyinstaller
RUN pyinstaller --name="VoiceForge" --onefile src/main.py

# Output
CMD ["cp", "-r", "dist", "/output"]