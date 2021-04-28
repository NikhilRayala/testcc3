Steps to execute the project:

1) install virtual environment
    command:-  pip install virtualenvwrapper-win
2) create test environment
    command:-  mkvirtualenv test
3) copy my file folder and got to file directory
    command:-  cd django_json( go to file directory)
4) install packages from requirements.txt file
    command:-  python -m pip install -r requirements.txt
5) run "python manage.py runserver"
5) open localhost "http://127.0.0.1:8000/"
6) open "http://127.0.0.1:8000/api/ping/"
    we get success message
7) http://127.0.0.1:8000/api/posts/?tags=science,history&sortBy=likes&direction=desc
    we get json output.
    by chamging different fields we get different output's.