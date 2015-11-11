from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/rowanv/giraffe_dash.git'  #1

def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)  #23
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    #_update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):  #1
        run('cd %s && git fetch' % (source_folder,))  #23
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))  #4
    current_commit = local("git log -n 1 --format=%H", capture=True)  #5
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))  #6

'''def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/rowanv_web/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")  #1
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)  #2
    )
    secret_key_file = source_folder + '/rowanv_web/secret_key.py'
    if not exists(secret_key_file):  #3
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')'''

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'): #1
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % ( #2
            virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % ( # 1
        source_folder,
    ))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))


