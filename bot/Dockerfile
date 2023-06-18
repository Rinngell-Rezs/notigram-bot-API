FROM python

EXPOSE 5000

ENV bot_TOKEN="5950145264:AAE40k_Dm9cb7P4Qly9P2_oWJVCEodFFhus"
  
ENV mongo_URI="mongodb+srv://notigram:seY3DsImx02HBjY3@cluster0.dnee7co.mongodb.net/?retryWrites=true&w=majority"
 
WORKDIR /home/bot

COPY ./requirements.txt /home/bot/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /home/bot/requirements.txt

COPY . /home/bot
 
CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "5000"]