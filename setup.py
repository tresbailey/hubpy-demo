from setuptools import setup

setup(name='Todo Demo',
      version='1.0',
      description='OpenShift App',
      author='Tres\' Bailey',
      author_email='tres.bailey@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[ 'Flask==0.8', 'MongoAlchemy==0.11',
        'Werkzeug==0.8.3',
        'pymongo==2.1.1', 'python-dateutil==1.5',
        'redis==2.4.11', 'simplejson==2.1.6', 
        'wsgiref==0.1.2',
        'Flask-MongoAlchemy==0.5.3', 'flask_oauth==0.12']
     )
