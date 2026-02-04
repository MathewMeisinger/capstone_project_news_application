# capstone_project_news_application
This is a capstone project for my course that is a news board application using the Django framework.


# Running project locally
In order to run the project locally you will need to clone the repository to your local machine. There are 3 ways it can be done, using the CLI, using the web browser or using the desktop application. The following link will guide you on how to perform each of those actions:

https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

Once te repository is cloned to your local machine you will need to set up and run a virtual environment (venv). This is done differently on Windows or Linux/Mac:
In the terminal input the following:

For Windows:    python -m venv [your_venv_name_here]
For Mac/Linux:  python3 -m venv [your_venv_name_here]

In order to run your created venv you will need to input a further command into the terminal:

For Windows:    [your_venv_name_here]\scripts\activate
For Mac/Linux:  source [your_venv_name_here]/bin/activate

Once your venv is active you will need to install the project dependencies. You will know your venv is active because the name of your created venv will be displayed in green within your terminal. If not please return to the above steps to rectify. 
To install the dependencies you will need to insert the following code into the terminal:

pip install -r requirements.txt'

Once all the dependencies are finished installing you will need to cd into the root directory of the project (contains the manage.py file) and you will need to run a further command in the terminal:

python manage.py runserver

Then follow the link in the terminal (http://localhost) to display the web application.


# Running project using docker
A docker image has been created and stored in a public repository. Below I will explain the steps to use the application using Docker Playground. Go to the following link and log in or create an account as requested:

https://labs.play-with-docker.com/

Once logged in press the start button. The user will then see ablue block with a countdown timer in the top right corner. Under this there will be an option to add a new instance which the user must click. The user will be provided with a virtual machine (VM) they can use to test docker images. Execute the following command in order to download and run my application using docker:

docker run -d -p 8000:8000 mathewmeisinger/django_capstone_project

Once this is complete there will be an open port on the top of the screen that will enable to user to click and follow in order to have application open in a separate browser window (http://localhost:8000)