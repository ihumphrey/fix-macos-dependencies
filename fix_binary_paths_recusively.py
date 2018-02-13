import os
import subprocess
import sys

DEBUG = True
VERBOSE = False

path = sys.argv[1]

print "path:  {}".format(path)
for root, dirs, files in os.walk(path):
    if VERBOSE:
        print "root:  {}".format(root)
        print "dirs:  {}".format(dirs)
        print "files: {}".format(files)

    for f in files:
        executable, ext = os.path.splitext(f)
        # Check to see that the file is a binary and is not a symlink
        if ext == "" and not os.path.islink(executable):
            print "Processing {}...".format(executable)
            otool_L_cmd = ["otool", "-L", executable]
            otool_L_cmd_output = subprocess.check_output(otool_L_cmd)
            if VERBOSE:
                print "otool -L : {}".format(otool_L_cmd_output)

            # Split the otool -L by newlines
            v00x_dependencies = otool_L_cmd_output.splitlines()
            old_v00x = "v006"
            new_v00x = "v007"
            for dependency in v00X_dependencies:
                # Replace old v00x with new v00x
                if old_v00x in dependency:
                    # Format of otool -L: dependency (extraneous info)
                    lib = dependency.split(' ')[0].strip()
                    newlib = lib.replace(old_v00x, new_v00x)
                    print "\told dependency: {}".format(lib)
                    print "\tnew dependency: {}".format(newlib)

                    install_name_tool_cmd = ["install_name_tool", "-change", lib, newlib, executable]
                    if DEBUG:
                        install_name_tool_cmd.insert(0, "echo")

                    install_name_tool_cmd_output = subprocess.check_output(install_name_tool_cmd)
                    if DEBUG:
                        print "\tinstall_name_tool cmd: {}".format(install_name_tool_cmd_ouput)

                    otool_L_cmd_output = subprocess.check_output(otool_L_cmd)
                    print "otool -L: {}".format(otool_L_cmd_output)
            print ""
            print "-"*80
            print ""
