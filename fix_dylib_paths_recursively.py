import os
import subprocess
import sys

DEBUG = True
VERBOSE = False

path = sys.argv[1]

print "path:  {}".format(path)
for root, dirs, files in os.walk(path):
    if "macports/sources" in root:
        continue
    if VERBOSE:
        print "root:  {}".format(root)
        print "dirs:  {}".format(dirs)
        print "files: {}".format(files)

    for f in files:
        stripped_executable, ext = os.path.splitext(f)
        executable = os.path.join(root, f)

        # Check to see that the file is a shared lib and is not a symlink
        if ext == ".dylib" and not os.path.islink(executable):
            print "Processing {} ...".format(executable)
            otool_D_cmd = ["otool", "-D", executable]
            try:
                otool_D_cmd_output = subprocess.check_output(otool_D_cmd)
            except subprocess.CalledProcessError as e:
                print "\tWARNING -- skipping {}".format(executable)
                print "\t\tCMD: {}".format(otool_D_cmd)
                print "\t\tMSG: {}".format(repr(e))
                continue
            if VERBOSE:
                print "otool -D : {}".format(otool_D_cmd_output)

            otool_L_cmd = ["otool", "-L", executable]
            try:
                otool_L_cmd_output = subprocess.check_output(otool_L_cmd)
            except subprocess.CalledProcessError as e:
                print "\tWARNING -- skipping {}".format(executable)
                print "\t\tCMD: {}".format(otool_L_cmd)
                print "\t\tMSG: {}".format(repr(e))
                continue
            if VERBOSE:
                print "otool -L : {}".format(otool_L_cmd_output)

            old_v00x = "v006"
            new_v00x = "v007"

            # Split the otool -D (format is libname:\n id)
            lib_id = otool_D_cmd_output.splitlines()
            # Check to see if dylib has an id set, and modify it if it does and has old v00x
            if len(lib_id) == 2:
                lib_id = lib_id[1]
            else:
                continue
            if old_v00x in lib_id:
                new_id = lib_id.replace(old_v00x, new_v00x)
                print "\told id: {}".format(lib_id)
                print "\tnew id: {}".format(new_id)

                install_name_tool_cmd = ["install_name_tool", "-id", new_id, executable]
                if DEBUG:
                    install_name_tool_cmd.insert(0, "echo")

                try:
                    install_name_tool_cmd_output = subprocess.check_output(install_name_tool_cmd)
                except subprocess.CalledProcessError as e:
                    print "\tWARNING -- skipping {}".format(executable)
                    print "\t\tCMD: {}".format(install_name_tool_cmd)
                    print "\t\tMSG: {}".format(repr(e))
                if DEBUG:
                    print "\tinstall_name_tool cmd: {}".format(install_name_tool_cmd_output)

                print ""

            # Split the otool -L by newlines
            v00x_dependencies = otool_L_cmd_output.splitlines()

            for dependency in v00x_dependencies:
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

                    try:
                        install_name_tool_cmd_output = subprocess.check_output(install_name_tool_cmd)
                    except subprocess.CalledProcessError as e:
                        print "\tWARNING -- skipping {}".format(executable)
                        print "\t\tCMD: {}".format(install_name_tool_cmd)
                        print "\t\tMSG: {}".format(repr(e))

                    if DEBUG:
                        print "\tinstall_name_tool cmd: {}".format(install_name_tool_cmd_output)

                    if VERBOSE:
                        otool_L_cmd_output = subprocess.check_output(otool_L_cmd)
                        print "otool -L: {}".format(otool_L_cmd_output)
            print ""
            print "-"*80
            print ""
