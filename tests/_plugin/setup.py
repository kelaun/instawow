from setuptools import setup

setup(
    name='instawow_plugin',
    py_modules=['instawow_plugin'],
    entry_points={'instawow.plugins': ['instawow_plugin = instawow_plugin']},
)
