import os
from PyAxe import AOS, APyInstaller, ACompress, AUtil

def initArgs(subparsers):
    subparser = subparsers.add_parser('PyInstaller', help='制作可执行文件')
    subparser.add_argument('Targets', nargs='+', help='目标列表')
    subparser.add_argument('--SkipTargetsOnWindows', nargs='*', help='在Windows平台上跳过的目标列表')
    subparser.add_argument('--SkipTargetsOnLinux', nargs='*', help='在Linux平台上跳过的目标列表')
    subparser.add_argument('--OneFile', action='store_true', help='单文件形式（默认为文件夹形式）')
    subparser.add_argument('--Pack', choices=['zip', 'tar'], help='打包方式（默认不打包）')


def getTargetsFromInput(args):
    targetMap = [['1', '所有', 'All']]
    index = 2
    for target in enumerate(args.Targets):
        if os.name == 'nt':
            if target in args.SkipTargetsOnWindows:
                continue
        else:
            if target in args.SkipTargetsOnLinux:
                continue
        targetMap.append([
            '%d' % index,
            target,
            target
        ])
        index += 1

    action = AUtil.inputChoice(targetMap, '*** 编译目标 ***')[2]
    if action == 'All':
        return [item[2] for item in targetMap if item[2] != 'All']
    else:
        return [action]


def makePackageFromDist(target, packStyle):
    AOS.makeDir(os.path.join('Installer', 'dist'))
    AOS.removeDir(os.path.join('Installer', 'dist', target))
    AOS.move(os.path.join('dist', target), os.path.join('Installer', 'dist', target))
    if packStyle:
        with AOS.ChangeDir(os.path.join('Installer', 'dist')):
            if packStyle == 'zip':
                ACompress.zip(target, target+'.zip')
            elif packStyle == 'tar':
                ACompress.tar(target, target+'.tar.gz')
            else:
                assert False


def makeTarget(target, args):
    with AOS.ChangeDir('..'):
        AOS.removeDir('build')
        AOS.removeDir('dist')
        extraOptions = APyInstaller.ExtraOptions()
        APyInstaller.execCommand(target+'.py', target, oneFile=args.OneFile, extraOptions=extraOptions)
        makePackageFromDist(target, args.Pack)
        AOS.removeDir('build')
        AOS.removeDir('dist')


def main(args):
    if args.SubCommand == 'PyInstaller':
        finalTargets = getTargetsFromInput(args)
        for target in finalTargets:
            makeTarget(target, args)
    else:
        return False
    return True
