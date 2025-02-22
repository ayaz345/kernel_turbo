"""
 exynos_checkpatch_helper.py - a helper script for exynos_checkpatch.sh

 Dept    : S/W Solution Dev Team
 Author  : Solution3 Power Part
 Update  : 2014.12.08
"""

import subprocess as sp
import sys

def print_log(color, log):
    colored_log = ''
    if color == 'r':
        colored_log = "\033[31m" + log + "\033[0m"
    else:
        colored_log = "\033[32m" + log + "\033[0m"
    print colored_log


def decide(result):
    num_error, num_warning = int(result[1]), int(result[3])
    return 'SUCCESS' if num_error == 0 and num_warning == 0 else 'FAIL'


def print_build_result():
    defconfig, build_log, result = sys.argv[2], sys.argv[3], int(sys.argv[4])
    if build_log == '0xefefefef':
        print_log('r', f'[ BUILD ] {defconfig} <- NOT EXIST')
        return
    if result == 1:
        print_log('g', f'[ BUILD ] {defconfig} <- SUCCESS')
    else:
        print_log('r', f'[ BUILD ] {defconfig} <- FAIL (refer to {build_log})')


def print_defconfig_result():
    defconfig, def_log, result = sys.argv[2], sys.argv[3], int(sys.argv[4])
    if def_log == '0xfefefefe':
        print_log('r', f'[ DEFCONFIG ] {defconfig} <- NOT EXIST')
        return
    if result == 1:
        print_log('g', f'[ DEFCONFIG ] {defconfig} <- SUCCESS')
    else:
        print_log('r', f'[ DEFCONFIG ] {defconfig} <- FAIL (refer to {def_log})')


def run_checkpatch_test():
    num_patch = 5 if sys.argv[2] == '' else int(sys.argv[2])
    patches = sp.check_output(['git', 'format-patch', f'-{num_patch}']).split()
    for patch in patches:
        try:
            r = sp.check_output(['./scripts/checkpatch.pl', patch]).strip().split()
        except sp.CalledProcessError:
            print_log('r', f'[ CHECKPATCH ] {patch} <- FAIL')
            continue
        color = 'g' if decide(r) == 'SUCCESS' else 'r'
        print_log(color, f'[ CHECKPATCH ] {patch} <- {decide(r)}')
        sp.check_output(['rm', patch])


def main():
    if sys.argv[1] == '-b':
        print_build_result()
    elif sys.argv[1] == '-c':
        run_checkpatch_test()
    elif sys.argv[1] == '-d':
        print_defconfig_result()
    else:
        assert False


main()
