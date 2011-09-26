import fabric
from fabric.api import env, local, sudo, cd, prefix

import sys
import fileinput
import re
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
            name = css_file.namebase
            mtime = int(css_file.mtime)
            pattern = "%s\.[0-9]*\.?css" % name
            repl = "%s.%s.css" % (name, mtime)

            # Walk through all html files and rewrite references to index.css or index.12345.css as index.76533.css where 76533 is the modification time of index.css
            html_files = list(cwd.walk('*.html'))
            for html_file in html_files:
                for line in fileinput.input(html_file, inplace=1):
                    line = re.sub(pattern, repl, line)
                    sys.stdout.write(line)


def deploy():
    local('hg push ' + master_repo)
    run('hg pull -u ' + master_repo)
    run('make html')
    run('fab refresh_css')


