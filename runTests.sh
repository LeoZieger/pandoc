#!/bin/bash

echo "Deleting every .tix file ..."
find . -name "*.tix" -type f -delete
echo "Running tests ..."

tests=(
        "figures-html.md"
        "html-writer-a-in-a.md"
        "html-trim-definition-list-terms.md"
        "html-read-figure.md"
        "html.writer.basic"
        "html.writer.tables"
        "html.writer.planets"
        "html.writer.nordics"
        "html.writer.students"
        "html.writer.lhs"
        "html.reader"
        "html4"
    )

for test in ${tests[@]}
do
   echo "Running" $test
   ./dist-newstyle/build/x86_64-linux/ghc-9.4.4/pandoc-3.1.3/t/test-pandoc/build/test-pandoc/test-pandoc -p $test
   if [[ $? -gt 0 ]]
   then
    mv ./test/test-pandoc.tix tixfiles/${test}_FAIL.tix
   else
    mv ./test/test-pandoc.tix tixfiles/${test}_PASS.tix
   fi
done
