# Restaurant Ecommerce API Documentation

```markdown
This documentation outlines the RESTful API endpoints and operations for the restaurant ecommerce project. The project is built using Django and includes modules for restaurant management, menu handling, order processing, and user management.

## Installation

To set up and run the project locally, follow these steps:

### Prerequisites

- Python 3.x
- Django/Rest Framework
- PostgreSQL (or other database of your choice)

### Clone the Repository

```bash
git clone https://github.com/pratik-udeshi1/restaurant-backend.git
```

### Change to the Project Directory

```bash
cd restaurant-backend
```

### Create and Activate a Virtual Environment

On Unix/Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

### Configure Database Settings

Update the database name, username, and password in `settings.py`.

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

### Usage

1. Access the Django admin interface by visiting `http://localhost:8000/admin/` and log in with the superuser credentials you created.

2. Use the admin interface to manage restaurant data, including reservations, payments, inventory, reviews, and more.

3. To access the API collections, refer to the [API Documentation](#restaurant-ecommerce-api-documentation) for details on each module's API endpoints and usage examples.

## API Documentation

Access the Swagger documentation by visiting `http://localhost:8000/swagger/`

### API E.g.

### Order API

#### Get Orders for a Restaurant

- **Endpoint:** `/api/order/restaurant/{restaurant_id}`
- **Methods:** GET
- **Parameters:**
  - `restaurant_id` (path) - ID of the restaurant
- **Response:**
  - 200 OK
  - Example:
    ```json
    [
      {
        "id": "order_id_1",
        "total": "50.00",
        "items": ["item_id_1", "item_id_2"],
        "user": "user_id_1",
        "created_at": "2023-01-15T12:00:00Z",
        "updated_at": "2023-01-15T12:30:00Z",
        "status": "processed",
        "special_instructions": "No onions",
        "payment_intent": "payment_intent_id_1",
        "payment_status": "completed",
        "restaurant": "restaurant_id_1",
        "menu_items": ["menu_item_id_1", "menu_item_id_2"]
      },
      {
        "id": "order_id_2",
        "total": "25.00",
        "items": ["item_id_3"],
        "user": "user_id_2",
        "created_at": "2023-01-16T14:00:00Z",
        "updated_at": "2023-01-16T14:15:00Z",
        "status": "pending",
        "special_instructions": null,
        "payment_intent": "payment_intent_id_2",
        "payment_status": "pending",
        "restaurant": "restaurant_id_1",
        "menu_items": ["menu_item_id_3"]
      }
    ]
    ```
- **Description:** Get a list of orders for a specific restaurant.

## Getting Started

Follow the steps in the [Installation](#installation) section to set up and run the project locally.

## Contributing

If you'd like to contribute to this project, please follow the [CONTRIBUTING.md](CONTRIBUTING.md) guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize the README further based on your project's specific details and requirements.
```