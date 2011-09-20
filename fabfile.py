import fabric
from fabric.api import env, local, sudo, cd, prefix
from path import path

env.hosts = ['praveen@173.255.241.59']
env.sphinx_root = '/home/praveen/cows/shutupandship'
env.activate = 'source /home/praveen/.virtualenvs/shush/bin/activate'
master_repo = 'ssh://hg@bitbucket.org/pgollakota/shutupandship'


def run(cmd):
    with cd(env.sphinx_root):
        with prefix(env.activate):
            fabric.api.run(cmd)


def refresh_css():
    with cd('_build/html'):
        cwd = path('.')
        css_files = list(cwd.walk('*.css'))
        for css_file in css_files:
            name = css_file.basename()
            mtime = css_file.mtime
            local("find . -name \*.html -type f -print | xargs sed -i s@_static/%s@_static/%s?m=%s@g" % (name, name, mtime) )


def deploy():
    local('hg push ' + master_repo)
    run('hg pull -u ' + master_repo)
    run('make html')
    run('fab refresh_css')


