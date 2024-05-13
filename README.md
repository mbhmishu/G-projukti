<h1> Project setup & run environment </h1>

Ensure you have python3 installed

Clone the repository

create a virtual environment using virtualenv venv( python -m venv env)

Activate the virtual environment by running source venv/bin/activate

On Windows use source venv\Scripts\activate

Install the dependencies using pip install -r requirements.txt

create a dot env file (name: .env) and copy the content fo dotenv-example.txt (SECRET_KEY & DEBUG)  

Migrate existing db tables by running python manage.py migrate ( py manage.py makemigrations & python manage.py migrate )

create super user or admin (python manage.py createsuperuser)

Run the django development server using python manage.py runserver






<h1>Task requirment </h1>

<h4>Django Backend Developer</h4> 

1. Create a discount model there are 2 types of discounts (Date and Time Wise) and discount amount is type is also 2 type (Flat amount, and percentage amounts)

2. In Discount create API must be checked when the date-wise create must be start and end date given and also given time-wise create must be start and end time given. when the discount amount is a percentage, then the amount must be less than 100.

For Discount Need API List:
1. Post
2. Patch
3. List
4. Delete
5. Details
6. Partially Search API
7. all valid discount list show

3. Create a Category And Product Model that is related (One to Many) relation.

For Category Need API List:
1. Post
2. Patch
3. List
4. Delete
5. Details
6. Partially Search API






For Product Need API List:

[* In the response must be details showing category and discount ]

1. Post
2. Patch
3. List
4. Delete
5. Details
6. Partially Search API
7. Add discount on all food by a single API
