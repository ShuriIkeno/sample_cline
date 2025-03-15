#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書管理アプリのメインモジュール。

このモジュールは、読書管理アプリのエントリーポイントとなるモジュールです。
BookManagerとStreamlitUIのインスタンスを作成し、アプリケーションを起動します。
"""

import os
import sys
import argparse

# 現在のディレクトリをPythonのパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from book_manager import BookManager
from streamlit_ui import StreamlitUI


def main():
    """アプリケーションのメイン関数。

    コマンドライン引数を解析し、アプリケーションを起動します。
    """
    parser = argparse.ArgumentParser(description="読書管理アプリ")
    parser.add_argument(
        "--data-file",
        type=str,
        default="book_data.json",
        help="データファイルのパス（デフォルト: book_data.json）",
    )
    args = parser.parse_args()

    # データファイルのディレクトリが存在しない場合は作成
    data_dir = os.path.dirname(args.data_file)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # BookManagerとStreamlitUIのインスタンスを作成
    book_manager = BookManager(data_file=args.data_file)
    ui = StreamlitUI(book_manager=book_manager)

    # アプリケーションを起動
    print(f"データファイル: {args.data_file}")
    print("読書管理アプリを起動しています...")
    ui.run()

main()
