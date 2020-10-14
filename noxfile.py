from __future__ import annotations

import nox

nox.options.envdir = '.py-nox'


@nox.session(python=['3.7', '3.8', '3.9'])
def test(session: nox.Session):
    session.install('.[server, test]')
    session.run('coverage', 'run', '-m', 'pytest')
    session.run('coverage', 'report', '-m')


@nox.session(python=['3.7', '3.8', '3.9'])
def type_check(session: nox.Session):
    # The instawow path is hardcoded in pyrightconfig.json relative
    # to the enclosing folder therefore we can't install instawow in a
    # virtual environment or Pyright won't be able to find it.
    # The next best (least worst) thing is to copy the repo into a
    # temporary folder before performing an editable install so that we don't
    # end up polluting the working directory.  An editable install would not
    # have been required at all if it weren't for ``_version.py``
    # which is generated by setuptools_scm at build time
    # and is imported in ``utils.py``.
    tmp_dir = session.create_tmp()
    session.run('git', 'clone', '.', tmp_dir)
    session.chdir(tmp_dir)
    session.install(
        '-e',
        '.[server]',
        'sqlalchemy-stubs @https://github.com/layday/sqlalchemy-stubs/archive/b4be519.zip',
    )
    session.run('npx', '--cache', '.npm', 'pyright')


@nox.session(reuse_venv=True)
def reformat(session: nox.Session):
    session.install('isort>=5.5.2', 'black>=20.8b1')
    for cmd in ('isort', 'black'):
        session.run(cmd, 'instawow', 'tests', 'noxfile.py', 'setup.py')


@nox.session(python=False)
def clobber_build_artefacts(session: nox.Session):
    session.run('rm', '-rf', 'build', 'dist', 'instawow.egg-info')


@nox.session(python='3.8')
def build(session: nox.Session):
    clobber_build_artefacts(session)
    session.install('build>=0.0.4')
    session.run('python', '-m', 'build', '.')


@nox.session
def publish(session: nox.Session):
    session.install('twine')
    for subcmd in ('check', 'upload'):
        session.run('twine', subcmd, 'dist/*')
