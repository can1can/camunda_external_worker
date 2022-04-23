   
# Запуск
Для локального запуска нужно python >= 3.7
1. `cd /way/to/project`
2. `pip3 install -r requirements.txt`
3. `python3 source/main.py -c ./example_config.ini`


# Запуск в Docker 
1. `cd /way/to/project`
2. `docker build -t camunda_course_task .`
3. `docker run --name camunda_course_task -v /way/to/project/config.ini:/app/config.ini camunda_course_task:latest`

# Описание конфига 
[camunda_connector]
location = http://127.0.0.1:8080/engine-rest  
Адрес запущенной камунды. ждя разработки использовался образ `camunda/camunda-bpm-platform:latest`


[email_sender] - Конфигурация отправитиля email  
name = my_sender  
email = my_sender@mail.ru  
smtp_port = 25  
password = 25xAqasQQ1  
smtp_server = smtp.mail.ru  
login = my_sender_login  


#Запуск БП
```
curl -X POST -d '{"variables":{"email":{"value":"my_email@email.com","type":"String"}}}' -H 'Content-Type: application/json' 'http://127.0.0.1:8080/engine-rest/process-definition/key/send_funny_email/submit-form'
```