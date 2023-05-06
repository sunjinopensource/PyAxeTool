import argparse, glob
from PyAxe import AHash

def is_glob_pattern(s):
    return ('?' in s) or ('*' in s)

def handle_sub_cmd_file(args):
    if is_glob_pattern(args.pattern):
        for file_path in glob.glob(args.pattern):
            print(file_path + ': ' + AHash.getMD5OfFile(file_path))
    else:
        print(AHash.getMD5OfFile(args.pattern))

def handle_sub_cmd_dir(args):
    print(AHash.getMD5OfDir(args.dirpath))

def handle_sub_cmd_str(args):
    print(AHash.getMD5OfStr(args.str))

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='sub_cmd')
    subparser = subparsers.add_parser('file', help='显示文件MD5')
    subparser.add_argument('pattern', help='通配符')
    subparser = subparsers.add_parser('dir', help='显示目录MD5')
    subparser.add_argument('dirpath', help='目录路径')
    subparser = subparsers.add_parser('str', help='显示字符串MD5')
    subparser.add_argument('str', help='字符串')

    return parser.parse_args()

g_args = parse_args()

def main():
    funcs = {
        'file': handle_sub_cmd_file,
        'dir': handle_sub_cmd_dir,
        'str': handle_sub_cmd_str,
    }
    funcs[g_args.sub_cmd](g_args)
    
if __name__ == '__main__':
    main()