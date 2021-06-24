# NITADDA
This is a "NITADDA" which gives students from various colleges the ability to upload notes, books,and examination papers. It also helps students to stay updated with all latest technologies and news with blog posts.

The backend is completely build on Django and frontend using html, css, bootrap and javascript.
### Features
* 2 different roles defined i.e Students and college moderators.
* Login/Registration for students
* Login/Registration for moderators with custom permissions.
* Student can upload study materials.
* Student can download and view study materials.
* Student can read blog post for upldated news on various contests and technologies.
* Student and Admin can send messages and get notification.
* Admin will approve all study material.
* Admin will answer all the queries.
* Student can like and report study materials.
* Admin can report most reported materials.
* Admin can write blog post dynamically with markdown editor.

## Project Setup
1. Clone this repository: `https://github.com/himanshukadian/nitadda.git`.
2. Change the current directory to folder: `cd ./nitadda`.
3. Create a virutal environment and install all backend dependencies with pip: `pip install -r requirements.txt`.
4. Start the virtual environment: `env\Script\activate`.
5. Run `python manage.py makemigrations`.
6. Run `python manage.py migrate`.
7. Create a superuser: `python manage.py createsuperuser`
8. Run the server: `python manage.py runserver`.

