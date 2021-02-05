FROM python:3.7
MAINTAINER Thomas Maschler thomas.maschler@wri.org

ENV NAME arcgis_proxy
ENV USER arcgis_proxy

RUN apt-get update && apt-get --assume-yes upgrade && \
   apt-get --assume-yes install bash git libssl-dev \
   libffi-dev gcc python3-dev musl-dev proj-bin

RUN addgroup $USER && adduser --shell /bin/bash --disabled-password --ingroup $USER $USER

RUN pip install --upgrade pip
RUN pip install virtualenv gunicorn gevent

RUN mkdir -p /opt/$NAME
RUN cd /opt/$NAME && virtualenv venv && . venv/bin/activate
COPY requirements.txt /opt/$NAME/requirements.txt
COPY requirements_dev.txt /opt/$NAME/requirements_dev.txt
RUN cd /opt/$NAME && pip install -r requirements.txt
RUN cd /opt/$NAME && pip install -r requirements_dev.txt

COPY entrypoint.sh /opt/$NAME/entrypoint.sh
COPY main.py /opt/$NAME/main.py
COPY test.py /opt/$NAME/test.py
COPY gunicorn.py /opt/$NAME/gunicorn.py

# Copy the application folder inside the container
WORKDIR /opt/$NAME

COPY ./$NAME /opt/$NAME/$NAME
COPY ./microservice /opt/$NAME/microservice
RUN chown $USER:$USER /opt/$NAME

# Tell Docker we are going to use this ports
EXPOSE 5700
USER $USER

# Launch script
ENTRYPOINT ["./entrypoint.sh"]
