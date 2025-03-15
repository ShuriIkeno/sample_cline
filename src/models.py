#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書管理アプリのモデルクラスを定義するモジュール。

このモジュールでは、読書管理アプリで使用する基本的なデータモデルである
Book（本）クラスとDiary（日記）クラスを定義しています。
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, ClassVar


class Book:
    """本の情報を管理するクラス。

    Attributes:
        id: 本の一意識別子
        title: タイトル
        author: 著者
        published_year: 出版年
        genre: ジャンル
        memo: メモ
    """

    def __init__(
        self,
        title: str,
        author: str,
        published_year: int,
        genre: str = "",
        memo: str = "",
        book_id: Optional[str] = None,
    ):
        """Bookクラスのコンストラクタ。

        Args:
            title: 本のタイトル
            author: 著者名
            published_year: 出版年
            genre: ジャンル（デフォルトは空文字列）
            memo: メモ（デフォルトは空文字列）
            book_id: 本のID（指定しない場合は自動生成）
        """
        self.id = book_id if book_id else str(uuid.uuid4())
        self.title = title
        self.author = author
        self.published_year = published_year
        self.genre = genre
        self.memo = memo

    def to_dict(self) -> Dict[str, Any]:
        """本の情報を辞書形式で返す。

        Returns:
            本の情報を含む辞書
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "published_year": self.published_year,
            "genre": self.genre,
            "memo": self.memo,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        """辞書から本のオブジェクトを生成する。

        Args:
            data: 本の情報を含む辞書

        Returns:
            生成されたBookオブジェクト
        """
        return cls(
            title=data["title"],
            author=data["author"],
            published_year=data["published_year"],
            genre=data.get("genre", ""),
            memo=data.get("memo", ""),
            book_id=data["id"],
        )

    def __str__(self) -> str:
        """本の情報を文字列で返す。

        Returns:
            本の情報を含む文字列
        """
        return f"{self.title} by {self.author} ({self.published_year})"


class Diary:
    """日記の情報を管理するクラス。

    Attributes:
        id: 日記の一意識別子
        book_id: 関連する本のID
        date: 日記の日付
        content: 日記の内容
    """

    DATE_FORMAT: ClassVar[str] = "%Y-%m-%d"

    def __init__(
        self,
        book_id: str,
        content: str,
        date: Optional[datetime] = None,
        diary_id: Optional[str] = None,
    ):
        """Diaryクラスのコンストラクタ。

        Args:
            book_id: 関連する本のID
            content: 日記の内容
            date: 日記の日付（指定しない場合は現在の日付）
            diary_id: 日記のID（指定しない場合は自動生成）
        """
        self.id = diary_id if diary_id else str(uuid.uuid4())
        self.book_id = book_id
        self.date = date if date else datetime.now()
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        """日記の情報を辞書形式で返す。

        Returns:
            日記の情報を含む辞書
        """
        return {
            "id": self.id,
            "book_id": self.book_id,
            "date": self.date.strftime(self.DATE_FORMAT),
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Diary":
        """辞書から日記のオブジェクトを生成する。

        Args:
            data: 日記の情報を含む辞書

        Returns:
            生成されたDiaryオブジェクト
        """
        date = datetime.strptime(data["date"], cls.DATE_FORMAT)
        return cls(
            book_id=data["book_id"],
            content=data["content"],
            date=date,
            diary_id=data["id"],
        )

    def __str__(self) -> str:
        """日記の情報を文字列で返す。

        Returns:
            日記の情報を含む文字列
        """
        return f"{self.date.strftime(self.DATE_FORMAT)}: {self.content[:30]}..."
