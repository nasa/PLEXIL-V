#!/usr/bin/env bash

MAUDE=maude

msgAndExit () {
    echo "$*"
    exit 1
}

if [ -z "$1" ]; then
  echo "Usage: $0 <plan.ple>"
  exit 1
fi

if ! [ -f "$1" ]; then
    echo "File '$1' does not exist"
    exit 1
fi

filename="$1"
expected_extension=".ple" # Change to your desired extension
actual_extension="${filename##*.}"

if ! [[ ".$actual_extension" == "$expected_extension" ]]; then
    echo "File '$filename' does NOT have the $expected_extension extension."
fi

i="${filename%%.*}"

# Check for SKIP flag
if [ -f SKIP ]; then
    echo "Plan: $i - SKIPPED"
    exit 0
fi

echo "Plan: $i"

plxPlan=`echo $plePlan | sed 's/\(.*\)\.ple/\1.plx/'`
maudePlan=`echo $plePlan | sed 's/\(.*\)\.ple/\1.maude/'`

# plx2maude="cabal run --project-dir=../../../../../plexil2maude/ plx2maude"
plx2maude="plx2maude"
psx2maude="psx2maude"

test -f $i.ple || msgAndExit "File $i.ple not found"
test -f $i.pst || msgAndExit "File $i.pst not found"
rm -f $i.psx
for p in $(ls *.ple); do
    plx=${p%.*}.plx
    rm -f $plx
    plexilc $p
done
xmllint --format --output $i.plx $i.plx
plexilc $i.pst
xmllint --format --output $i.psx $i.psx
test -f $i.plx || msgAndExit "Error producing file $i.plx"
test -f $i.psx || msgAndExit "Error producing file $i.psx"
rm -f input.maude
if ! [ -f NO_PLX2MAUDE ]; then
    rm -f $i.maude
    plx2maude $i.plx > $i.maude
else
    echo "Warning: $i.maude has been crafted manually"
fi
$psx2maude $i.psx > input.maude
test -f $i.maude    || msgAndExit "Error producing file $i.maude"
test -f input.maude || msgAndExit "Error producing file input.maude"
echo -n "Input [$i]: "

# create run.maude
rm -f run.maude
rm -f output.maude
rm -f output.plexil
printf "load ../../../../src/plexil-v.maude\nload $i.maude\nload input.maude\nset print attribute on .\nset print color on .\nmod PLAN-SIMULATION is\n    protecting $i-PLAN .\n    protecting INPUT .\nendm\nrew run(compile(rootNode,input)) .\nq" >> run.maude

plexiltest -p $i.plx -s $i.psx -d ../../Debug.AcceptanceTest.cfg > output.plexil 2>&1
plexilog < output.plexil > output.plexil.trace
$MAUDE -no-ansi-color -no-wrap -no-banner -no-advise -print-to-stderr run.maude > /dev/null 2> output.maude
plexilog-maude < output.maude > output.maude.trace
plexilog-diff output.plexil output.maude
