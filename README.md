# CivicsTest

The Civics Practice Application contains the questions and answers from the 2008 version of the civics test 
which is made up of 100 questions and answers about American government and history.

The live app can be found by the following this link:  
http://civicstest.davtyan.net/cards/

![](https://github.com/mr-davtyan/CivicsTest/blob/master/preview.png?raw=true)

##Docker image:  
https://hub.docker.com/repository/docker/davtyan/django-civics-test

## Features
- Django based project.
- CSS only (no JS) for the main app.
- View for mobile devices supported.
- Keeps user session to save the current order and group.

## Notice
- The database is prefilled with the questions.
- There is no Django admin account, you need to create it from console.
- Please make sure you have changed the SECRET_KEY and DEBUG mode before publishing.
- Questions update in text-only format can be found on the official USCIS web page:  
https://www.uscis.gov/citizenship/find-study-materials-and-resources/study-for-the-test  
And uploaded through the admin part of the website.