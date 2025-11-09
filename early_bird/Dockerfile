ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-flask \
    && pip3 install --upgrade pip

# Copy files
COPY . /app
WORKDIR /app

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python3", "run.py"]
