FROM python

EXPOSE 8080

ENV bot_TOKEN="<bot_token>"
  
ENV mongo_URI="<db_uri>"

ENV PORT=8080
 
WORKDIR /home/api

COPY ./requirements.txt /home/api/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /home/api/requirements.txt

COPY . /home/api
 
CMD ["uvicorn", "app:API", "--host", "0.0.0.0", "--port", "8080"]
