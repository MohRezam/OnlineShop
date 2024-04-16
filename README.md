# OnlineShop

**Online Digital Product Store**

## Introduction

This online store serves as a platform for buying and selling various Digital Products. The store offers various features that allow users to easily find and order their desired products.

Getting Started

Follow these steps to set up the project locally:
1. Clone the Repository

bash

git clone git@github.com:MohRezam/OnlineShop.git
cd OnlineShop

2. Create a Virtual Environment

Create a virtual environment to isolate project dependencies:

bash

python3 -m venv venv

Activate the virtual environment:

bash

# On macOS and Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate

3. Install Dependencies

Install project dependencies from requirements.txt:

bash

pip install -r requirements.txt

4. Set Up Environment Variables

Create a .env file in the project root directory and add the following environment variables:

env

SECRET_KEY='your-secret-key'
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

REDISHOST=redis
REDISPORT=6379
REDISDB=0
REDISPASS=your-redis-password

POSTGRES_NAME=postgres_django
POSTGRES_USER=postgres_django
POSTGRES_PASSWORD=your-postgres-password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

APP_HOST=localhost

Replace your-secret-key, your-redis-password, and your-postgres-password with your actual values.
5. Docker Setup

Run the following commands to build and run the Docker containers:

bash

docker-compose up --build

6. Access the Application

Once Docker containers are up and running, you can access the application at:

arduino

http://localhost:80/

Notes

    Make sure Docker is running before executing Docker commands.
    Update .env file with your actual values for SECRET_KEY, REDISPASS, and POSTGRES_PASSWORD.
    If you encounter any issues, refer to Docker logs or run docker-compose logs to troubleshoot.


## Features

- **Display Categories and Products**: Users can view different types of laptops, computers ... based on various categories and easily find their desired products.

- **Add to Cart**: By using the "Add to Cart" feature, users can add products to their shopping cart and then start the purchasing process.

- **User Account Management**: Users can manage their user accounts, edit their personal information, and view their order history.

- **Discount Coupons**: Users have the option to use discount coupons to gain special discounts on purchases.

- **Leave Comments and Reviews**: Users can leave comments and reviews about products and share their experiences with other users.

## User Guide

### Browse Products

To view the products available in the store, use the relevant menu and find your desired products.

### Add to Cart

To purchase products, add the desired product to your shopping cart and then start the purchasing process.
