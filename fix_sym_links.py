import os
import subprocess
import sys

def process_files(files):
    DEBUG = True
    for f in files:
        executable, ext = os.path.splitext(f)
        # Only work on binary (executable) files
        if ext == "":
            print "Processing %s" % executable
            ls_cmd = ["ls", "-l", executable]
            ls_cmd_output = subprocess.check_output(ls_cmd)
            if DEBUG:
                print "\tls cmd output: {}".format(ls_cmd_output)
            sym_path = ls_cmd_output.split("->")
            # TODO: use the 2nd arg of split to get the path (and then remove the trailing \n)
            # TODO: run the ln commands needed.
            print "" 
            print "\tsym path: {}".format(sym_path)
            print ""
            print "-"*80
            print ""


if __name__ == '__main__':
    process_files(sys.argv[1:])
