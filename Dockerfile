# Use an official Python runtime
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Set environment variables
ENV PORT=5000

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]