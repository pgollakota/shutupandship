import fabric
from fabric.api import env, local, sudo, cd, prefix

env.hosts = ['praveen@173.255.241.59']
env.sphinx_root = '/home/praveen/cows/shutupandship'
env.activate = 'source /home/praveen/.virtualenvs/shush/bin/activate'
master_repo = 'ssh://hg@bitbucket.org/pgollakota/shutupandship'


def run(cmd):
    with cd(env.sphinx_root):
        with prefix(env.activate):
            fabric.api.run(cmd)


def deploy():
    local('hg push ' + master_repo)
    run('hg pull -u ' + master_repo)
    run('make html')


