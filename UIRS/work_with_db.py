# Файловая база данных SQL, которая поставляется в комплекте с Python и
# может использоваться в приложениях Python, устраняя необходимость
# устанавливать дополнительное программное обеспечение
import sqlite3

# Класс, в котором описаны методы взаимодействия с базой данных "bot_news"
class DataBaseWork:
    connector = ''

    # Создание базы данных "bot_news"(если еще не была создана)
    # и установка связи с ней
    def create_db(self):
        self.connector = sqlite3.connect('bot_news.db')

    # Создание таблицы "users" с атрибутами "user_id" и "user_name"
    def create_table_users(self):
        with self.connector:
            self.connector.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT,
                        rgru_received BOOLEAN,
                        primeru_received BOOLEAN,
                        vedomosti_received BOOLEAN
                    );
                """)

    # Создание таблицы "news" с атрибутами "header", "time", "url"
    def create_table_news(self):
        with self.connector:
            self.connector.execute("""
                    CREATE TABLE IF NOT EXISTS news(
                        site_name TEXT PRIMARY KEY,
                        header TEXT,
                        time TEXT,
                        url TEXT
                    );
                """)

    # Удаление таблицы
    def delete_table(self, name_table):
        with self.connector:
            self.connector.execute(f"""DROP TABLE IF EXISTS {name_table};""")

    # Добавление пользователя в таблицу "users"
    def add_user_in_users_table(self, user_id, user_name):
        with self.connector:
            self.connector.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?);", [user_id, user_name, False, False, False])

    # Добавление новости в таблицу "news"
    def add_news_in_news_table(self,site_name, header, time, url):
        with self.connector:
            self.connector.execute(f"INSERT INTO news VALUES(?, ?, ?, ?);", [site_name, header, time, url])

    # Удаление пользователя из таблицы "users"
    def delete_user_from_users_table(self, user_id):
        with self.connector:
            self.connector.execute(f"DELETE FROM users WHERE user_id = {user_id}")

    # Удаление новости из таблицы "news"
    def delete_news_from_news_table(self, site_name):
        with self.connector:
            self.connector.execute(f"DELETE FROM news WHERE site_name = '{site_name}'")

    # Проверка на существование пользователя в таблице "users"
    def is_exist_user_in_db(self, user_id):
        try:
            with self.connector:
                current_id = self.connector.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}").fetchone()[0]
                return True
        except:
            return False

    # Проверка на существование новости в таблице "news"
    def is_exist_news_in_db(self, site_name, header):
        try: # Проверка на совпадение источника и заголовка
            with self.connector:
                current_site_name = self.connector.execute(
                    f"SELECT site_name FROM news WHERE site_name = '{site_name}' AND header = '{header}'").fetchone()[0]

                return 0
        except:
            pass

        try: # Проверка на собвпадение источника
            with self.connector:
                current_site_name = self.connector.execute(
                    f"SELECT site_name FROM news WHERE site_name = '{site_name}'").fetchone()[0]

                return 1
        except:
            pass

        return 2

    # Получение новости из таблицы "news"
    def getting_news_from_db(self, name):
        data = self.connector.execute(f"SELECT * FROM news WHERE site_name = '{name}'")
        return data.fetchone()
    # Обновление значения "получил пользователь с конкретного источника новость"
    def update_received_news_for_current_user(self, user_id, update_perem, bool_value):
        with self.connector:
            update = self.connector.execute(
                f"UPDATE users SET {update_perem} = ? WHERE user_id = ?", (bool_value, user_id))

    # Обновление значения "получили пользователи с конкретного источника новость"
    def update_received_news_for_all_users(self, sourse_name, bool_value):
        with self.connector:
            update = self.connector.execute(f"UPDATE users SET {sourse_name} = ?", (bool_value,))

    # Проверка на факт получения новости пользователем с конкретного источника
    def is_user_received_current_news(self, user_id, soure_name):
        data = self.connector.execute(f"SELECT {soure_name} FROM users WHERE user_id = '{user_id}'")
        return data.fetchone()[0]

if __name__ == "__main__":
    db = DataBaseWork()
    db.create_db()

    print(db.is_user_received_current_news(817688918, 'primeru_received'))