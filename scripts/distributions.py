#!/usr/bin/python3

from collections import defaultdict
from configparser import ConfigParser
from glob import glob
from json import load
from os import mkdir
from os.path import join
from re import search
from shutil import rmtree


mapper = {}
distfiles = defaultdict(str)
with open('distributions.json') as json_file:
    distributions = load(json_file)
for dist in distributions:
    for arch in (dist['architectures'] + dist['ports']):
        name = dist['name']
        if dist['origin'] == 'debian':
            if not search('# Debian', distfiles[arch]):
                distfiles[arch] += '# Debian\n\n'
            if dist['experimental']:
                suite = 'unstable'
            elif dist['type'] == 'backports':
                suite = name.split('-')[0]
            else:
                suite = name
            url = 'http://deb.debian.org/debian'
            components = 'main contrib non-free'
            if dist['type'] in ('supported', 'backports'):
                if dist['oldsecurity']:
                    security = '{0}/updates'.format(suite)
                else:
                    security = '{0}-security'.format(suite)
                extramirrors = ('deb http://deb.debian.org/debian-security ' +
                                '{0} {1}\n'.format(security, components) +
                                '              ' +
                                'deb http://deb.debian.org/debian ' +
                                '{0}-updates {1}'.format(suite, components))
                if dist['type'] == 'backports':
                    extramirrors += ('\n              deb {0} {1} {2}'
                                     .format(url, name, components))
            elif dist['type'] == 'development' and dist['experimental']:
                extramirrors = ('deb {0} {1} {2}\n'
                                .format(url, name, components))
            else:
                extramirrors = ''
        elif dist['origin'] == 'ubuntu':
            if not search('# Ubuntu', distfiles[arch]):
                distfiles[arch] += '\n\n\n# Ubuntu\n\n'
            if dist['type'] == 'backports':
                suite = name.split('-')[0]
            else:
                suite = name
            if arch in dist['ports']:
                url = 'http://ports.ubuntu.com'
            else:
                url = 'http://archive.ubuntu.com/ubuntu'
            components = 'main restricted universe multiverse'
            if dist['type'] in ('supported', 'backports'):
                extramirrors = ('deb {0} {1}-updates {2}\n'
                                .format(url, suite, components) +
                                '              ' +
                                'deb {0} {1}-security {2}'
                                .format(url, suite, components))
            else:
                extramirrors = ''
        distfiles[arch] += ('[{}]\n'.format(name) +
                            'suite: {}\n'.format(suite) +
                            'mirror: {}\n'.format(url) +
                            'components: {}\n'.format(components))
        if dist['type'] == 'development':
            if extramirrors:
                extramirrors += ('              ' +
                                 'deb http://debomatic-{0}.debian.net/'
                                 .format(arch) +
                                 'debomatic/{0} {0} main'.format(name))
            else:
                extramirrors += ('deb http://debomatic-{0}.debian.net/'
                                 .format(arch) +
                                 'debomatic/{0} {0} main'.format(name))
        if extramirrors:
            distfiles[arch] += 'extramirrors: {}\n'.format(extramirrors)
        if 'extrapackages' in dist and dist['extrapackages']:
            distfiles[arch] += ('extrapackages: {}\n'
                                .format(dist['extrapackages']))
        distfiles[arch] += '\n'
    if dist['origin'] == 'debian':
        if 'codename' in dist:
            if dist['name'] in ('unstable', 'experimental'):
                suffixes = ('',)
            elif '-backports' in dist['name']:
                suffixes = ('', '-sloppy')
            else:
                suffixes = ('', '-updates', '-proposed-updates', '-security')
            for suffix in suffixes:
                mapper[f'''{dist['codename']}{suffix}'''] = dist['name']
for arch in glob('../architectures/*'):
    cp = ConfigParser(delimiters=':')
    cp.read(arch)
    cp['distributions']['mapper'] = str(mapper).replace(', ', ',\n  ')
    with open(arch, 'w') as fd:
        cp.write(fd)
rmtree('../distributions')
mkdir('../distributions')
for arch in distfiles:
    with open(join('../distributions', arch), 'w') as fd:
        fd.write(distfiles[arch])
