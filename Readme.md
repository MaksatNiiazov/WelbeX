# Restaurant Review Platform

## Overview

The Truck Service  is a web application built with Django and Django REST Framework. The application provides RESTful APIs and is containerized with Docker for easy setup and deployment.

## Features

- View list of restaurants and detailed information about each.
- User authentication system for secure access and user management.
- Users can post reviews and rate restaurants.
- Integration with external map APIs to display restaurant locations.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- Docker and Docker Compose (for container management)

### Local Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/MaksatNiiazov/WelbeX.git
   ```
Install the dependencies:

   ```sh
pip install -r requirements.txt
```
Run database migrations:

   ```sh
python manage.py migrate
```
### Start the development server:

   ```sh
python manage.py runserver
```
The application will be available at http://localhost:8000.

### Using Docker
Build the Docker image:

   ```sh

docker-compose build
```
###Start the Docker containers:

   ```sh
docker-compose up
```