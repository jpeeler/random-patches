#!/usr/bin/env python

import re
import os

from git import Repo


repo = Repo('.git')

head_commit = repo.head.commit
committed_files = head_commit.stats.files.keys()
committed_files.reverse()

remote = re.search('Remote: (.*)', head_commit.message).group(1)
reponame = remote.rpartition('/')[2].split('.git')[0]

try:
    os.chdir(reponame)
    remote_repo = Repo('.git')
    remote_repo.remotes.origin.pull()
except OSError:
    remote_repo = Repo.clone_from(remote, reponame, branch='master')

for file in committed_files:
    remote_repo.git.execute(['git', 'am', '../' + file])
