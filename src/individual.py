#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pathlib
from typing import List, Optional


def display_tree(
    directory: pathlib.Path,
    args: argparse.Namespace,
    prefix: str = "",
    current_depth: int = 0
) -> None:
    """
    Рекурсивная функция для отображения дерева каталогов и файлов.

    :param directory: Путь к директории, которую нужно отображать.
    :param args: Объект аргументов командной строки.
    :param prefix: Префикс для отступов при отображении дерева.
    :param current_depth: Текущий уровень глубины для отображения дерева.
    """
    if args.s is not None and current_depth > args.s:
        return

    items = list(directory.iterdir())
    items.sort()

    for idx, item in enumerate(items):
        connector = "├── " if idx < len(items) - 1 else "└── "
        new_prefix = prefix + ("│   " if idx < len(items) - 1 else "    ")

        # Вывести дерево директорий
        if item.is_dir():
            if not args.f:
                print(prefix + connector + item.name + "/")
            display_tree(item, args, new_prefix, current_depth + 1)
        # Вывести дерево только с файлами
        elif item.is_file() and not args.d:
            # Если указан ключ -a, то учитываются скрытые файлы
            if args.a or not item.name.startswith("."):
                size = item.stat().st_size
                # Если ключ -t, то указывать полный путь
                if args.t:
                    print(f"{prefix}{connector}{item} ({size} bytes)")
                else:
                    print(f"{prefix}{connector}{item.name} ({size} bytes)")


def main(command_line: Optional[List[str]] = None) -> None:
    """
    Главная функция программы.

    :param command_line: Аргументы командной строки (по умолчанию None, если
                          вызывается непосредственно из командной строки).
    """
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.0.1"
    )
    parser.add_argument("directory", type=str, help="The directory to list.")
    # Выводятся даже скрытые файлы.
    parser.add_argument(
        "-a", action="store_true", help="All files are listed."
    )
    # -f и -d взаимосключающие, их нужно запретить вводить одновременно.
    choose = parser.add_mutually_exclusive_group()
    # Отображать каталоги.
    choose.add_argument(
        "-d", action="store_true", help="List directories only."
    )
    # Отображать файлы.
    choose.add_argument("-f", action="store_true", help="List files only.")
    # Максимальная глубина отображения дерева
    parser.add_argument(
        "-s", type=int, help="Max display depth of the directory tree."
    )
    # Не просто имя файла, а полное имя.
    parser.add_argument(
        "-t",
        action="store_true",
        help="Print the full path prefix for each file.",
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    directory = pathlib.Path(args.directory).resolve(strict=True)
    display_tree(directory, args)


if __name__ == "__main__":
    main()
