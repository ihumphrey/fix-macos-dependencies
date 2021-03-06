This is used for updating the dependencies of the mac v00X areas.

*You probably want to make a copy of the v00X directory first to modify and make sure it is correct.*

The dependencies are absolute paths to v006 (since v007 was a copy of v006).

These scripts facilitate changing the v006 to v007 by using install_name_tool.

***Please note that the scripts have DEBUG = True. You may run them as is after
copying them to see what they will do. To actually make changes, after copying
the script, change DEBUG to False.***

***Please note that to fix the qt5 and qtw framworks, modify fix_dylib_paths_recursively.py
to check ext == ""***

***ISSUES: does not handle liblevel.dylib.1.18 type dylib's (it looks for .dylib and NOT symlinks)***

1. Run the fix_sym_links.py script on the path you want to fix (recursive).
This will change any binary symlinks from v006 to v007 (ports/libexec/gnubin/)

```
ssh isis3mgr@prog26
cd /opt/usgs/v007_fix
sudo cp <location-of-this-repo>/fix_sym_links.py .

sudo python fix_sym_links.py ports
```

2. Run the fix_binary_paths_recursively.py script on the path you want to fix binaries for:
This will change any binary executable dependencies from v006 to v007.

```
ssh isis3mgr@prog26
cd /opt/usgs/v007_fix
sudo cp <location-of-this-repo/fix_binary_paths_recursively.py .
touch out.log
sudo chown isis3mgr:softlib out.log

sudo python fix_binary_paths_recursively.py 3rdParty >>& out.log
sudo python fix_binary_paths_recursively.py proprietary >>& out.log
sudo python fix_binary_paths_recursively.py ports >>& out.log
sudo python fix_binary_paths_recursively.py tools >>& out.log
```

3. Fix the .dylib dependencies

```
ssh isis3mgr@prog26
cd /opt/usgs/v007_fix
sudo cp <location-of-this-repo/fix_dylib_paths_recursively.py .
touch out.log
sudo chown isis3mgr:softlib out.log

sudo python fix_dylib_paths_recursively.py 3rdParty >>& out.log
sudo python fix_dylib_paths_recursively.py proprietary >>& out.log
sudo python fix_dylib_paths_recursively.py ports >>& out.log
sudo python fix_dylib_paths_recursively.py tools >>& out.log
```

1. Verifying the changes

You have made changes to /opt/usgs/v007_fix.
***Temporarily***:

```
ssh isis3mgr@prog26
cd /opt/usgs
mv v006 v006_BACKUP
mv v007 v007_BACKUP
mv v007_fix v007
exit

ssh prog26
cd /work/users/<your-name>
mkdir test_v007_fix && cd test_v007_fix
git clone git@github.com:<username>/ISIS3.git 
cd ISIS3/isis
sic
<build>
```