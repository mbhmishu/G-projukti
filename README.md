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
