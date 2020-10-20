from datetime import datetime

import click

from instawow.models import Pkg, PkgOptions
import instawow.plugins
from instawow.resolvers import Defn, Resolver, Strategy


@click.command()
def foo():
    "don't foo where you bar"
    print('success!')


class FooResolver(Resolver):
    source = 'foo'
    name = 'Foo Inc.'
    strategies = frozenset({Strategy.default})

    async def resolve_one(self, defn: Defn, metadata: None) -> Pkg:
        return Pkg(
            source=self.source,
            id='1',
            slug=defn.alias,
            name='Bar',
            description='The quintessential bar add-on, brought to you by Foo',
            url='http://example.com/',
            download_url='...',
            date_published=datetime.now(),
            version='0',
            options=PkgOptions(strategy=defn.strategy.name),
        )


@instawow.plugins.hookimpl
def instawow_add_commands():
    return (foo,)


@instawow.plugins.hookimpl
def instawow_add_resolvers():
    return (FooResolver,)
