# 読書管理アプリ 設計書

## 要件定義書

### アプリケーションの目的
- 読書管理と読書日記の記録を行うアプリケーション
- ユーザーが読んだ本の情報を管理し、それに対する日記をつけられるようにする

### 主な機能要件
1. 本の登録・管理機能
   - タイトル、著者、出版年などの基本情報を登録できる
   - 登録した本の情報を編集・削除できる
   - 登録した本の一覧を表示できる

2. 読書日記機能
   - 特定の本に対して日記を記録できる
   - 日付、内容を記録できる
   - 過去の日記を閲覧できる
   - 日記を編集・削除できる

### 技術的要件
- GUIはStreamlitを使用して実装する
- データはJSONファイルに保存する
- Pythonで実装する

## 設計書（概略）

### アプリケーション構成
アプリケーションは以下の2つの主要部分から構成されます：
1. データ管理部分：本と日記のデータを管理するクラス群
2. GUI部分：Streamlitを使用したユーザーインターフェース

### データフロー
1. ユーザーがGUI経由で入力（本の登録、日記の追加など）
2. 入力データがデータ管理クラスに渡される
3. データ管理クラスがデータを処理し、JSONファイルに保存
4. 保存されたデータがGUI経由でユーザーに表示される

## 設計書（機能）

### 本の登録・管理機能
- 本の登録：タイトル、著者、出版年、ジャンル、メモなどの情報を入力して登録
- 本の編集：登録済みの本の情報を編集
- 本の削除：登録済みの本を削除
- 本の一覧表示：登録されている本の一覧を表示
- 本の検索：タイトルや著者などで本を検索

### 読書日記機能
- 日記の追加：特定の本に対して日付と内容を入力して日記を追加
- 日記の編集：登録済みの日記を編集
- 日記の削除：登録済みの日記を削除
- 日記の一覧表示：特定の本に対する日記の一覧を表示
- 日記の検索：日付や内容で日記を検索

## 設計書（クラス構成）

### Book クラス
本の情報を管理するクラス

**属性**
- id: str - 本の一意識別子
- title: str - タイトル
- author: str - 著者
- published_year: int - 出版年
- genre: str - ジャンル
- memo: str - メモ

**メソッド**
- to_dict(): dict - 本の情報を辞書形式で返す
- from_dict(data: dict): Book - 辞書から本のオブジェクトを生成する

### Diary クラス
日記の情報を管理するクラス

**属性**
- id: str - 日記の一意識別子
- book_id: str - 関連する本のID
- date: datetime - 日記の日付
- content: str - 日記の内容

**メソッド**
- to_dict(): dict - 日記の情報を辞書形式で返す
- from_dict(data: dict): Diary - 辞書から日記のオブジェクトを生成する

### BookManager クラス
本と日記のデータを管理するクラス

**属性**
- books: Dict[str, Book] - 本のIDをキーとした本のオブジェクトの辞書
- diaries: Dict[str, List[Diary]] - 本のIDをキーとした日記のリストの辞書
- data_file: str - データを保存するJSONファイルのパス

**メソッド**
- add_book(book: Book): str - 本を追加し、IDを返す
- update_book(book: Book): bool - 本の情報を更新する
- delete_book(book_id: str): bool - 本を削除する
- get_book(book_id: str): Book - 指定したIDの本を取得する
- get_all_books(): List[Book] - すべての本のリストを取得する
- search_books(query: str): List[Book] - クエリに一致する本のリストを取得する
- add_diary(diary: Diary): str - 日記を追加し、IDを返す
- update_diary(diary: Diary): bool - 日記の情報を更新する
- delete_diary(diary_id: str): bool - 日記を削除する
- get_diary(diary_id: str): Diary - 指定したIDの日記を取得する
- get_diaries_for_book(book_id: str): List[Diary] - 指定した本のすべての日記のリストを取得する
- search_diaries(book_id: str, query: str): List[Diary] - 指定した本の中でクエリに一致する日記のリストを取得する
- save_data(): bool - データをJSONファイルに保存する
- load_data(): bool - JSONファイルからデータを読み込む

### StreamlitUI クラス
Streamlitを使用したGUIを提供するクラス

**属性**
- book_manager: BookManager - 本と日記のデータを管理するオブジェクト

**メソッド**
- run(): None - アプリケーションを実行する
- _render_book_management(): None - 本の管理画面を表示する
- _render_diary_management(): None - 日記の管理画面を表示する
