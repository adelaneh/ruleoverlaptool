#docker-compose run -d --service-ports web
#docker-compose run -d --service-ports web python manage.py runserver
#docker run -d -P --name django_rulemanagement dockerimages_web python manage.py runserver
docker run -d -p 8000:8000 --name rule_management -w="/code" rulemanagemenet_web python manage.py runserver 0.0.0.0:8000
