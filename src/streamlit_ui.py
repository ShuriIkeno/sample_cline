#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書管理アプリのGUIを定義するモジュール。

このモジュールでは、読書管理アプリのGUIを提供するStreamlitUIクラスを定義しています。
"""

import os
from datetime import datetime, time
from typing import Dict, List, Any, Tuple, Optional

import streamlit as st

from models import Book, Diary
from book_manager import BookManager


class StreamlitUI:
    """Streamlitを使用したGUIを提供するクラス。

    このクラスは、Streamlitを使用して読書管理アプリのGUIを提供します。

    Attributes:
        book_manager: 本と日記のデータを管理するオブジェクト
    """

    def __init__(self, book_manager: BookManager):
        """StreamlitUIクラスのコンストラクタ。

        Args:
            book_manager: 本と日記のデータを管理するオブジェクト
        """
        self.book_manager = book_manager

    def run(self) -> None:
        """アプリケーションを実行する。"""
        st.set_page_config(
            page_title="読書管理アプリ",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        st.title("読書管理アプリ")

        # サイドバーにタブ選択を表示
        tab = st.sidebar.radio("メニュー", ["本の管理", "日記の管理"])

        if tab == "本の管理":
            self._render_book_management()
        else:
            self._render_diary_management()

    def _render_book_management(self) -> None:
        """本の管理画面を表示する。"""
        st.header("本の管理")

        # 本の一覧と操作を2カラムに分ける
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("本の一覧")
            books = self.book_manager.get_all_books()
            if books:
                # 本の一覧をデータフレームで表示
                book_data = {
                    "ID": [],
                    "タイトル": [],
                    "著者": [],
                    "出版年": [],
                    "ジャンル": [],
                    "メモ": [],
                }
                for book in books:
                    book_data["ID"].append(book.id)
                    book_data["タイトル"].append(book.title)
                    book_data["著者"].append(book.author)
                    book_data["出版年"].append(book.published_year)
                    book_data["ジャンル"].append(book.genre)
                    book_data["メモ"].append(book.memo)

                book_df = st.dataframe(book_data, use_container_width=True)

                # 本の選択
                selected_book_id = st.selectbox(
                    "編集または削除する本を選択",
                    options=[book.id for book in books],
                    format_func=lambda x: next((f"{b.title} by {b.author}" for b in books if b.id == x), x),
                )

                if selected_book_id:
                    selected_book = self.book_manager.get_book(selected_book_id)
                    if selected_book:
                        # 選択した本の操作
                        operation = st.radio("操作を選択", ["編集", "削除"])
                        
                        if operation == "編集":
                            with st.form("edit_book_form"):
                                st.subheader("本の編集")
                                edit_title = st.text_input("タイトル", value=selected_book.title)
                                edit_author = st.text_input("著者", value=selected_book.author)
                                edit_year = st.number_input("出版年", value=selected_book.published_year, min_value=0, max_value=3000)
                                edit_genre = st.text_input("ジャンル", value=selected_book.genre)
                                edit_memo = st.text_area("メモ", value=selected_book.memo)
                                
                                submit_edit = st.form_submit_button("更新")
                                
                                if submit_edit:
                                    if edit_title and edit_author and edit_year:
                                        updated_book = Book(
                                            title=edit_title,
                                            author=edit_author,
                                            published_year=int(edit_year),
                                            genre=edit_genre,
                                            memo=edit_memo,
                                            book_id=selected_book_id,
                                        )
                                        if self.book_manager.update_book(updated_book):
                                            st.success(f"本「{edit_title}」を更新しました。")
                                            st.rerun()
                                        else:
                                            st.error("本の更新に失敗しました。")
                                    else:
                                        st.error("タイトル、著者、出版年は必須です。")
                        
                        elif operation == "削除":
                            if st.button(f"「{selected_book.title}」を削除", type="primary"):
                                if self.book_manager.delete_book(selected_book_id):
                                    st.success(f"本「{selected_book.title}」を削除しました。")
                                    st.rerun()
                                else:
                                    st.error("本の削除に失敗しました。")
            else:
                st.info("登録されている本はありません。")

            # 本の検索
            st.subheader("本の検索")
            search_query = st.text_input("検索キーワード")
            if search_query:
                search_results = self.book_manager.search_books(search_query)
                if search_results:
                    search_data = {
                        "ID": [],
                        "タイトル": [],
                        "著者": [],
                        "出版年": [],
                        "ジャンル": [],
                        "メモ": [],
                    }
                    for book in search_results:
                        search_data["ID"].append(book.id)
                        search_data["タイトル"].append(book.title)
                        search_data["著者"].append(book.author)
                        search_data["出版年"].append(book.published_year)
                        search_data["ジャンル"].append(book.genre)
                        search_data["メモ"].append(book.memo)

                    st.dataframe(search_data, use_container_width=True)
                else:
                    st.info(f"「{search_query}」に一致する本は見つかりませんでした。")

        with col2:
            st.subheader("本の登録")
            with st.form("add_book_form"):
                title = st.text_input("タイトル")
                author = st.text_input("著者")
                year = st.number_input("出版年", min_value=0, max_value=3000, value=datetime.now().year)
                genre = st.text_input("ジャンル")
                memo = st.text_area("メモ")
                
                submit = st.form_submit_button("登録")
                
                if submit:
                    if title and author and year:
                        book = Book(
                            title=title,
                            author=author,
                            published_year=int(year),
                            genre=genre,
                            memo=memo,
                        )
                        self.book_manager.add_book(book)
                        st.success(f"本「{title}」を登録しました。")
                        st.rerun()
                    else:
                        st.error("タイトル、著者、出版年は必須です。")

    def _render_diary_management(self) -> None:
        """日記の管理画面を表示する。"""
        st.header("日記の管理")

        # 本の選択
        books = self.book_manager.get_all_books()
        if not books:
            st.warning("本が登録されていません。先に本を登録してください。")
            return

        book_options = {f"{book.title} by {book.author}": book.id for book in books}
        selected_book_name = st.selectbox("本を選択", options=list(book_options.keys()))
        selected_book_id = book_options[selected_book_name]
        selected_book = self.book_manager.get_book(selected_book_id)

        if selected_book:
            # 日記の一覧と操作を2カラムに分ける
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader(f"「{selected_book.title}」の日記一覧")
                diaries = self.book_manager.get_diaries_for_book(selected_book_id)
                
                if diaries:
                    # 日記の一覧をデータフレームで表示
                    diary_data = {
                        "ID": [],
                        "日付": [],
                        "内容": [],
                    }
                    for diary in diaries:
                        diary_data["ID"].append(diary.id)
                        diary_data["日付"].append(diary.date.strftime(Diary.DATE_FORMAT))
                        diary_data["内容"].append(diary.content)

                    diary_df = st.dataframe(diary_data, use_container_width=True)

                    # 日記の選択
                    selected_diary_id = st.selectbox(
                        "編集または削除する日記を選択",
                        options=[diary.id for diary in diaries],
                        format_func=lambda x: next((f"{d.date.strftime(Diary.DATE_FORMAT)}: {d.content[:30]}..." for d in diaries if d.id == x), x),
                    )

                    if selected_diary_id:
                        selected_diary = self.book_manager.get_diary(selected_diary_id)
                        if selected_diary:
                            # 選択した日記の操作
                            operation = st.radio("操作を選択", ["編集", "削除"], key="diary_operation")
                            
                            if operation == "編集":
                                with st.form("edit_diary_form"):
                                    st.subheader("日記の編集")
                                    edit_date = st.date_input(
                                        "日付",
                                        value=selected_diary.date,
                                    )
                                    edit_content = st.text_area("内容", value=selected_diary.content, height=200)
                                    
                                    submit_edit = st.form_submit_button("更新")
                                    
                                    if submit_edit:
                                        if edit_content:
                                            updated_diary = Diary(
                                                book_id=selected_book_id,
                                                content=edit_content,
                                                date=datetime.combine(edit_date, time.min),
                                                diary_id=selected_diary_id,
                                            )
                                            if self.book_manager.update_diary(updated_diary):
                                                st.success("日記を更新しました。")
                                                st.rerun()
                                            else:
                                                st.error("日記の更新に失敗しました。")
                                        else:
                                            st.error("内容は必須です。")
                            
                            elif operation == "削除":
                                if st.button(f"{selected_diary.date.strftime(Diary.DATE_FORMAT)}の日記を削除", type="primary"):
                                    if self.book_manager.delete_diary(selected_diary_id):
                                        st.success("日記を削除しました。")
                                        st.rerun()
                                    else:
                                        st.error("日記の削除に失敗しました。")
                else:
                    st.info(f"「{selected_book.title}」の日記はまだありません。")

                # 日記の検索
                st.subheader("日記の検索")
                search_query = st.text_input("検索キーワード", key="diary_search")
                if search_query:
                    search_results = self.book_manager.search_diaries(selected_book_id, search_query)
                    if search_results:
                        search_data = {
                            "ID": [],
                            "日付": [],
                            "内容": [],
                        }
                        for diary in search_results:
                            search_data["ID"].append(diary.id)
                            search_data["日付"].append(diary.date.strftime(Diary.DATE_FORMAT))
                            search_data["内容"].append(diary.content)

                        st.dataframe(search_data, use_container_width=True)
                    else:
                        st.info(f"「{search_query}」に一致する日記は見つかりませんでした。")

            with col2:
                st.subheader("日記の追加")
                with st.form("add_diary_form"):
                    date = st.date_input("日付", value=datetime.now())
                    content = st.text_area("内容", height=200)
                    
                    submit = st.form_submit_button("追加")
                    
                    if submit:
                        if content:
                            diary = Diary(
                                book_id=selected_book_id,
                                content=content,
                                date=datetime.combine(date, time.min),
                            )
                            self.book_manager.add_diary(diary)
                            st.success("日記を追加しました。")
                            st.rerun()
                        else:
                            st.error("内容は必須です。")


def main():
    """Streamlitアプリのメイン関数。"""
    import argparse
    
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
    
    book_manager = BookManager(data_file=args.data_file)
    ui = StreamlitUI(book_manager)
    ui.run()


if __name__ == "__main__":
    main()
