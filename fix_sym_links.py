import os
import subprocess
import sys

# This script is used to re-symlink binaries in a v00x area on macOS.
# It will replace the old_v00x with new_v00x in the target of the symlink.
#
# Arg: files to modify
#
# e.g.: prog26> cd /opt/usgs/v007_fix; python fix_sym_links.py ports/libexec/gnubin/*

def process_files(files):
    DEBUG = True

    for f in files:
        # Grab executables (no extensions)
        executable, ext = os.path.splitext(f)

        # Only work on symlinks to binaries
        if ext == "" and os.path.islink(executable):
            print "Processing %s" % executable

            ls_cmd = ["ls", "-l", executable]
            ls_cmd_output = subprocess.check_output(ls_cmd)
            if DEBUG:
                print "\tls cmd output: {}".format(ls_cmd_output)

            sym_path = ls_cmd_output.split("->")
            old_sym_target = sym_path[1].strip()
            if DEBUG:
                print "\told sym target: {}".format(old_sym_target)

            rm_cmd = ["rm", executable]
            if DEBUG:
                rm_cmd.insert(0, "echo")
            rm_cmd_output = subprocess.check_output(rm_cmd)
            if DEBUG:
                print "\trm cmd: {}".format(rm_cmd_output)

            # Before symlinking, we need to update the target from v006 to v007
            old_v00x = "v006"
            new_v00x = "v007"
            new_sym_target = old_sym_target.replace(old_v00x, new_v00x)

            sym_cmd = ["ln", "-s", new_sym_target, executable]
            if DEBUG:
                sym_cmd.insert(0, "echo")
            sym_cmd_output = subprocess.check_output(sym_cmd)
            if DEBUG:
                print "\tsym cmd: {}".format(sym_cmd_output)

            print "-"*80
            print ""


if __name__ == '__main__':
    process_files(sys.argv[1:])
