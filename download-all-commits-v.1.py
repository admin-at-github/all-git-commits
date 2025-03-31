#!/usr/bin/python

# python3 ./all-git-commits.py -u <user> -d <directory> -r <repo> -n <number of commits>
#
# Tool to inspect Github and pull local copies of all commits for
# for the given user.
#
# Why?  Every ask yourself the question 'I know I did this before, but
#       which repos commit was it in?'
# With all files local, you can use any serach-in-files app to look.
#
# Companion App: all-gethub.py to get all repos for a user.

import getopt
import json
import os
import sys
import requests
from urllib.request import urlopen

def Usage():
    print("Usage: %s -u <github user> -d <directory> -r <repo> -n <number of commits>" % sys.argv[0])
    print("  -u <github user>  github user name")
    print("  -d <directory>    local directory for repos commits")
    print("  -r <repo>         specific repo")
    print("  -n <number>       (optional) number of commits (newest to oldest)")

def main():

    githubUser  = ''
    destDirectory = ''
    currentRepo = ''
    numberCommits = 10000000
    try:
        # process command arguments
        ouropts, args = getopt.getopt(sys.argv[1:],"u:d:r:n:h")
        for o, a in ouropts:
            if   o == '-u':
                githubUser = a
            elif o == '-d':
                destDirectory = a
            elif o == '-r':
                currentRepo = a
            elif o == '-n':
                numberCommits = int(a)
            elif o == '-h':
                Usage()
                sys.exit(0)
    except getopt.GetoptError as e:
        print(str(e))
        Usage()
        sys.exit(2)

    if type(githubUser) != str or len(githubUser) <= 0:
        print("please use -u for github user")
        Usage()
        sys.exit(0)
    if type(destDirectory) != str or len(destDirectory) <= 0:
        print("please use -d for local directory")
        Usage()
        sys.exit(0)
    if type(currentRepo) != str or len(currentRepo) <= 0:
        print("please use -r for repo")
        Usage()
        sys.exit(0)

    commitsLink = "https://api.github.com/repos/{0}/{1}/commits".format(githubUser, currentRepo)
    f = urlopen(commitsLink)
    commits = json.loads(f.readline())
    print("repo: '{0}' ; total commits: {1}".format(currentRepo, len(commits)))

    os.makedirs(os.path.join(destDirectory, githubUser, currentRepo, 'commits'), exist_ok=True)

    count = 0
    for commit in commits:
        sha = commit['sha']
        zip_name = "{0}-{1}.zip".format(currentRepo, sha)
        zip_path = os.path.join(destDirectory, githubUser, currentRepo, 'commits', zip_name)
        zip_url = "https://github.com/{0}/{1}/archive/{2}.zip".format(githubUser, currentRepo, sha)
        print("Downloading", zip_name)
        
        response = requests.get(zip_url)
        with open(zip_path, 'wb') as f:
            f.write(response.content)

        # are we done?
        count += 1
        if (count >= numberCommits):
            break

if __name__ == "__main__":
    main()