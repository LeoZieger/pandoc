import os
import subprocess
import shutil
import os
from pathlib import Path

TIX_DIRECTORY = Path("./tixfiles/")
GEN_TIX_LOCATION = Path("./test-pandoc.tix")


def escapeTestName(s):
    return s.replace('\\#', '\\\\#')


def main():
    print('[INFO] Deleting every tix-file')
    os.system('find . -name "*.tix" -type f -delete')

    print('[INFO] Collecting all available tests')
    proc = subprocess.run(['./dist-newstyle/build/x86_64-linux/ghc-9.4.4/pandoc-3.1.3/t/test-pandoc/build/test-pandoc/test-pandoc',
                        '-l'],
                        stdout=subprocess.PIPE)

    tests_text = proc.stdout.decode('UTF-8')
    tests = tests_text.split('\n')

    tests = [x for x in tests if x != ""]

    for i, test in enumerate(tests):
        print(f"[INFO] Test {i+1} / {len(tests)} [{test}]")

        proc = subprocess.run(['./dist-newstyle/build/x86_64-linux/ghc-9.4.4/pandoc-3.1.3/t/test-pandoc/build/test-pandoc/test-pandoc',
                            '-p',
                            f'$0 == \"{escapeTestName(test)}\"'])

        test_result = proc.returncode

        if test_result == 0:
            suffix = "PASS"
        else:
            suffix = "FAIL"
            print(f"[ERROR] Test {test} failed")

        filename = test.replace(" ", "")
        filename = filename.replace("/", "")

        index = 2
        if os.path.exists(TIX_DIRECTORY / f"{filename}_{suffix}.tix"):
            while os.path.exists(TIX_DIRECTORY / (f"{filename}_{str(index)}_{suffix}.tix")):
                index += 1
            filename = f"{filename}_{str(index)}"

        filename = f"{filename}_{suffix}.tix"

        shutil.move(GEN_TIX_LOCATION, TIX_DIRECTORY / filename)

if __name__ == "__main__":
    main()