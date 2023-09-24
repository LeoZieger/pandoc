import os
import subprocess
import shutil
import os
from pathlib import Path

TIX_DIRECTORY = Path("./tixfiles/")
GEN_TIX_LOCATION_1 = Path("./test-pandoc.tix")
GEN_TIX_LOCATION_2 = Path("./test/test-pandoc.tix")
GEN_TIX_LOCATION_COMB = Path("./combined-test-pandoc.tix")


SEPERATOR = "."
SUCCESS = "PASSED"
FAILED = "FAILED"


def escapeTestName(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\\"')
    return s


def main():
    print('[INFO] Deleting every tix-file')
    os.system(f'find {TIX_DIRECTORY} -name "*.tix" -type f -delete')

    print('[INFO] Collecting all available tests')
    out = subprocess.check_output(['cabal', 'run', 'test-pandoc', '--', '-l'])

    tests_text = out.decode('UTF-8')
    tests = tests_text.split('\n')

    tests = [x for x in tests if x != ""]

    for i, test in enumerate(tests):
        print(f"[INFO] Test {i+1} / {len(tests)} [{test}]")

        proc = subprocess.run(['cabal',
                               'run',
                               'test-pandoc',
                               '--',
                               '-p',
                               f'$0 == \"{escapeTestName(test)}\"'])

        test_result = proc.returncode

        if test_result == 0:
            suffix = SUCCESS
        else:
            suffix = FAILED
            print(f"[ERROR] Test {test} failed")

        filename = test.replace(" ", "")
        filename = filename.replace("/", "")

        index = 2
        if os.path.exists(TIX_DIRECTORY / f"{filename}{SEPERATOR}{suffix}.tix"):
            while os.path.exists(TIX_DIRECTORY / (f"{filename}_{str(index)}{SEPERATOR}{suffix}.tix")):
                index += 1
            filename = f"{filename}_{str(index)}"

        filename = f"{filename}{SEPERATOR}{suffix}.tix"

        if os.path.exists(GEN_TIX_LOCATION_1) and not os.path.exists(GEN_TIX_LOCATION_2):
            shutil.move(GEN_TIX_LOCATION_1, TIX_DIRECTORY / filename)
        elif not os.path.exists(GEN_TIX_LOCATION_1) and os.path.exists(GEN_TIX_LOCATION_2):
            shutil.move(GEN_TIX_LOCATION_2, TIX_DIRECTORY / filename)
        elif os.path.exists(GEN_TIX_LOCATION_1) and os.path.exists(GEN_TIX_LOCATION_2):
            print("combining")
            proc = subprocess.run(['hpc',
                                'combine',
                                f'{GEN_TIX_LOCATION_1}',
                                f'{GEN_TIX_LOCATION_2}',
                                f'--output',
                                f'{GEN_TIX_LOCATION_COMB}'])

            shutil.move(GEN_TIX_LOCATION_COMB, TIX_DIRECTORY / filename)
            os.remove(GEN_TIX_LOCATION_1)
            os.remove(GEN_TIX_LOCATION_2)
        else:
            pass


if __name__ == "__main__":
    main()
