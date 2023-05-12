# Scraper Flask API

This is an ongoing project that is currently in development.

## Description

The Scraper Flask API is designed to scrape data from various websites and help users monitor and track that data. Currently, the API can only scrape Amazon products. Data is stored in memory since a database has not yet been implemented.

The primary goal of this project is to create a reliable and efficient tool for users to track and analyze data from different websites.

## Installation

To use this API, you can run it in a Docker container using the following steps:

1. Clone the repository to your local machine.
2. Install Docker on your machine, if it's not already installed.
3. In your terminal, navigate to the root directory of the project.
4. Run the following command to start the Docker containers:

docker-compose -f docker-compose-run.yml up

5. Wait for the containers to start up. Once they're running, you can access the API by going to `http://localhost:8080/my-flask-api/v1` in your web browser.

## Usage

There are two available endpoints:

1. `POST /products/scrape` – This endpoint takes a `product_name` in the request body and scrapes Amazon for products matching that name.

2. `GET /products` – This endpoint returns all scraped Amazon products.
