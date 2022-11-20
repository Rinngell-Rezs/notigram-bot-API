FROM python

EXPOSE 5000
 
WORKDIR /home/bot

COPY ./requirements.txt /home/bot/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /home/bot/requirements.txt

COPY . /home/bot
 
CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "5000"]