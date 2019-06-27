import glob
from PyAxe import AHash

def isGlobPattern(s):
    return ('?' in s) or ('*' in s)

def initArgs(subparsers):
    subparser = subparsers.add_parser('ShowMD5OfFile', help='显示文件MD5')
    subparser.add_argument('Pattern', help='通配符')

    subparser = subparsers.add_parser('ShowMD5OfDir', help='显示目录MD5')
    subparser.add_argument('DirPath', help='目录路径')

    subparser = subparsers.add_parser('ShowMD5OfStr', help='显示字符串MD5')
    subparser.add_argument('Str', help='字符串')

def ShowMD5OfFile(pattern):
    if isGlobPattern(pattern):
        for filePath in glob.glob(pattern):
            print(filePath + ': ' + AHash.getMD5OfFile(filePath))
    else:
        print(AHash.getMD5OfFile(pattern))

def ShowMD5OfDir(dirPath):
        print(AHash.getMD5OfDir(dirPath))

def ShowMD5OfStr(s):
        print(AHash.getMD5OfStr(s))

def main(args):
    if args.SubCommand == 'ShowMD5OfFile':
        ShowMD5OfFile(args.Pattern)
    elif args.SubCommand == 'ShowMD5OfDir':
        ShowMD5OfDir(args.DirPath)
    elif args.SubCommand == 'ShowMD5OfStr':
        ShowMD5OfDir(args.Str)
    else:
        return False
    return True