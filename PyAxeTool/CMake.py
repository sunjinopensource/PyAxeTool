import argparse, glob
from PyAxe import AHash

def handle_sub_cmd_archetype_generate_lib(args):
    print('TODO')
    
def handle_sub_cmd_archetype_generate(args):
    funcs = {
        'lib': handle_sub_cmd_archetype_generate_lib,
    }
    funcs[args.archetype_name](args)

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='sub_cmd')
    subparser = subparsers.add_parser('archetype:generate', help='通过模板创建项目')
    subparser.add_argument('archetype_name', choices=['lib'], help='模板名称')

    return parser.parse_args()

g_args = parse_args()

def main():
    funcs = {
        'archetype:generate': handle_sub_cmd_archetype_generate,
    }
    funcs[g_args.sub_cmd](g_args)
    
if __name__ == '__main__':
    main()