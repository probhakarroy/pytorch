#!/usr/bin/env bash
set -ex -o pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Check if we should actually run
echo "BUILD_ENVIRONMENT: ${BUILD_ENVIRONMENT:-}"
echo "CIRCLE_PULL_REQUEST: ${CIRCLE_PULL_REQUEST:-}"
if [ -z "${BUILD_ENVIRONMENT:-}" ]; then
  echo "Cannot run should_run_job.sh if BUILD_ENVIRONMENT is not defined!"
  echo "CircleCI scripts are probably misconfigured."
  exit 1
fi
#if ! [ -d ".git" ]; then
#  echo "Cannot run should_run_job.sh if you don't have a Git checkout!"
#  echo "CircleCI scripts are probably misconfigured."
#  exit 1
#fi
if [ -n "${CIRCLE_PULL_REQUEST:-}" ]; then
  # Don't swallow "script doesn't exist
  [ -e "$SCRIPT_DIR/should_run_job.py"  ]
  if ! python "$SCRIPT_DIR/should_run_job.py" "${BUILD_ENVIRONMENT:-}"; then
    circleci step halt
    exit
  fi
fi