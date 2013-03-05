#!/usr/bin/env python
import requests


repos = [
    'amo-validator',
    'app-validator',
    'bedrock',
    'django-browserid',
    'elasticutils',
    'elmo',
    'firefox-flicks',
    'fireplace',
    'fjord',
    'funfactory',
    'high-fidelity',  # Mozilla's Podcasts Reference App
    'input.mozilla.org',
    'kitsune',
    'kuma',
    'mozillians',
    'nocturnal',
    'playdoh',
    'playdoh-docs',
    'remo',
    'socorro',
    'solitude',
    'webdev-bootcamp',
    'zamboni',
    'airmozilla',
    'socorro',
    'socorro-crashstats',
    'unicode-slugify',
    'webdev-contributors',
]
GITHUB_API_HOST = 'https://api.github.com'
GITHUB_API_CLIENT_ID = ''
GITHUB_API_CLIENT_SECRET = ''
base_url = '%s/repos/mozilla' % GITHUB_API_HOST
params = {'client_id': GITHUB_API_CLIENT_ID,
          'client_secret': GITHUB_API_CLIENT_SECRET}
commit_levels = [100, 50, 25, 10, 1]
contributors = {}
contributors_by_level = {}


# Figure out the number of contributions per contributor:
for repo in repos:
    url = '%s/%s/contributors' % (base_url, repo)
    for repocontributor in requests.get(url, params=params).json():
        username = repocontributor['login']
        contributions = repocontributor['contributions']
        contributor = contributors.setdefault(username, {})
        contributor['contributions'] = (
            contributor.get('contributions', 0) + contributions)
        contributor.setdefault('repos', []).append(repo)

# Get all available email addresses of contributors:
for user, contributor in contributors.items():
    user_url = '%s/users/%s' % (API_GITHUB_HOST, user)
    user_obj = requests.get(user_url, params=params).json()
    contributor['email'] = user_obj.get('email', '')


# Group the contributors into levels by number of contributions:
for user, contributor in contributors.items():
    contributions = contributor['contributions']
    for level in commit_levels:
        if contributions >= level:
            contributors_by_level.setdefault(level, []).append((user,
                                                                contributor))
            break


def print_contributors():
    """Output contributors and their number of contributions."""
    for user, contributor in contributors.items():
        print '%s, %s, %s, %s' % (
            user, contributor['contributions'], contributor['email'],
            ' '.join(contributor['repos']))


def print_contributors_by_level():
    """Output contributors, based on their contribution levels."""
    for level in commit_levels:
        print '========== %s+ ==========' % level
        for user, contributor in contributors_by_level[level]:
            print contributor['email']


print_contributors_by_level()
