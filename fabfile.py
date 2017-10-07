from fabric.api import local, run, cd, env, settings, shell_env

env.use_ssh_config = True
env.user = 'pyconkr'
env.hosts = ['pythonkorea1']


def deploy(target='dev-seminar', sha1=None):
    if sha1 is None:
        # get current working git sha1
        sha1 = local('git rev-parse HEAD', capture=True)

    # server code reset to current working sha1
    home_dir = '/home/pyconkr/{target}.pycon.kr/'.format(target=target)

    if target == 'dev-seminar':
        python_env = '/home/pyconkr/.pyenv/versions/dev-seminar'
        django_settings_module='seminar.settings.dev'
    elif target == 'seminar':
        python_env = '/home/pyconkr/.pyenv/versions/seminar'
        django_settings_module='seminar.settings.production'
    else:
        raise Exception

    with settings(cd(home_dir), shell_env(DJANGO_SETTINGS_MODULE=django_settings_module)):
        run('git fetch --all -p')
        run('git reset --hard ' + sha1)

        # run('bower install')
        run('%s/bin/pip install -r requirements.txt' % python_env)
        # run('%s/bin/python manage.py compilemessages' % python_env)
        run('%s/bin/python manage.py migrate' % python_env)
        # run('%s/bin/python manage.py collectstatic --noinput' % python_env)

        # worker reload
        run('echo r > /home/pyconkr/run/%s.fifo' % target)
