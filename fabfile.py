from fabric.connection import Connection

with Connection('127.0.0.1',port=8000) as c:
    c.run("./manage.py test library_api")
    c.run('add -p && git commit')
    c.run("git push")