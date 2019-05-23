import argparse
import subprocess
import re
import sys

# Modify this variable if you want to change the set of default jobs
# which are run on all pull requests.

default_set = [
    # PyTorch CPU
    # Selected oldest Python 2 version to ensure Python 2 coverage
    'pytorch-linux-trusty-py2.7.9',
    # PyTorch CUDA
    'pytorch-linux-xenial-cuda9-cudnn7-py3',
    # PyTorch ASAN
    'pytorch-linux-xenial-py3-clang5-asan',
    # PyTorch DEBUG
    'pytorch-linux-trusty-py3.6-gcc5.4',

    # Caffe2 CPU
    'caffe2-py2-mkl-ubuntu16.04',
    # Caffe2 CUDA
    'caffe2-py2-cuda9.1-cudnn7-ubuntu16.04',
    # Caffe2 ONNX
    'caffe2-onnx-py2-gcc5-ubuntu16.04',
    # Caffe2 Clang
    'caffe2-py2-clang7-ubuntu16.04',
    # Caffe2 CMake
    'caffe2-cmake-cuda9.0-cudnn7-ubuntu16.04',

    # Binaries
    'manywheel 2.7mu cpu devtoolset3',

    # Caffe2 Android
    'caffe2-py2-android-ubuntu16.04',
    # Caffe2 OSX
    'caffe2-py2-system-macos10.13',
    # PyTorch OSX
    'pytorch-macos-10.13-cuda9.2-cudnn7-py3',
    # PyTorch Android
    'pytorch-linux-xenial-py3-clang5-android-ndk-r19c',

    # Other checks
    'pytorch-short-perf-test-gpu',
    'pytorch-doc-push',
]

# Assumes it's run in a valid Git checkout
#
# This script will query Git and attempt to determine if we should
# run the current CI job under question
#
# NB: Try to avoid hard-coding names here, so there's less place to update when jobs
# are updated/renamed
#
# Semantics in the presence of multiple tags:
#   - Let D be the set of default builds
#   - Let S be the set of explicitly specified builds
#   - Run S \/ D

parser = argparse.ArgumentParser()
parser.add_argument('build_environment')
args = parser.parse_args()

commit_msg = subprocess.check_output(("git", "log", "--format=%B", "-n", "1", "HEAD"), universal_newlines=True)

# Matches anything that looks like [foo ci] or [ci foo] or [foo test]
# or [test foo]
RE_MARKER = re.compile(r'\[(?:([^ \[\]]+) )?(?:ci|test)(?: ([^ \[\]]+))?\]')

markers = RE_MARKER.finditer(commit_msg)

for m in markers:
    if m.group(1) and m.group(2):
        print("Unrecognized marker: {}".format(m.group(0)))
        continue
    spec = m.group(1) or m.group(2)
    if spec in args.build_environment or spec == 'all':
        print("Accepting {} due to commit marker {}".format(args.build_environment, m.group(0)))
        sys.exit(0)

for spec in default_set:
    if spec in args.build_environment:
        print("Accepting {} as part of default set".format(args.build_environment))
        sys.exit(0)

print("Rejecting {}".format(args.build_environment))
sys.exit(1)