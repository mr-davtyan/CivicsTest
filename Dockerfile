# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.8-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
	
RUN mkdir -p /opt/CivicsTest
COPY . /opt/CivicsTest/
WORKDIR /opt/CivicsTest
RUN pip install -r requirements.txt --cache-dir /opt/CivicsTest/.pip_cache
RUN chown -R www-data:www-data /opt/CivicsTest

EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/CivicsTest/start-server.sh"]