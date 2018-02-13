import os
import subprocess
import sys

def process_files(files):
    DEBUG = True

    for f in files:
        # Grab executables (no extensions)
        executable, ext = os.path.splitext(f)

        # Only work on binary (executable) files
        if ext == "":
            print "Processing %s" % executable

            ls_cmd = ["ls", "-l", executable]
            ls_cmd_output = subprocess.check_output(ls_cmd)
            if DEBUG:
                print "\tls cmd output: {}".format(ls_cmd_output)

            sym_path = ls_cmd_output.split("->")
            sym_target = sym_path[1]
            if DEBUG:
                print "\tsplit[1]: {}".format(sym_target)

            rm_cmd = ["rm", executable]
            if DEBUG:
                rm_cmd.insert(0, "echo")
            rm_cmd_output = subprocess.check_call(rm_cmd)
            if DEBUG:
                print "\trm cmd: {}".format(rm_cmd_output)

            sym_cmd = ["ln", "-s", sym_target, executable]
            if DEBUG:
                sym_cmd.insert(0, "echo")
            sym_cmd_output = subprocess.check_output(sym_cmd)
            if DEBUG:
                print "\tsym cmd: {}".format(sym_cmd_output)

            print "-"*80
            print ""


if __name__ == '__main__':
    process_files(sys.argv[1:])
