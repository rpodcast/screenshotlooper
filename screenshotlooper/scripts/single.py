import argh

from argh.decorators import arg
from screenshotlooper.cli import cmd

def main():

    p = argh.ArghParser()
    argh.set_default_command(p, cmd)
    p.dispatch()

if __name__ == '__main__':
    main()