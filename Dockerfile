FROM python:slim
RUN apt-get update && apt-get install -y openssl
WORKDIR /deploy
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV PYTHONUNBUFFERED=1
COPY entrypoint.sh .
RUN ["chmod", "+x", "./entrypoint.sh"]
EXPOSE 8443
ENTRYPOINT [ "/bin/bash", "./entrypoint.sh" ] 
