import sys
from utils import *
import time as tm
from datetime import datetime, timedelta


def travel(dump_file: str, diff_dir:str, target_date: str, target_file: str):
    actual_date = time()
    date_before = datetime.strftime(datetime.strptime(actual_date, "%Y_%m_%d") - timedelta(days=1), "%Y_%m_%d")
    cmd(["xdelta3", "-d", "-s", dump_file, diff_dir + dump_file.split("/")[-1] + "-" + actual_date + "-" + date_before, target_file + "." + date_before])   
    actual_date = date_before
    while actual_date != target_date:
        date_before = datetime.strftime(datetime.strptime(actual_date, "%Y_%m_%d") - timedelta(days=1), "%Y_%m_%d")
        output, error = cmd(["xdelta3", "-d", "-f", "-s", target_file + "." + actual_date, diff_dir + dump_file.split("/")[-1] + "-" + actual_date + "-" + date_before, target_file + "." + date_before])
        if error != b'':
            exit("Fatal: " + error.decode("UTF-8"))
        cmd(["rm", target_file + "." + actual_date])
        actual_date = date_before
    print(target_file + "." + date_before)    

def main(args):
    if (len(args) != 4):
        exit("Usage:\n python main.py <path_to_dump_file> <path_to_diff_dir> <target_date> <path_to_target_dump_file>");
    travel(args[0], args[1], args[2], args[3])
    

if __name__ == "__main__":
    main(sys.argv[1:])
