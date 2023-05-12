FROM python

RUN useradd -ms /bin/bash app

RUN apt-get update && \
    apt-get -y install sudo

USER app

WORKDIR /home/app/code

COPY --chown=app . .

RUN pip install -r requirements.txt --user


