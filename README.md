# Ecomsite: Django E-Commerce Web Application

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Ecomsite** is a simple yet functional e-commerce web application built with Django. It allows users to browse products, search, view details, add items to a cart (using localStorage), and place orders. The project demonstrates core e-commerce features and is a great starting point for learning Django and web development best practices.

## Features
- Product listing with pagination
- Product search by name
- Product detail view with similar product suggestions
- Add to cart (client-side, using localStorage)
- Cart popover in navbar with item management
- Checkout form with order submission
- Admin interface for managing products and orders
- Responsive design using Bootstrap 5

## Tech Stack
- **Backend:** Django 5.x
- **Frontend:** HTML, CSS (custom + Bootstrap 5), JavaScript (vanilla + jQuery)
- **Database:** SQLite (default for Django)

## Project Structure
```
ecomsite/
├── ecomsite/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── shop/               # Main app
│   ├── admin.py        # Admin customizations
│   ├── models.py       # Product & Order models
│   ├── views.py        # Main views (index, detail, checkout)
│   ├── templates/
│   │   └── shop/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── detail.html
│   │       └── checkout.html
│   ├── static/
│   │   └── shop/
│   │       └── style.css
│   └── ...
├── manage.py
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- (Optional) Virtual environment tool (e.g., `venv` or `virtualenv`)

### 1. Clone the Repository
```bash
git clone https://github.com/IshwikVashishtha/Ecomsite.git
cd ecomsite
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser (for Admin Panel)
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage
- **Browse Products:** Home page lists products with pagination and search bar.
- **View Details:** Click on a product to see details and similar products.
- **Add to Cart:** Use the "Add to Cart" button; cart is managed in browser localStorage.
- **View Cart:** Click the cart button in the navbar to see items and proceed to checkout.
- **Checkout:** Fill in the form and submit to place an order.
- **Admin:** Visit `/admin/` to manage products and orders (login as superuser).


## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

