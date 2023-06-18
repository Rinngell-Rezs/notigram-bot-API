FROM python

EXPOSE 8080

ENV bot_TOKEN="5950145264:AAE40k_Dm9cb7P4Qly9P2_oWJVCEodFFhus"
  
ENV mongo_URI="mongodb+srv://notigram:seY3DsImx02HBjY3@cluster0.dnee7co.mongodb.net/?retryWrites=true&w=majority"

ENV PORT=8080
 
WORKDIR /home/api

COPY ./requirements.txt /home/api/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /home/api/requirements.txt

COPY . /home/api
 
CMD ["uvicorn", "app:API", "--host", "0.0.0.0", "--port", "8080"]