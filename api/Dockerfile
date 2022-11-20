FROM python

EXPOSE 8000
 
WORKDIR /home/api

COPY ./requirements.txt /home/api/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /home/api/requirements.txt

COPY . /home/api
 
CMD ["uvicorn", "app:API", "--host", "0.0.0.0", "--port", "8000"]