# pull official base image
FROM amazonlinux

# create the app user
RUN yum -y install shadow-utils.x86_64 util-linux python3 python3-pip
RUN useradd -m -d /home/app -G root app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip -r requirements.txt

COPY app.py $APP_HOME
COPY wsgi.py $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]