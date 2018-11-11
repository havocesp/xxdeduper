# -*- coding: utf-8 -*-

import pathlib
from collections import OrderedDict
from datetime import datetime
from mmap import mmap, ACCESS_READ

_MEASURES = OrderedDict(bytes=1, kb=1024, mb=pow(1024, 2), gb=pow(1024, 3), tb=pow(1024, 4))
_UNITS = list(_MEASURES.keys())
_DATETIME = '%d-%m-%Y %H:%M:%S'


def mod_time2datetime(file):
    """
    Return file modification timestamp as a human readable format (%d-%m-%Y %H:%M:%S)

    :param file: file path where modification timestamp will be extracted.
    :type file: str or pathlib.Path
    :return str: file modification timestamp as a human readable format.
    """
    mod_time = pathlib.Path(file).stat().st_mtime
    mod_time = datetime.fromtimestamp(mod_time)
    return mod_time.strftime(_DATETIME)


def bytes2unit(size, unit=None):
    """
    Convert N bytes to a specific filesystem unit.

    >>> bytes2unit(1024)
    1024
    >>> bytes2unit(5242, 'kb')
    5.119140625

    :param size: size type should be a Path like object or int / float file size in bytes.
    :type size: int or float or pathlib.Path
    :param str unit: unit to convert to. Accepted values: bytes, kb, mb, gb
    :return float: conversion result as float.
    """
    unit = str(unit or 'bytes').lower()
    result = 0

    size = size.stat().st_size if isinstance(size, pathlib.Path) else size
    if size > 0:
        result = size / _MEASURES.get(unit)  # type: float
        result = int(result) if result.is_integer() else result
    return result


def infer_unit(size):
    """
    Returns most suitable filesystem unit for size bytes amount.

    >>> infer_unit(256)
    'bytes'
    >>> infer_unit(1024)
    'kb'
    >>> infer_unit(1024*1024)
    'mb'

    :param size:  size type should be a Path like object or int / float file size in bytes.
    :type size: float or int or pathlib.Path
    :return str: most suitable filesystem unit for size.
    """
    if isinstance(size, pathlib.Path):
        size = size.stat().st_size
    if size > 0:
        prev_unit = 'bytes'
        for u in _UNITS:
            converted_size = bytes2unit(size, u)
            if converted_size < 1:
                return prev_unit
            else:
                prev_unit = u
    else:
        return 'bytes'


def get_formatted_size(size, unit=None, precision=2):
    """
    Get format file size.

    >>> get_formatted_size(45389, unit='mb')
    '0.04329 mb'
    >>> get_formatted_size(242)
    '242 bytes'
    >>> get_formatted_size(3432543654)
    '3.19681 gb'

    :param size: file size bytes as float.
    :param str unit: if set file size will be formatted according "unit" param value, otherwise it will be inferred.
    :param int precision: desired result decimals precision.
    :return str: str type file size represented using unit.
    """
    unit = str(unit).lower() if unit and unit in _UNITS else infer_unit(size)
    str_format = '{:.@f}'.replace('@', str(precision))
    return '{} {}'.format(str_format.format(bytes2unit(size if size else 0, unit)).rstrip('.0'), unit)


def readfile(file_path):
    """
    Read all bytes from file in path

    >>> content = readfile('/home/godmin/.bashrc')
    >>> isinstance(content, bytes) and len(content) > 0
    True

    :param file_path: path to file which is to be read
    :type file_path: str or pathlib.Path
    :return bytes: a bytes type with file content
    """
    if isinstance(file_path, str):
        file_path = pathlib.Path(file_path)
    data = bytes()
    if file_path.is_file():
        size = file_path.stat().st_size
        if size > 0.0:
            with file_path.open() as infile:
                m = mmap(infile.fileno(), 0, access=ACCESS_READ)
                data = m.read()
    return data
