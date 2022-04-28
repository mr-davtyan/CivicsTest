# CivicsTest

The Civics Practice Application contains the questions and answers from the 2008 version of the civics test 
which is made up of 100 questions and answers about American government and history.

The live app (Massachusetts version of tests) can be found by the following this link:  
http://civicstest.davtyan.net

![](https://github.com/mr-davtyan/CivicsTest/blob/master/preview.png?raw=true)

## Docker images:  
https://hub.docker.com/r/davtyan/django-civics-test

https://hub.docker.com/r/davtyan/django-civics-test-ma

## Features
- Django based project.
- View for mobile devices supported.
- Fully functional if JS is disabled.
- Keeps user session to save the current progress, order and group.
- Use `python manage.py runserver 0.0.0.0:8000` for development 
  (Debug-On, local SQL DB file, admin account needs to be created manually
  `python manage.py createsuperuser`).
- Use `docker-compose up --build` for production. Put your own credentials 
  to the `.env` file.

## Notice
- The database can be prefilled with the questions on startup.
- There is no Django admin account, you need to create it from console and 
  from the `.env` file.
- Please make sure you have changed the SECRET_KEY and DEBUG mode before publishing.
- Questions update in text-only format can be found on the official USCIS web page:  
https://www.uscis.gov/citizenship/find-study-materials-and-resources/study-for-the-test  
And uploaded through the admin part of the website.  
- Update the text file before uploading to include all the current government updates. 
