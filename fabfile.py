__author__ = 'centralstation'

from fabric.api import *


env.hosts = ['188.166.57.42']
env.user = 'root'
env.key_filename = 'liams.pem'
code_dir = '/var/www/dukebox/'


def deploy():
    with cd(code_dir):
        run("source bin/activate")
        run("git pull origin master")
        run("pip install -r requirements.txt ")
        run("python manage.py collectstatic --noinput")
        run("sudo service apache2 restart")
