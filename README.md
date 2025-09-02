# ModernShop - Modern E-commerce Django Application

A fully-featured, modern e-commerce platform built with Django, featuring a beautiful responsive design, advanced functionality, and seamless user experience.

## 🚀 Features

### Backend Features
- **User Authentication & Authorization**
  - User registration and login
  - Password strength validation
  - Session management
  - User profile management

- **Product Management**
  - Product categories with hierarchical structure
  - Product search and filtering
  - Advanced sorting options (price, rating, date)
  - Product reviews and ratings system
  - Stock management
  - Discount pricing

- **Shopping Cart System**
  - Persistent cart functionality
  - Real-time cart updates via AJAX
  - Quantity management
  - Cart item removal

- **Order Management**
  - Complete order processing workflow
  - Order status tracking
  - Order history for users
  - Order details with timeline

- **Payment Integration**
  - Razorpay payment gateway integration
  - Secure payment processing
  - Payment verification
  - Cash on Delivery option

- **Admin Panel**
  - Comprehensive admin interface
  - Product and category management
  - Order management
  - User management
  - Sales analytics

### Frontend Features
- **Modern Responsive Design**
  - Bootstrap 5 framework
  - Mobile-first approach
  - Beautiful animations and transitions
  - Professional UI/UX

- **Interactive Components**
  - Real-time search suggestions
  - Dynamic cart updates
  - Product quick view
  - Image lazy loading
  - Smooth scrolling

- **User Experience**
  - Intuitive navigation
  - Breadcrumb navigation
  - Product filtering and sorting
  - Wishlist functionality
  - Order tracking

## 🛠️ Technology Stack

- **Backend**: Django 5.0.2
- **Frontend**: Bootstrap 5, jQuery, CSS3
- **Database**: SQLite (development), PostgreSQL (production)
- **Payment**: Razorpay
- **Icons**: Bootstrap Icons
- **Styling**: Custom CSS with CSS Variables

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/IshwikVashishtha/Ecomsite.git
   cd ecomsite
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   .venv/bin/activate  # On Mac/Linux: Source venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   RAZORPAY_KEY_ID=your-razorpay-key-id
   RAZORPAY_KEY_SECRET=your-razorpay-secret-key
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## 🗄️ Database Models

### Core Models
- **User**: Extended Django User model
- **Category**: Product categories with hierarchical structure
- **Product**: Products with pricing, stock, and metadata
- **Cart**: Shopping cart for users
- **CartItem**: Individual items in cart
- **Order**: Complete order information
- **OrderItem**: Individual items in orders
- **Review**: Product reviews and ratings

### Model Relationships
- User → Cart (One-to-One)
- User → Orders (One-to-Many)
- Category → Products (One-to-Many)
- Product → Reviews (One-to-Many)
- Cart → CartItems (One-to-Many)
- Order → OrderItems (One-to-Many)

## 🔧 Configuration

### Settings Configuration
The application uses Django's settings system with environment variable support:

```python
# settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Razorpay Configuration
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')
```

### Static Files
Static files are organized in the `shop/static/shop/` directory:
- CSS: `shop/static/shop/css/style.css`
- JavaScript: `shop/static/shop/js/main.js`
- Images: `shop/static/shop/images/`

## 🎨 Customization

### Styling
The application uses CSS custom properties for easy theming:

```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --danger-color: #dc3545;
    --border-radius: 0.5rem;
    --box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    --transition: all 0.3s ease;
}
```

### Templates
Templates are organized in `shop/templates/shop/`:
- `base.html`: Main layout template
- `index.html`: Home page with product listing
- `product_detail.html`: Individual product page
- `cart.html`: Shopping cart page
- `checkout.html`: Checkout process
- `login.html` & `register.html`: Authentication pages

## 🔒 Security Features

- CSRF protection on all forms
- XSS prevention
- SQL injection protection
- Secure password hashing
- Session security
- Payment signature verification

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: > 768px

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in settings
2. Configure production database (PostgreSQL recommended)
3. Set up static file serving (nginx/Apache)
4. Configure HTTPS
5. Set up environment variables
6. Run `python manage.py collectstatic`

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📊 API Endpoints

### Cart Management
- `POST /add-to-cart/`: Add product to cart
- `POST /update-cart-item/`: Update cart item quantity
- `POST /remove-from-cart/`: Remove item from cart

### Payment
- `POST /create-razorpay-order/`: Create payment order
- `POST /verify-payment/`: Verify payment signature

### Orders
- `GET /orders/`: User's order history
- `GET /order/<uuid>/`: Order details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Razorpay for payment gateway integration
- All contributors and users of this project

---

**ModernShop** - Building the future of e-commerce, one pixel at a time! 🛒✨

