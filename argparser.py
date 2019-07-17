import argparse


def arg_parser(flags):
    parser = argparse.ArgumentParser(
            description="This is the program \
                    for download from tweet with picture"
            )
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
            '-H',
            "--head",
            help='display browser.(default:False)',
            action="store_false",
            default=True
            )
    parser.add_argument(
            "--parallel",
            help='Parallelize download.(default:False)',
            action="store_true",
            default=False
            )
    parser.add_argument(
            "--thread",
            help='do with multi thread. \
                    use with --parallel option(default:False)',
            action="store_true",
            default=False
            )
    parser.add_argument(
            '-f',
            "--followers",
            help='adapt to followers tweet.(default:False)',
            action="store_true"
            )
    group.add_argument(
            '-m',
            "--media",
            help='download target\'s media tweet. \
                    Don\'t use with -l option. (default:False)',
            action="store_true",
            default=False
            )
    group.add_argument(
            '-l',
            "--likes",
            help='download target\'s likes tweet. \
                    Don\'t use with -m option.(default:True)',
            action="store_true",
            default=True
            )
    parser.add_argument(
            '-t',
            "--target",
            help='set download target.(default:i)',
            default="i"
            )
    parser.add_argument(
            '-u',
            "--user",
            dest='UserID',
            help='set your twitter userID.',
            default=False
            )
    parser.add_argument(
            '-d',
            dest='dirName',
            help='set optional directory name.',
            default="./pictures/"
            )
    parser.add_argument(
            '-p',
            "--password",
            dest='Password',
            help='set your twitter password.',
            default=False)
    parser.add_argument(
            '-n',
            '--number',
            dest='N',
            help='set number of download.',
            type=int,
            default=-1)
    parser.add_argument(
            '--degree',
            dest='DOP',
            help='set degree of parallelism.',
            type=int,
            default=-1)
    args = parser.parse_args()
    flags['followers'] = args.followers
    flags['media'] = args.media
    flags['likes'] = args.likes
    flags['target'] = args.target
    flags['userID'] = args.UserID
    flags['password'] = args.Password
    flags['number'] = args.N
    flags['headless'] = args.head
    flags['parallel'] = args.parallel
    flags['thread'] = args.thread
    flags['dir'] = args.dirName
    flags['dop'] = args.DOP
