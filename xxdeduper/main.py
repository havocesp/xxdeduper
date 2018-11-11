# -*- coding: utf-8 -*-
"""
 XXDeduper

 - Author:      Daniel J. Umpierrez
 - Created:     11-11-2018
 - License:     UNLICENSE
"""
import argparse
import pathlib
from collections import OrderedDict

import tqdm
import xxhash

from utils import get_formatted_size, bytes2unit, mod_time2datetime

_SEP = '-' * 25
_HASH_TEMPLATE = 'Hash {} - ({})'


def main(args):
    file_map = dict()

    print(' === XXHASH dupes finder ===')
    print(' - Searching for duplicate files ...\n')

    num_files = 0
    min_size = args.min_size
    max_size = args.max_size
    hide_time = args.hide_time
    hide_recent = args.hide_recent
    hide_hash = args.hide_hash
    paths = [p for p in args.paths if p.exists()]
    print('  * Building file list ...')
    total_size = 0

    def add_file(file):
        file_hash = xxhash.xxh64(file.read_bytes()).hexdigest()
        if file_hash in file_map:
            file_map[file_hash].append(pathlib.Path(file))
        else:
            file_map.update(**{file_hash: [pathlib.Path(file)]})

    def check_size_limits(value):
        return max_size > bytes2unit(value) > min_size

    try:
        for e in paths:
            try:
                if e.exists():
                    if e.is_dir():
                        print(' - Creating list of files from {}, this could take a while ...'.format(str(e)))
                        files = list()
                        for f in e.rglob('*'):
                            if f.exists() and not f.is_symlink() and f.is_file() and check_size_limits(f):
                                total_size += f.stat().st_size
                                num_files += 1
                                files.append(f)
                        print('  * {} files found ({}).'.format(num_files, get_formatted_size(total_size)))
                        for i, f in zip(tqdm.tqdm(range(num_files), unit='file'), files):
                            add_file(f)
                    elif not e.is_symblink() and e.is_file():
                        e = e.resolve(strict=True)
                        if check_size_limits(e):
                            print(' - Reading {} file.'.format(str(e)))
                            add_file(e)
            except FileNotFoundError as err:
                print(str(err))

        if len(file_map) > 0:

            dupes_size = 0
            num_dupes = 0
            file_map = OrderedDict(sorted(file_map.items(), key=lambda item: item[1][0].stat().st_size))
            for k, v in file_map.items():
                if len(v) > 1:
                    num_dupes += len(v[1:])
                    file_size = get_formatted_size(v[0])
                    dupes_size += bytes2unit(v[0])
                    v = sorted(v, key=lambda x: x.stat().st_mtime, reverse=True)

                    if hide_recent:
                        v = v[1:]

                    if not hide_hash:
                        print(_HASH_TEMPLATE.format(k, file_size))
                        print(_SEP)
                    if hide_time:
                        data = ['"{}"'.format(dupe) for dupe in v]
                    else:
                        data = ['{}:"{}"'.format(mod_time2datetime(dupe), dupe) for dupe in v]
                    print('\n'.join(data))
                    print()

                print('  * {} duplicate files ({}).'.format(num_dupes, dupes_size))
            else:
                print('No duplicated files found.')

    except KeyboardInterrupt:
        print('Forced exit.')
    except RuntimeError:
        print('Forced exit.')
    except (FileNotFoundError, EnvironmentError, EOFError) as err:
        raise err


if __name__ == '__main__':
    parser = argparse.ArgumentParser('xxdeduper')
    parser.add_argument('paths', nargs='+', type=pathlib.Path, metavar='PATH',
                        help='Paths where look for duplicated files.')
    parser.add_argument('-m', '--min-size', type=int, default=0, help='Min file size filter in bytes.')
    parser.add_argument('-M', '--max-size', type=int, default=pow(1024, 5), help='Min file size filter in bytes.')
    parser.add_argument('-r', '--hide-recent', action="store_true",
                        help='Hide most recently modified file from each dupes group.')
    parser.add_argument('-H', '--hide-hash', action="store_true", help='Hide file hash info.')
    parser.add_argument('-t', '--hide-time', action="store_true", help='Hide file hash info.')
    parser.add_argument('-d', '--del-empty', action="store_true", help='Remove empty files / dirs.')

    parsed_args = parser.parse_args()
    main(parsed_args)
