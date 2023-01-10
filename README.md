# GPUser

愛媛大学 工学部 人工知能研究室 自然言語処理グループの研究室用の GPU サーバー管理ツールです。

# Features

- 自動更新
- アイコンによる状態表示
- 最終更新日時の表示

# Requirement

- python = "^3.11"
- django = "^4.1.4"
- psycopg2-binary = "^2.9.5"
- paramiko = "^2.12.0"
- apscheduler = "^3.9.1.post1"
- ddjango-cors-headers = "^3.13.0"

# Installation

Poetry を使ってインストールする

```bash
poetry install
```

# Usage

サーバーの起動 (with poetry)

```bash
poetry run server
```

サーバーの起動

```bash
python manage.py runserver
```

データベースの起動 (with docker)
```bash
cp .env.example .env
bash database.sh
```

# Note

初回のみ、http://localhost:8000/admin にアクセスして、Servers にサーバー名を登録する必要があります。

# Author

- 大塚 琢生
- ohtsuka@ai.cs.ehime-u.ac.jp
- 山内洋輝
- /
- 樽本空宙
- /
- 宮田莉奈
- /
