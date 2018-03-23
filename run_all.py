"""Usage: run_all.py [-h | --help] [-ab] (--sys1 | --sys2 | --sys3)

Example, try:
  run_all.py -a -b --sys1

Options:
  -h --help
  -a        analyse
  -b        build
  --sys1    apply to system one
  --sys2    apply to system two
  --sys3    apply yo system three
"""
from docopt import docopt


def main(analysis=False, build=False, sys1=False, sys2=False, sys3=False):
    if sys1:
        if analysis:
            print('analysing system 1')
        if build:
            print('building system 1')

if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(analysis=arguments['-a'], build=arguments['-b'],
         sys1=arguments['--sys1'], sys2=arguments['--sys2'], sys3=arguments['--sys3'])