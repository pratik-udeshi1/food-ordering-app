# Restaurant Backend Project

This is the backend of a restaurant management system built using Django. The project consists of several modules to manage various aspects of a restaurant's operations.

## Modules

1. **Restaurant**: Create and list all restaurants.
2. **Menu**: Handles menu for the restaurant.
3  **Order**: Manage customer food orders.
4  **Payment**: Handle payment processing for customer orders via Stripe API.
5. **User**: Manages users on the platform.

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.x
- Django
- PostgreSQL (or other database of your choice)
- Stripe (Payment API)
- Boto AWS (AWS Operations)
- Swagger (API Documentation)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/pratik-udeshi1/restaurant-backend.git
   ```

2. Change to the project directory:

   ```
   cd restaurant-backend
   ```

3. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

5. Configure your database settings in `settings.py`. Make sure to update the database name, username, and password. (or create .env for env variables)

6. Apply migrations:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create a superuser to access the Django admin interface:

   ```
   python manage.py createsuperuser
   ```

8. Run the development server:

   ```
   python manage.py runserver
   ```

### Usage

1. Access the Django admin interface by visiting `http://localhost:8000/admin/` and log in with the superuser credentials you created.

2. Use the admin interface to manage restaurant data, including reservations, payments, inventory, reviews, and more.

3. To access the API collections visit `http://localhost:8000/swagger/`. Here's an example format:

   #### Order API

   - Endpoint: `/api/order/`
   - Methods: GET, POST, PUT, DELETE

   ##### Basic Usage

   - To create a order:
     ```
     POST /api/order/
     {
       "user": "John Doe",
       "menu_items": [list of menu items],
       "special_instructions": "Make all spicy, Indian style!!"
     }
     ```

   - To list order:
     ```
     GET /api/order/
     ```

   - To update the order:
     ```
     PUT /api/order/{order_id}/
     {
       "status": "processing"
     }
     ```

   - To cancel the order:
     ```
     DELETE /api/order/{order_id}/
     ```

Repeat the above format for each module's API endpoints.

## Running Test Cases
#### To run test cases for the project, use the following command:
```
python manage.py test
```


## Contributing

If you'd like to fork this project, please feel free to.

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) file for details.

---

Feel free to customize the README to better suit your project and its specific API endpoints. Make sure to provide more detailed information about each API, input validation, and any other specifics your project may have.