#!/bin/bash

rm -rf dist/

rm -rf build/
BUILD_MAC=1 python3 setup.py bdist_wheel

rm -rf build/
BUILD_MAC_M1=1 python3 setup.py bdist_wheel

rm -rf build/
BUILD_LINUX=1 python3 setup.py bdist_wheel

rm -rf build/
BUILD_LINUX_ARM=1 python3 setup.py bdist_wheel

rm -rf build/
BUILD_LINUX_PPC64LE=1 python3 setup.py bdist_wheel

rm -rf build/
BUILD_LINUX_S390X=1 python3 setup.py bdist_wheel

rm -rf build/
BUILD_WIN=1 python3 setup.py bdist_wheel

twine check dist/*.whl
