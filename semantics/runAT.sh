#!/bin/bash

CHECK=NO

while [[ $# -gt 0 ]]; do
  case $1 in
    -c|--check)
      CHECK=YES
      shift
      ;;
    *)
      break
      ;;
  esac
done

TIMEOUT=${1:-timeout}
MD5=${2:-md5sum}
MAUDE=${3:-maude}

function run {
  pushd test/acceptance > /dev/null
  clear
  $TIMEOUT -v -k 0 80 ./runICAROUS0.sh
  $TIMEOUT -v -k 0 80 ./runICAROUS1.sh
  ./runAcceptance.sh $TIMEOUT $MD5 $MAUDE
  popd > /dev/null
}

function check {
  count=$(grep -o "EQ" $1 | wc -l)
  skipped=$(find ./test/acceptance/tests/ -name "SKIP" | wc -l)
  expected=$((17 + $(ls ./test/acceptance/tests/ | wc -l) - $skipped))
  if [ "$count" -eq "$expected" ]; then
    exit 0
  else
    exit 1
  fi
}

if [ "$CHECK" == "YES" ]; then
  TEMP_FILE=$(mktemp)
  run | tee $TEMP_FILE
  check $TEMP_FILE
else
  run
  while true; do
    sum1=$($MD5 `find src -name "*.maude" -not -name ".*"`)
    sleep 2
    sum2=$($MD5 `find src -name "*.maude" -not -name ".*"`)
    if [ "$sum1" != "$sum2" ]; then
      run
    fi
  done
fi
