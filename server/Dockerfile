FROM python:3.6.7

ENV PYTHONUNBUFFERED 1
ENV HOME /root
ENV APP_DIR /app
ENV LOG_DIR /app/logs
ENV C_FORCE_ROOT=true

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
        apt-transport-https \
        ca-certificates \
        gnupg \
        curl \
        git \
        imagemagick \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        openssh-client \
        file \
        libtiff5-dev \
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        tcl8.6-dev \
        tk8.6-dev \
        python-tk \
        libncurses5-dev \
        python-pip \
        python3-dev


# Clean up APT and bundler when done.
RUN rm -rf /usr/share/doc \
           /usr/share/man \
           /usr/share/groff \
           /usr/share/info \
           /usr/share/lintian \
           /usr/share/linda \
           /usr/share/locale/ \
           /var/cache/man

# Clean up APT when done.
RUN apt-get clean
RUN apt-get autoclean
RUN apt-get autoremove
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN mkdir -p $APP_DIR
RUN mkdir -p $LOG_DIR

COPY ./requirement.txt /requirement.txt

RUN pip install -r requirement.txt \
  && groupadd -r webserver \
  && useradd -r -g webserver webserver

ADD . $APP_DIR/
WORKDIR $APP_DIR
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
