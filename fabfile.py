import os

from fabric.state import env
from fabric.api import cd, run, sudo, settings
from fabric.contrib.files import exists, upload_template

env.hosts = ['sergey@138.68.145.206']

def _set_env():
    home_path = '/var/www/'
    env.user = 'sergey'
    env.PROJECT_NAME = 'open_music'
    env.TEMPLATES_PATH = 'deploy_templates'
    env.BASE_PYTHON_PATH = '/usr/bin/python3.5'
    env.REMOTE_PROJECT_PATH = os.path.join(home_path, 'src/%s/' % env.PROJECT_NAME)
    env.VIRTUAL_ENV_PATH = os.path.join(
        home_path,
        'src/.virtualenvs/%s/' % env.PROJECT_NAME
    )
    env.PIP = os.path.join(env.VIRTUAL_ENV_PATH, 'bin/pip')
    env.PYTHON = os.path.join(env.VIRTUAL_ENV_PATH, 'bin/python')
    env.DJANGO_CONFIGURATION_NAME = 'Prod'
    env.UWSGI_PROCESSES = 5
    env.DOMAIN_NAME = '138.68.145.206'
    env.UWSGI_MODULE = 'music_project'
    env.SUDO_PERMISSION =True
    env.GIT_REP_PATH ='https://github.com/seregagavrilov/open_music'

def bootstrap():
    _set_env()

    install_system_packages(
        packages=[
            'python3-dev',
            'python-pip',
            'nginx',
            'git'
        ]
    )
    # _put_template('uwsgi.service', '/etc/systemd/system/', use_sudo=True)
    create_folders()
    configure_nginx()
    configure_uwsgi()
    update_src()
    create_virtualenv()
    install_libs()
    restart_all()
    run_management_command('collectstatic --noinput')
    run_management_command('migrate')


def install_system_packages(packages, do_apt_get_update=True):
    if do_apt_get_update:
        sudo('apt-get update')
    sudo('apt-get install  %s' % (" ".join(packages)))


def configure_nginx():
    _put_template('nginx.conf', '/etc/nginx/sites-available/nginx.conf', use_sudo=True)


def configure_uwsgi():
    uwsgi_config_filename = 'project.ini'
    uwsgi_base_config_filename = 'uwsgi.service'
    _put_template(uwsgi_config_filename, '/etc/uwsgi/apps-available/', use_sudo=True)
    apps_enabled_link_path = '/etc/uwsgi/apps-enabled/%s' % uwsgi_config_filename
    if not exists(apps_enabled_link_path):
        sudo(
            'ln -s /etc/uwsgi/apps-available/%(file)s %(link)s' % {
                'file': uwsgi_config_filename,
                'link': apps_enabled_link_path,
            }
        )

    _put_template(uwsgi_base_config_filename, '/etc/systemd/system/uwsgi.service', use_sudo=True)


def create_folders():
    _mkdir(env.VIRTUAL_ENV_PATH, is_sudo=True)
    _mkdir(os.path.join(env.REMOTE_PROJECT_PATH, 'static'), is_sudo=True)
    _mkdir('/etc/uwsgi/apps-enabled/', is_sudo=True)
    _mkdir('/etc/uwsgi/apps-available/', is_sudo=True)
    # _mkdir('/etc/systemd/system/uwsgi.service', is_sudo=True)

def update_src():
    runner = return_runner_if_is_sudo()
    if not is_git_repo_exists():
        clear_project_folder(True)
        clone_src(True)
    with cd(env.REMOTE_PROJECT_PATH):
        runner('git pull')


def clone_src(is_sudo=False):
    runner = sudo if is_sudo else run
    with cd(env.REMOTE_PROJECT_PATH):
        runner('git clone %s .' % env.GIT_REP_PATH)


def is_git_repo_exists():
    return exists(os.path.join(env.REMOTE_PROJECT_PATH, '.git'))


def clear_project_folder(is_sudo):
    runner = sudo if is_sudo else run
    runner('rm -rf %s*' % env.REMOTE_PROJECT_PATH)


def return_runner_if_is_sudo():
    return sudo if env.SUDO_PERMISSION else run


def create_virtualenv(reinstall_pip=True):
    runner = return_runner_if_is_sudo()
    if reinstall_pip:  # http://askubuntu.com/questions/488529/
        runner('%s -m venv --without-pip %s' % (env.BASE_PYTHON_PATH, env.VIRTUAL_ENV_PATH))
        activate_command = 'source %s' % os.path.join(env.VIRTUAL_ENV_PATH, 'bin/activate')
        runner('%s && curl https://bootstrap.pypa.io/get-pip.py | python' % activate_command)
    else:
        runner('%s -m venv  %s' % (env.BASE_PYTHON_PATH, env.VIRTUAL_ENV_PATH))


def install_libs():
    runner = return_runner_if_is_sudo()
    requirements_path = os.path.join(env.REMOTE_PROJECT_PATH, 'requirements.txt')
    runner('%s install -r %s' % (env.PIP, requirements_path))


# def restart_all():
#     #sudo('service nginx restart')
#     restart_initctl_services(['uwsgi'])


def run_management_command(command):
    run('DJANGO_CONFIGURATION=%s %s %s %s' % (
        env.DJANGO_CONFIGURATION_NAME,
        env.PYTHON,
        os.path.join(env.REMOTE_PROJECT_PATH, 'open_music', 'manage.py'),
        command
    ))


def _put_template(template_name, destination_full_path, use_sudo=False, backup_path=None):
    context = {
        'uwsgi_module': env.UWSGI_MODULE,
        'user': env.user,
        'project_path': env.REMOTE_PROJECT_PATH,
        'uwsgi_processes_amount' : env.UWSGI_PROCESSES,
        'venv_path': env.VIRTUAL_ENV_PATH,
        'python': env.PYTHON,
        'project_name': env.PROJECT_NAME,
        'configuration_name': env.DJANGO_CONFIGURATION_NAME,
        'domain_name' : env.DOMAIN_NAME,
    }
    if backup_path:
        with settings(warn_only=True):
            sudo('mv %s %s' % (destination_full_path, backup_path))
    upload_template(
        os.path.join(env.TEMPLATES_PATH, template_name),
        destination_full_path,
        use_sudo=use_sudo,
        context=context,
        backup=False,
    )


def _mkdir(path, is_sudo=False):
    runner = sudo if is_sudo else run
    runner('mkdir -p %s' % path)


def restart_all(services=None):
    services = services or ['uwsgi', 'nginx']
    sudo('systemctl daemon-reload')
    for service in services:
        sudo('service %s restart' % service)
