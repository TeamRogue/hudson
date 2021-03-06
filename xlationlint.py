import sys
import urllib
import urllib2
import json
import os

for change in sys.argv[1:]:
    print change
    f = urllib2.urlopen('http://review.cyanogenmod.com/query?q=change:%s' % change)
    d = f.read()
    # gerrit doesnt actually return json. returns two json blobs, separate lines. bizarre.
    d = d.split('\n')[0]
    data = json.loads(d)
    project = data['project']
    project = project.replace('CyanogenMod/', '').replace('android_', '')

    while not os.path.isdir(project):
        new_project = project.replace('_', '/', 1)
        if new_project == project:
            break
        project = new_project

    retval = os.system('cd %s ; git show FETCH_HEAD | grep ^diff | awk {\'print $3\'} | egrep "res/.*xml$" | sed -e \'s/^a\///g\' | grep "donottranslate"' % (project))

    if (retval == 0):
        print "Translating a 'donottranslate' file, invalid patch"
        sys.exit(1)

    retval = os.system('cd %s ; xmllint --noout `git show FETCH_HEAD | grep ^diff | awk {\'print $3\'} | egrep "res/.*xml$" | sed -e \'s/^a\///g\'`' % (project))
    sys.exit(retval!=0)
