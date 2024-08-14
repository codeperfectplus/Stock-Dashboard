# Use the official Python image with a specific version
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and source code
COPY requirements.txt ./
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Dash will run on
EXPOSE 5000

# Install supervisor
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Create supervisor configuration file
RUN echo "[supervisord]\n" \
    "nodaemon=true\n\n" \
    "[program:app]\n" \
    "command=python3 dash_server.py\n" \
    "autostart=true\n" \
    "autorestart=true\n" \
    "stdout_logfile=/var/log/app.log\n" \
    "stderr_logfile=/var/log/app.err\n\n" \
    "[program:main]\n" \
    "command=python3 stock_scrapper.py\n" \
    "autostart=true\n" \
    "autorestart=true\n" \
    "stdout_logfile=/var/log/main.log\n" \
    "stderr_logfile=/var/log/main.err\n" \
    > /etc/supervisor/conf.d/supervisord.conf

# Run supervisor to start both scripts
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
