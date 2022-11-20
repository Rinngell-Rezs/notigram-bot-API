FROM python
 
WORKDIR /home/bot

COPY ./requirements.txt /home/bot/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /home/bot/requirements.txt

COPY . /home/bot
 
CMD ["uvicorn", "bot:app"]