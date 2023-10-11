# Try-Django-3.2

Welcome to the Try-Django repository! This repository contains a Django tutorial that will help you learn the fundamentals of building web applications with Django, a high-level Python web framework. Whether you're a beginner or an experienced developer looking to learn Django, this tutorial is designed to get you started.<br>
A huge shout-out to "Coding for Entrepreneurs" for putting together this fantastic course!<br>
Checkout their youtube channel for this course: <br>
[Try-Django-3.2 Youtube Course](https://www.youtube.com/watch?v=SlHBNXW1rTk&list=PLEsfXFp6DpzRMby_cSoWTFw8zaMdTEXgL&ab_channel=CodingEntrepreneurs)

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Tutorial Content](#tutorial-content)
5. [Contributing](#contributing)


## Getting Started
In this project you will learn django which is a popular backend framework in python.
This project includes:
- django models
- django forms
- django views
- django authentication
- django admin page
- django signals
- django urls
- django db management with migrations & ..
- configuring settings in django
- diffrent templates in html, css and js
- bootstrap framework
- and more!

## Prerequisites
1. Install python 3.6 on your machine. [Install Python](https://www.python.org/downloads/release/python-368/) <br>
2. Perhaps you need Git! [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) <br>

## Installation

```bash
# Clone the repository
git clone https://github.com/amirh-far/Try-Django.git
cd Try-Django

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create Tables in Database for Existing Apps:
python manage.py makemigrations
python manage.py migrate

# Run the Django development server
python manage.py runserver
```
## Tutorial Content
In this project we don't focus on fancy frontend because we are focusing on learning Django!

#### Home View
<img src="https://github.com/amirh-far/Try-Django/blob/main/readme-images-files/home%20view.png"/>

#### Login View
<img src="https://github.com/amirh-far/Try-Django/blob/main/readme-images-files/login%20view.png"/>

#### Recipes List View
<img src="https://github.com/amirh-far/Try-Django/blob/main/readme-images-files/recipes%20list%20view.png"/>

#### Create-Update Recipe View
<img src="https://github.com/amirh-far/Try-Django/blob/main/readme-images-files/create-update%20view.png"/>

## Contributing

Feel free to modify this template to suit your specific tutorial and repository. Ensure that you provide clear and concise information to help users get started with your Django tutorial. <br>
Happy coding!
