# Use an official Python runtime as a parent image
FROM python:3.11.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/
RUN python manage.py collectstatic --noinput

# Expose port 8000 to the outside world
EXPOSE 8000

# Define the command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "eCommercePlatform.wsgi:application"]
