# Ecommerce Online Shopping

A modern, responsive eCommerce platform built with Django. It allows users to browse, search, and purchase a variety of men’s and women’s shoes. The platform includes features like a shopping cart, user authentication, checkout with M-Pesa, email and SMS notifications, and an admin dashboard for managing orders.


##  Features

-  User registration & login
-  Browse shoes by category (Men/Women)
-  Add to cart with live cart count
- View & update cart (quantity + remove items)
- Checkout page with payment method:
  - Pay Before Delivery (via M-Pesa)
  - Pay After Delivery
-  Order confirmation via Email & SMS
-  Admin panel to manage orders and products
-  Flash messages for actions (add, remove, update)
-  Responsive design using Tailwind CSS

---

##  Tech Stack

- **Backend**: Django, Python
- **Frontend**: HTML, Tailwind CSS
- **Database**: PostgreSQL or SQLite (default)
- **Email**: SMTP (Gmail or any SMTP provider)


---

##  Project Structure
creative/
├── store/
│ ├── models.py # Shoe, CartItem, Order, OrderItem
│ ├── views.py # Home, Cart, Checkout logic
│ ├── urls.py # App-level routes
│ ├── templates/store/ # HTML templates
│ └── static/images/ # Product images
├── creative/ # Project config
├── db.sqlite3 # Default database
└── manage.py

