#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書管理アプリのデータ管理クラスを定義するモジュール。

このモジュールでは、読書管理アプリで使用するデータ（本と日記）を管理する
BookManagerクラスを定義しています。
"""

import json
import os
from typing import Dict, List, Optional, Union, Any

from models import Book, Diary


class BookManager:
    """本と日記のデータを管理するクラス。

    このクラスは、本と日記のデータを管理し、JSONファイルに保存・読み込みを行います。

    Attributes:
        books: 本のIDをキーとした本のオブジェクトの辞書
        diaries: 本のIDをキーとした日記のリストの辞書
        data_file: データを保存するJSONファイルのパス
    """

    def __init__(self, data_file: str = "book_data.json"):
        """BookManagerクラスのコンストラクタ。

        Args:
            data_file: データを保存するJSONファイルのパス（デフォルトは"book_data.json"）
        """
        self.books: Dict[str, Book] = {}
        self.diaries: Dict[str, List[Diary]] = {}
        self.data_file = data_file
        self.load_data()

    def add_book(self, book: Book) -> str:
        """本を追加する。

        Args:
            book: 追加する本のオブジェクト

        Returns:
            追加された本のID
        """
        self.books[book.id] = book
        if book.id not in self.diaries:
            self.diaries[book.id] = []
        self.save_data()
        return book.id

    def update_book(self, book: Book) -> bool:
        """本の情報を更新する。

        Args:
            book: 更新する本のオブジェクト

        Returns:
            更新が成功したかどうか
        """
        if book.id not in self.books:
            return False
        self.books[book.id] = book
        self.save_data()
        return True

    def delete_book(self, book_id: str) -> bool:
        """本を削除する。

        Args:
            book_id: 削除する本のID

        Returns:
            削除が成功したかどうか
        """
        if book_id not in self.books:
            return False
        del self.books[book_id]
        if book_id in self.diaries:
            del self.diaries[book_id]
        self.save_data()
        return True

    def get_book(self, book_id: str) -> Optional[Book]:
        """指定したIDの本を取得する。

        Args:
            book_id: 取得する本のID

        Returns:
            取得した本のオブジェクト。存在しない場合はNone。
        """
        return self.books.get(book_id)

    def get_all_books(self) -> List[Book]:
        """すべての本のリストを取得する。

        Returns:
            すべての本のリスト
        """
        return list(self.books.values())

    def search_books(self, query: str) -> List[Book]:
        """クエリに一致する本のリストを取得する。

        タイトル、著者、ジャンル、メモのいずれかにクエリが含まれる本を検索します。

        Args:
            query: 検索クエリ

        Returns:
            クエリに一致する本のリスト
        """
        query = query.lower()
        results = []
        for book in self.books.values():
            if (
                query in book.title.lower()
                or query in book.author.lower()
                or query in book.genre.lower()
                or query in book.memo.lower()
            ):
                results.append(book)
        return results

    def add_diary(self, diary: Diary) -> str:
        """日記を追加する。

        Args:
            diary: 追加する日記のオブジェクト

        Returns:
            追加された日記のID
        """
        if diary.book_id not in self.books:
            raise ValueError(f"Book with ID {diary.book_id} does not exist")

        if diary.book_id not in self.diaries:
            self.diaries[diary.book_id] = []

        self.diaries[diary.book_id].append(diary)
        self.save_data()
        return diary.id

    def update_diary(self, diary: Diary) -> bool:
        """日記の情報を更新する。

        Args:
            diary: 更新する日記のオブジェクト

        Returns:
            更新が成功したかどうか
        """
        if diary.book_id not in self.diaries:
            return False

        for i, d in enumerate(self.diaries[diary.book_id]):
            if d.id == diary.id:
                self.diaries[diary.book_id][i] = diary
                self.save_data()
                return True
        return False

    def delete_diary(self, diary_id: str) -> bool:
        """日記を削除する。

        Args:
            diary_id: 削除する日記のID

        Returns:
            削除が成功したかどうか
        """
        for book_id, diaries in self.diaries.items():
            for i, diary in enumerate(diaries):
                if diary.id == diary_id:
                    del self.diaries[book_id][i]
                    self.save_data()
                    return True
        return False

    def get_diary(self, diary_id: str) -> Optional[Diary]:
        """指定したIDの日記を取得する。

        Args:
            diary_id: 取得する日記のID

        Returns:
            取得した日記のオブジェクト。存在しない場合はNone。
        """
        for diaries in self.diaries.values():
            for diary in diaries:
                if diary.id == diary_id:
                    return diary
        return None

    def get_diaries_for_book(self, book_id: str) -> List[Diary]:
        """指定した本のすべての日記のリストを取得する。

        Args:
            book_id: 本のID

        Returns:
            指定した本のすべての日記のリスト
        """
        if book_id not in self.diaries:
            return []
        return sorted(self.diaries[book_id], key=lambda d: d.date, reverse=True)

    def search_diaries(self, book_id: str, query: str) -> List[Diary]:
        """指定した本の中でクエリに一致する日記のリストを取得する。

        日記の内容にクエリが含まれる日記を検索します。

        Args:
            book_id: 本のID
            query: 検索クエリ

        Returns:
            クエリに一致する日記のリスト
        """
        if book_id not in self.diaries:
            return []

        query = query.lower()
        results = []
        for diary in self.diaries[book_id]:
            if query in diary.content.lower():
                results.append(diary)
        return results

    def save_data(self) -> bool:
        """データをJSONファイルに保存する。

        Returns:
            保存が成功したかどうか
        """
        try:
            data: Dict[str, Any] = {
                "books": {book_id: book.to_dict() for book_id, book in self.books.items()},
                "diaries": {
                    book_id: [diary.to_dict() for diary in diaries]
                    for book_id, diaries in self.diaries.items()
                },
            }
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self) -> bool:
        """JSONファイルからデータを読み込む。

        Returns:
            読み込みが成功したかどうか
        """
        if not os.path.exists(self.data_file):
            return False

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.books = {
                book_id: Book.from_dict(book_data)
                for book_id, book_data in data.get("books", {}).items()
            }
            self.diaries = {
                book_id: [Diary.from_dict(diary_data) for diary_data in diaries_data]
                for book_id, diaries_data in data.get("diaries", {}).items()
            }
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
