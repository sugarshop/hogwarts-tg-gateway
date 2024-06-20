# use Python 3.9 base image.
FROM python:3.9

# set work dir
WORKDIR /app

# COPY Python exec file to WORKDIR
COPY . .
COPY script/bootstrap.sh .

# install requirements
RUN pip install -r requirements.txt

# Give execute permission to bootstrap.sh
RUN chmod +x /app/bootstrap.sh

# expose 8080 endpoint
# EXPOSE 8080

# set ENV Variable
ENV TG_BOT_TOKEN=XXXXX
ENV WALLET_URL=https://cxlinks.us

# bootstrap
CMD ["./bootstrap.sh"]