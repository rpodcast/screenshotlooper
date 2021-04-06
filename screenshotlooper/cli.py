"""Console script for screenshotlooper."""
import argh
from argh.decorators import arg

@arg('-m', '--myarg', help='Test arg.', default=True)
@arg('--output_dir', help='Directory to store screenshot files. If not specified, the current working directory where the tool is being executed will be used.')
def cmd(**kwargs):
    print('my arg: ', kwargs['myarg'])

# import argparse
# import sys

# from screenshotlooper import say_hello

# def main():
#     """Console script for screenshotlooper."""
#     parser = argparse.ArgumentParser()
#     #parser.add_argument('_', nargs='*')
#     parser.add_argument('-n', '--name', action='store', help='Provides name')
#     args = parser.parse_args()

#     say_hello(args.name)

#     # print("Arguments: " + str(args._))
#     # print("Replace this message by putting your code into "
#     #       "screenshotlooper.cli.main")
#     # return 0


# if __name__ == "__main__":
#     sys.exit(main())  # pragma: no cover
