#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from wheel.bdist_wheel import bdist_wheel


version = '3.5.1'
repo_base = os.path.dirname(__file__)


def platform_ext():
    if os.environ.get('BUILD_MAC', None) is not None:
        return 'darwin-amd64'
    if os.environ.get('BUILD_MAC_M1', None) is not None:
        return 'darwin-arm64'
    if os.environ.get('BUILD_LINUX', None) is not None:
        return 'linux-amd64'
    if os.environ.get('BUILD_LINUX_ARM', None) is not None:
        return 'linux-arm64'
    if os.environ.get('BUILD_LINUX_PPC64LE', None) is not None:
        return 'linux-ppc64le'
    if os.environ.get('BUILD_LINUX_S390X', None) is not None:
        return 'linux-s390x'
    if os.environ.get('BUILD_WIN', None) is not None:
        return 'windows-amd64'
    raise RuntimeError('Set the BUILD_* environment before packaging')


def platform_name():
    if os.environ.get('BUILD_MAC', None) is not None:
        return 'macosx_10_9_x86_64'
    if os.environ.get('BUILD_MAC_M1', None) is not None:
        return 'macosx_10_15_arm64'
    if os.environ.get('BUILD_LINUX', None) is not None:
        return 'manylinux1_x86_64'
    if os.environ.get('BUILD_LINUX_ARM', None) is not None:
        return 'manylinux2014_aarch64'
    if os.environ.get('BUILD_LINUX_PPC64LE', None) is not None:
        return 'manylinux2014_ppc64le'
    if os.environ.get('BUILD_LINUX_S390X', None) is not None:
        return 'manylinux2014_s390x'
    if os.environ.get('BUILD_WIN', None) is not None:
        return 'win_amd64'
    raise RuntimeError('Set the BUILD_* environment before packaging')


class bdist_wheel_injected(bdist_wheel):
    def finalize_options(self):
        self.plat_name = platform_name()
        super(bdist_wheel_injected, self).finalize_options()
        self.root_is_pure = True


class build_py_with_extra_data(build_py):
    def _get_data_files(self):
        """Add custom out-of-tree package data files."""
        rs = super()._get_data_files()

        platform = platform_ext()
        folder = 'etcd-v%s-%s' % (version, platform)

        package = 'etcd_distro.etcdbin'
        src_dir = os.path.join(repo_base, 'etcd', 'v%s' % version, folder)
        build_dir = os.path.join(*([self.build_lib] + package.split('.')))
        if 'windows' in platform:
            filenames = ['etcd.exe', 'etcdctl.exe', 'etcdutl.exe']
        else:
            filenames = ['etcd', 'etcdctl', 'etcdutl']
        rs.append((package, src_dir, build_dir, filenames))

        return rs


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8', mode='r') as fp:
    long_description = fp.read()


setup(
    name='etcd-distro',
    version=version,
    description='Python distribution for etcd, a key-value store, to make the installation easier on various platforms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='The etcd Authors',
    author_email='sighingnow@gmail.com',
    url='https://github.com/sighingnow/etcd-distro',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Compilers",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: Apache Software License",
    ],
    platforms='any',
    keywords='etcd Python distribution',

    cmdclass={
        'build_py': build_py_with_extra_data,
        'bdist_wheel': bdist_wheel_injected,
    },
    zip_safe=False,

    package_dir={'': 'src'},
    packages=find_packages('src'),

    entry_points={
        'console_scripts': [
            'etcd=etcd_distro:etcd',
            'etcdctl=etcd_distro:etcdctl',
            'etcdutl=etcd_distro:etcddutl',
        ]
    },

    project_urls={
        'Source': 'https://github.com/sighingnow/etcd-distro',
        'Tracker': 'https://github.com/sighingnow/etcd-distro/issues',
    },
)
