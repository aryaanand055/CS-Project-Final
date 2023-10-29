# Step-by-Step Guide: How to Download and Run my Project

## Getting Started

### Prerequisites

- Python (3.6 or higher)
- pip (Python package manager)

### Clone the Repository

Clone the repository to your local machine using Git:

1. `git clone https://github.com/aryaanand055/CS-Project-Final.git`

2. Navigate to the project directory:
   ```
   cd ecommerce_project
   ```
(Ignore the next step if you don't have any other django projects in usage).  
Create a virtual environment (optional) and activate it: 

1. `python -m venv venv` (Create a virtual environment)
2. `source venv/bin/activate` (Activate the virtual environment)

Install project dependencies from the `requirements.txt` file:

1. `pip install -r requirements.txt`

## Running the Project

Apply database migrations:

1. `python manage.py migrate`
   
Create a superuser (for admin access):  
(Not Neccessary if you are just viewing the site)


1. `python manage.py createsuperuser`

Run the development server:

1. `python manage.py runserver`

The project should be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Access the admin interface by navigating to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/), and log in using the superuser credentials.

## Usage

This is a simple ecommerce project. It includes filters for categories, search bar, wishlist and cart along with signup and login.

## Contributing

If you want to contribute to this project, follow these steps:

- Fork the project on GitHub.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them with descriptive messages.
- Push your changes to your fork.
- Submit a pull request to the original repository.

## License

This project is created by Arya A
