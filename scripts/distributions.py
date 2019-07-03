#!/usr/bin/python3

from collections import defaultdict
from os import mkdir
from os.path import join
from re import search
from shutil import rmtree


distfiles = defaultdict(str)
distributions = (
    {'name': 'unstable',
     'origin': 'debian',
     'type': 'development',
     'experimental': False,
     'architectures': ('amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips',
                       'mips64el', 'mipsel', 'powerpc', 'ppc64el', 's390x'),
     'ports': ()},

    {'name': 'experimental',
     'origin': 'debian',
     'type': 'development',
     'experimental': True,
     'architectures': ('amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips',
                       'mips64el', 'mipsel', 'powerpc', 'ppc64el', 's390x'),
     'ports': ()},

    {'name': 'testing',
     'origin': 'debian',
     'type': 'development',
     'experimental': False,
     'architectures': ('amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips',
                       'mips64el', 'mipsel', 'ppc64el', 's390x'),
     'ports': ()},

    {'name': 'stable',
     'origin': 'debian',
     'type': 'supported',
     'experimental': False,
     'architectures': ('amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips',
                       'mips64el', 'mipsel', 'ppc64el', 's390x'),
     'ports': ()},

    {'name': 'oldstable',
     'origin': 'debian',
     'type': 'supported',
     'experimental': False,
     'architectures': ('amd64', 'armel', 'armhf', 'i386'),
     'ports': ()},

    {'name': 'buster-backports',
     'origin': 'debian',
     'type': 'backports',
     'experimental': False,
     'architectures': ('amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips',
                       'mips64el', 'mipsel', 'ppc64el', 's390x'),
     'ports': ()},

    {'name': 'stretch-backports',
     'origin': 'debian',
     'type': 'backports',
     'experimental': False,
     'architectures': ('amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips',
                       'mips64el', 'mipsel', 'ppc64el', 's390x'),
     'ports': ()},

    {'name': 'jessie-backports',
     'origin': 'debian',
     'type': 'backports',
     'experimental': False,
     'architectures': ('amd64', 'armel', 'armhf', 'i386'),
     'ports': ()},

    {'name': 'eoan',
     'origin': 'ubuntu',
     'type': 'development',
     'experimental': False,
     'architectures': ('amd64', 'i386'),
     'ports': ('arm64', 'armhf', 'ppc64el', 's390x'),
     'extrapackages': 'pkgbinarymangler'},

    {'name': 'disco',
     'origin': 'ubuntu',
     'type': 'supported',
     'experimental': False,
     'architectures': ('amd64', 'i386'),
     'ports': ('arm64', 'armhf', 'ppc64el', 's390x'),
     'extrapackages': 'pkgbinarymangler'},

    {'name': 'bionic',
     'origin': 'ubuntu',
     'type': 'supported',
     'experimental': False,
     'architectures': ('amd64', 'i386'),
     'ports': ('arm64', 'armhf', 'ppc64el', 's390x'),
     'extrapackages': 'pkgbinarymangler'},

    {'name': 'xenial',
     'origin': 'ubuntu',
     'type': 'supported',
     'experimental': False,
     'architectures': ('amd64', 'i386'),
     'ports': ('arm64', 'armhf', 'powerpc', 'ppc64el', 's390x'),
     'extrapackages': 'pkgbinarymangler pkg-create-dbgsym'},

    {'name': 'trusty',
     'origin': 'ubuntu',
     'type': 'supported',
     'experimental': False,
     'architectures': ('amd64', 'i386'),
     'ports': ('arm64', 'armhf', 'powerpc', 'ppc64el', 's390x'),
     'extrapackages': 'pkgbinarymangler pkg-create-dbgsym'},
)

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
                extramirrors = ('deb http://deb.debian.org/debian-security ' +
                                '{0}/updates {1}\n'.format(suite, components) +
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
rmtree('../distributions')
mkdir('../distributions')
for arch in distfiles:
    with open(join('../distributions', arch), 'w') as fd:
        fd.write(distfiles[arch])
