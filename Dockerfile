# use Python 3.9 base image.
FROM python:3.9

# set work dir
WORKDIR /app

# COPY Python exec file to WORKDIR
COPY wondroussortinghatbot.py .
COPY requirements.txt .

# install requirements
RUN pip install -r requirements.txt

# expose 8080 endpoint
# EXPOSE 8080

# set ENV Variable
ENV TG_BOT_TOKEN=XXXXXXXXXX
ENV WALLET_URL=https://cxlinks.us

# 运行 Python 脚本
CMD ["python", "wondroussortinghatbot.py"]