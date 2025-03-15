#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書管理アプリのGUIを定義するモジュール。

このモジュールでは、読書管理アプリのGUIを提供するGradioUIクラスを定義しています。
"""

import os
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

import gradio as gr

from models import Book, Diary
from book_manager import BookManager


class GradioUI:
    """Gradioを使用したGUIを提供するクラス。

    このクラスは、Gradioを使用して読書管理アプリのGUIを提供します。

    Attributes:
        book_manager: 本と日記のデータを管理するオブジェクト
    """

    def __init__(self, book_manager: BookManager):
        """GradioUIクラスのコンストラクタ。

        Args:
            book_manager: 本と日記のデータを管理するオブジェクト
        """
        self.book_manager = book_manager
        self.interface = None

    def create_ui(self) -> gr.Blocks:
        """Gradio UIを作成する。

        Returns:
            作成されたGradio Blocksオブジェクト
        """
        with gr.Blocks(title="読書管理アプリ") as interface:
            gr.Markdown("# 読書管理アプリ")

            with gr.Tabs():
                # 本の管理タブ
                with gr.TabItem("本の管理"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("## 本の登録")
                            with gr.Group():
                                title_input = gr.Textbox(label="タイトル", placeholder="タイトルを入力してください")
                                author_input = gr.Textbox(label="著者", placeholder="著者名を入力してください")
                                year_input = gr.Number(label="出版年", placeholder="出版年を入力してください", precision=0)
                                genre_input = gr.Textbox(label="ジャンル", placeholder="ジャンルを入力してください")
                                memo_input = gr.Textbox(label="メモ", placeholder="メモを入力してください", lines=3)
                                add_book_btn = gr.Button("本を登録", variant="primary")
                                add_book_output = gr.Textbox(label="結果", interactive=False)

                            gr.Markdown("## 本の検索")
                            with gr.Group():
                                search_input = gr.Textbox(label="検索キーワード", placeholder="検索キーワードを入力してください")
                                search_btn = gr.Button("検索", variant="secondary")

                        with gr.Column(scale=2):
                            gr.Markdown("## 本の一覧")
                            books_table = gr.Dataframe(
                                headers=["ID", "タイトル", "著者", "出版年", "ジャンル", "メモ"],
                                datatype=["str", "str", "str", "number", "str", "str"],
                                row_count=10,
                                col_count=(6, "fixed"),
                                interactive=False,
                            )

                            with gr.Row():
                                refresh_books_btn = gr.Button("一覧を更新", variant="secondary")
                                delete_book_btn = gr.Button("選択した本を削除", variant="stop")

                            gr.Markdown("## 本の編集")
                            with gr.Group():
                                edit_book_id = gr.Textbox(label="本のID", visible=False)
                                edit_title_input = gr.Textbox(label="タイトル", placeholder="タイトルを入力してください")
                                edit_author_input = gr.Textbox(label="著者", placeholder="著者名を入力してください")
                                edit_year_input = gr.Number(label="出版年", placeholder="出版年を入力してください", precision=0)
                                edit_genre_input = gr.Textbox(label="ジャンル", placeholder="ジャンルを入力してください")
                                edit_memo_input = gr.Textbox(label="メモ", placeholder="メモを入力してください", lines=3)
                                update_book_btn = gr.Button("本を更新", variant="primary")
                                update_book_output = gr.Textbox(label="結果", interactive=False)

                # 日記の管理タブ
                with gr.TabItem("日記の管理"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("## 本の選択")
                            book_dropdown = gr.Dropdown(label="本を選択", choices=[], interactive=True)
                            refresh_dropdown_btn = gr.Button("本の一覧を更新", variant="secondary")

                            gr.Markdown("## 日記の追加")
                            with gr.Group():
                                diary_date_input = gr.Textbox(
                                    label="日付",
                                    placeholder="YYYY-MM-DD",
                                    value=datetime.now().strftime(Diary.DATE_FORMAT),
                                )
                                diary_content_input = gr.Textbox(
                                    label="内容", placeholder="日記の内容を入力してください", lines=5
                                )
                                add_diary_btn = gr.Button("日記を追加", variant="primary")
                                add_diary_output = gr.Textbox(label="結果", interactive=False)

                            gr.Markdown("## 日記の検索")
                            with gr.Group():
                                diary_search_input = gr.Textbox(
                                    label="検索キーワード", placeholder="検索キーワードを入力してください"
                                )
                                diary_search_btn = gr.Button("検索", variant="secondary")

                        with gr.Column(scale=2):
                            gr.Markdown("## 日記の一覧")
                            diaries_table = gr.Dataframe(
                                headers=["ID", "日付", "内容"],
                                datatype=["str", "str", "str"],
                                row_count=10,
                                col_count=(3, "fixed"),
                                interactive=False,
                            )

                            with gr.Row():
                                refresh_diaries_btn = gr.Button("一覧を更新", variant="secondary")
                                delete_diary_btn = gr.Button("選択した日記を削除", variant="stop")

                            gr.Markdown("## 日記の編集")
                            with gr.Group():
                                edit_diary_id = gr.Textbox(label="日記のID", visible=False)
                                edit_diary_date_input = gr.Textbox(
                                    label="日付", placeholder="YYYY-MM-DD"
                                )
                                edit_diary_content_input = gr.Textbox(
                                    label="内容", placeholder="日記の内容を入力してください", lines=5
                                )
                                update_diary_btn = gr.Button("日記を更新", variant="primary")
                                update_diary_output = gr.Textbox(label="結果", interactive=False)

            # イベントハンドラの設定
            # 本の管理
            add_book_btn.click(
                fn=self.add_book_ui,
                inputs=[title_input, author_input, year_input, genre_input, memo_input],
                outputs=add_book_output,
                triggers=[refresh_books_btn.click],
            )

            refresh_books_btn.click(
                fn=self.get_book_list_ui,
                inputs=[],
                outputs=books_table,
            )

            search_btn.click(
                fn=self.search_books_ui,
                inputs=[search_input],
                outputs=books_table,
            )

            delete_book_btn.click(
                fn=self.delete_book_ui,
                inputs=[books_table],
                outputs=[books_table, book_dropdown],
                triggers=[refresh_dropdown_btn.click],
            )

            # 本の選択時に編集フォームに値を設定
            books_table.select(
                fn=self.select_book_ui,
                inputs=[books_table],
                outputs=[
                    edit_book_id,
                    edit_title_input,
                    edit_author_input,
                    edit_year_input,
                    edit_genre_input,
                    edit_memo_input,
                ],
            )

            update_book_btn.click(
                fn=self.update_book_ui,
                inputs=[
                    edit_book_id,
                    edit_title_input,
                    edit_author_input,
                    edit_year_input,
                    edit_genre_input,
                    edit_memo_input,
                ],
                outputs=[update_book_output, books_table, book_dropdown],
                triggers=[refresh_dropdown_btn.click],
            )

            # 日記の管理
            refresh_dropdown_btn.click(
                fn=self.get_book_dropdown_ui,
                inputs=[],
                outputs=book_dropdown,
            )

            book_dropdown.change(
                fn=self.get_diary_list_ui,
                inputs=[book_dropdown],
                outputs=diaries_table,
            )

            add_diary_btn.click(
                fn=self.add_diary_ui,
                inputs=[book_dropdown, diary_date_input, diary_content_input],
                outputs=add_diary_output,
                triggers=[
                    lambda: self.get_diary_list_ui(book_dropdown.value),
                    lambda: diary_content_input.update(""),
                ],
            )

            refresh_diaries_btn.click(
                fn=self.get_diary_list_ui,
                inputs=[book_dropdown],
                outputs=diaries_table,
            )

            diary_search_btn.click(
                fn=self.search_diaries_ui,
                inputs=[book_dropdown, diary_search_input],
                outputs=diaries_table,
            )

            delete_diary_btn.click(
                fn=self.delete_diary_ui,
                inputs=[diaries_table],
                outputs=diaries_table,
            )

            # 日記の選択時に編集フォームに値を設定
            diaries_table.select(
                fn=self.select_diary_ui,
                inputs=[diaries_table],
                outputs=[edit_diary_id, edit_diary_date_input, edit_diary_content_input],
            )

            update_diary_btn.click(
                fn=self.update_diary_ui,
                inputs=[edit_diary_id, edit_diary_date_input, edit_diary_content_input],
                outputs=[update_diary_output, diaries_table],
            )

            # 初期データの読み込み
            interface.load(
                fn=self.get_book_list_ui,
                inputs=[],
                outputs=books_table,
            )

            interface.load(
                fn=self.get_book_dropdown_ui,
                inputs=[],
                outputs=book_dropdown,
            )

        self.interface = interface
        return interface

    def add_book_ui(
        self, title: str, author: str, published_year: int, genre: str, memo: str
    ) -> str:
        """本を追加するUI関数。

        Args:
            title: タイトル
            author: 著者
            published_year: 出版年
            genre: ジャンル
            memo: メモ

        Returns:
            処理結果のメッセージ
        """
        if not title or not author or not published_year:
            return "タイトル、著者、出版年は必須です。"

        try:
            published_year = int(published_year)
            book = Book(title=title, author=author, published_year=published_year, genre=genre, memo=memo)
            self.book_manager.add_book(book)
            return f"本「{title}」を登録しました。"
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"

    def update_book_ui(
        self,
        book_id: str,
        title: str,
        author: str,
        published_year: int,
        genre: str,
        memo: str,
    ) -> Tuple[str, List[List[Any]], List[Tuple[str, str]]]:
        """本を更新するUI関数。

        Args:
            book_id: 本のID
            title: タイトル
            author: 著者
            published_year: 出版年
            genre: ジャンル
            memo: メモ

        Returns:
            処理結果のメッセージ、更新された本の一覧、更新された本のドロップダウン
        """
        if not book_id:
            return "本が選択されていません。", self.get_book_list_ui(), self.get_book_dropdown_ui()

        if not title or not author or not published_year:
            return "タイトル、著者、出版年は必須です。", self.get_book_list_ui(), self.get_book_dropdown_ui()

        try:
            published_year = int(published_year)
            book = Book(
                title=title,
                author=author,
                published_year=published_year,
                genre=genre,
                memo=memo,
                book_id=book_id,
            )
            if self.book_manager.update_book(book):
                return (
                    f"本「{title}」を更新しました。",
                    self.get_book_list_ui(),
                    self.get_book_dropdown_ui(),
                )
            else:
                return "本の更新に失敗しました。", self.get_book_list_ui(), self.get_book_dropdown_ui()
        except Exception as e:
            return f"エラーが発生しました: {str(e)}", self.get_book_list_ui(), self.get_book_dropdown_ui()

    def delete_book_ui(
        self, books_table: List[List[Any]]
    ) -> Tuple[List[List[Any]], List[Tuple[str, str]]]:
        """本を削除するUI関数。

        Args:
            books_table: 本の一覧テーブル

        Returns:
            更新された本の一覧、更新された本のドロップダウン
        """
        if not books_table or not books_table.selected_rows:
            return self.get_book_list_ui(), self.get_book_dropdown_ui()

        try:
            selected_row = books_table.selected_rows[0]
            book_id = selected_row[0]
            self.book_manager.delete_book(book_id)
            return self.get_book_list_ui(), self.get_book_dropdown_ui()
        except Exception as e:
            print(f"Error deleting book: {e}")
            return self.get_book_list_ui(), self.get_book_dropdown_ui()

    def get_book_list_ui(self) -> List[List[Any]]:
        """本の一覧を取得するUI関数。

        Returns:
            本の一覧データ
        """
        books = self.book_manager.get_all_books()
        return [
            [book.id, book.title, book.author, book.published_year, book.genre, book.memo]
            for book in books
        ]

    def search_books_ui(self, query: str) -> List[List[Any]]:
        """本を検索するUI関数。

        Args:
            query: 検索クエリ

        Returns:
            検索結果の本の一覧データ
        """
        if not query:
            return self.get_book_list_ui()

        books = self.book_manager.search_books(query)
        return [
            [book.id, book.title, book.author, book.published_year, book.genre, book.memo]
            for book in books
        ]

    def select_book_ui(
        self, books_table: List[List[Any]]
    ) -> Tuple[str, str, str, int, str, str]:
        """本を選択したときに編集フォームに値を設定するUI関数。

        Args:
            books_table: 本の一覧テーブル

        Returns:
            選択された本の情報（ID、タイトル、著者、出版年、ジャンル、メモ）
        """
        if not books_table or not books_table.selected_rows:
            return "", "", "", 0, "", ""

        selected_row = books_table.selected_rows[0]
        return selected_row[0], selected_row[1], selected_row[2], selected_row[3], selected_row[4], selected_row[5]

    def get_book_dropdown_ui(self) -> List[Tuple[str, str]]:
        """本のドロップダウンリストを取得するUI関数。

        Returns:
            本のドロップダウンリスト（IDとタイトルのタプルのリスト）
        """
        books = self.book_manager.get_all_books()
        return [(book.id, f"{book.title} by {book.author}") for book in books]

    def add_diary_ui(self, book_id: str, date_str: str, content: str) -> str:
        """日記を追加するUI関数。

        Args:
            book_id: 本のID
            date_str: 日記の日付（文字列形式）
            content: 日記の内容

        Returns:
            処理結果のメッセージ
        """
        if not book_id:
            return "本が選択されていません。"

        if not content:
            return "内容は必須です。"

        try:
            date = datetime.strptime(date_str, Diary.DATE_FORMAT)
            diary = Diary(book_id=book_id, content=content, date=date)
            self.book_manager.add_diary(diary)
            return "日記を追加しました。"
        except ValueError:
            return "日付の形式が正しくありません。YYYY-MM-DD形式で入力してください。"
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"

    def update_diary_ui(
        self, diary_id: str, date_str: str, content: str
    ) -> Tuple[str, List[List[Any]]]:
        """日記を更新するUI関数。

        Args:
            diary_id: 日記のID
            date_str: 日記の日付（文字列形式）
            content: 日記の内容

        Returns:
            処理結果のメッセージ、更新された日記の一覧
        """
        if not diary_id:
            return "日記が選択されていません。", []

        if not content:
            return "内容は必須です。", []

        try:
            diary = self.book_manager.get_diary(diary_id)
            if not diary:
                return "指定された日記が見つかりません。", []

            date = datetime.strptime(date_str, Diary.DATE_FORMAT)
            updated_diary = Diary(
                book_id=diary.book_id, content=content, date=date, diary_id=diary_id
            )
            if self.book_manager.update_diary(updated_diary):
                return "日記を更新しました。", self.get_diary_list_ui(diary.book_id)
            else:
                return "日記の更新に失敗しました。", []
        except ValueError:
            return "日付の形式が正しくありません。YYYY-MM-DD形式で入力してください。", []
        except Exception as e:
            return f"エラーが発生しました: {str(e)}", []

    def delete_diary_ui(self, diaries_table: List[List[Any]]) -> List[List[Any]]:
        """日記を削除するUI関数。

        Args:
            diaries_table: 日記の一覧テーブル

        Returns:
            更新された日記の一覧
        """
        if not diaries_table or not diaries_table.selected_rows:
            return diaries_table

        try:
            selected_row = diaries_table.selected_rows[0]
            diary_id = selected_row[0]
            diary = self.book_manager.get_diary(diary_id)
            if diary:
                self.book_manager.delete_diary(diary_id)
                return self.get_diary_list_ui(diary.book_id)
            return diaries_table
        except Exception as e:
            print(f"Error deleting diary: {e}")
            return diaries_table

    def get_diary_list_ui(self, book_id: str) -> List[List[Any]]:
        """指定した本の日記一覧を取得するUI関数。

        Args:
            book_id: 本のID

        Returns:
            日記の一覧データ
        """
        if not book_id:
            return []

        diaries = self.book_manager.get_diaries_for_book(book_id)
        return [[diary.id, diary.date.strftime(Diary.DATE_FORMAT), diary.content] for diary in diaries]

    def search_diaries_ui(self, book_id: str, query: str) -> List[List[Any]]:
        """日記を検索するUI関数。

        Args:
            book_id: 本のID
            query: 検索クエリ

        Returns:
            検索結果の日記の一覧データ
        """
        if not book_id:
            return []

        if not query:
            return self.get_diary_list_ui(book_id)

        diaries = self.book_manager.search_diaries(book_id, query)
        return [[diary.id, diary.date.strftime(Diary.DATE_FORMAT), diary.content] for diary in diaries]

    def select_diary_ui(
        self, diaries_table: List[List[Any]]
    ) -> Tuple[str, str, str]:
        """日記を選択したときに編集フォームに値を設定するUI関数。

        Args:
            diaries_table: 日記の一覧テーブル

        Returns:
            選択された日記の情報（ID、日付、内容）
        """
        if not diaries_table or not diaries_table.selected_rows:
            return "", "", ""

        selected_row = diaries_table.selected_rows[0]
        return selected_row[0], selected_row[1], selected_row[2]

    def run(self, share: bool = False) -> None:
        """アプリケーションを実行する。

        Args:
            share: Gradioの共有リンクを生成するかどうか
        """
        if not self.interface:
            self.create_ui()
        self.interface.launch(share=share)
