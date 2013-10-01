hubpy-demo
==========

Demo for the use of python flask targeted for RedHat's OpenShift PaaS platform.

Setup your user in OpenShift using rhc CLI
>>> rhc setup -l tres.bailey@partner.bmwgroup.com

Create the python app
>>> rhc app create todo python-2.7

Copy resultant Git URL:
>>> ssh://524a382e4382ec00dd00004c@todo-tresbailey.rhcloud.com/~/git/todo.git/

Add the openshift repo to existing repo
>>> git remote add openshift -f ssh://524a382e4382ec00dd00004c@todo-tresbailey.rhcloud.com/~/git/todo.git/

Merge the openshift repo into the existing repo
>>> git merge openshift/master -s recursive -X ours

Modify the setup.py and application python files to use flask and other components

Add the MongoDB cartridge to the app
>>> rhc cartridge add mongodb-2.2 -a todo

Commit and push your changes to the existing repo
>>> git commit -m "Getting openshift up and running"
>>> git push

Push those changes to the openshift repo, which will kickoff a build to openshift
>>> git push openshift master

Check out your instance via ssh
>>> ssh 524a382e4382ec00dd00004c@todo-tresbailey.rhcloud.com

Watch logs from the application
>>> rhc tail -a todo

Add redis custom cartridge
>>> rhc cartridge add http://cartreflect-claytondev.rhcloud.com/reflect?github=smarterclayton/openshift-redis-cart --app todo

Confirm redis values in OpenShift server
>>> export | grep redis

Confirm redis setup using OpenShift status command
>>> rhc cartridge status redis -a todo

Add phantomjs cartridge for headless testing
>>> rhc cartridge add https://raw.github.com/tresbailey/phantomjs-cartridge/master/metadata/manifest.yml -a todo


