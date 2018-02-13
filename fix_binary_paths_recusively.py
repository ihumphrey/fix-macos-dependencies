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
            # Run otool -L and -D on each file
            otool_L = subprocess.check_output(["otool", "-L", executable])
            # otool_D = subprocess.check_output(["otool", "-D", executable])
            # Split the otool -L by newlines
            libs = otool_L.splitlines()
            for s in libs:
                # Replace any "v006" with "v007"
                if "v006" in s:
                    lib = s.split(' ')[0].strip()
                    if DEBUG:
                        print "\t{}".format(lib)
                        print "\t{}".format(lib.replace("v006", "v007"))
                        # print "otool -D: {}".format(otool_D)
                    newlib = lib.replace("v006", "v007")
                    install_name_tool_cmd = ["install_name_tool", "-change", lib, newlib, executable]
                    if DEBUG:
                        install_name_tool_cmd.insert(0, "echo")
                    try:
                        change_path = subprocess.check_output(install_name_tool_cmd)
		        print "CMD: {}".format(change_path)
                    except CalledProcessError as e:
                        print "Error running the following command: "
                        print "\t{}".format(install_name_tool_cmd)
                        print "\tERROR: {}".format(e.strerror)
            print ""


if __name__ == '__main__':
    process_files(sys.argv[1:])
