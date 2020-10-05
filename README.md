# portfolio_django
Проект и приложение для получения информации об инвестиционных инструментах

# Install
## [Install Django](https://docs.djangoproject.com/en/1.8/howto/windows/#install-django)
Для установки Django используйте PIP:
`> pip install django`
## Clone
Клонируйте проект с GitHub: 
`> git clone https://github.com/SubMax/portfolio_django.git`
## Virtual environment
1. Установите инструмент для создания изолированного виртуального окружения Python: 
`> pip install virtualenv`
1. Создайте виртуальное окружение в папке с проектом 
`> ...\portfolio_django> virtualenv venv`
1. Активируйте виртуальное окружение и установите зависимости (порядок пунктов важен):
  - Запустите скрипт __activate__ `...\portfolio_django\venv\Scripts> activate`. 
Теперь в командной строке должен отображаться префикс с именем вашего виртуального окружения в данном случае __(venv)__:
`(venv) C:\...\portfolio_django\venv\Scripts>`
  - Установите зависимости: `(venv) ...\portfolio_django\portfolio_prj> python -m pip install -r requirements.txt`
## Migrations Django
1. Создайте новую миграцию: `(venv) ...\portfolio_django\portfolio_prj> manage.py makemigrations`
2. Примените миграцию: `(venv) ...\portfolio_django\portfolio_prj> manage.py migrate `
## Runserver
Запустите сервер: `(venv) ...\portfolio_django\portfolio_prj> manage.py runserver 8080 `
