#!/usr/bin/env python3

import click

@click.command()
@click.argument('init')
def init(init):
    click.echo(init)

if __name__ == '__main__':
    hello()
