FROM python:3.12

# Set working directory
WORKDIR /usr/src/

# Install system dependencies
RUN apt update && apt upgrade -y

# Add server files
COPY . .

RUN chmod +x ./docker-entrypoint.sh

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask to run in development mode
ENV FLASK_ENV=development

ENTRYPOINT ["./docker-entrypoint.sh"]