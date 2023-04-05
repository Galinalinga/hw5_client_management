import psycopg2
from pprint import pprint


    def create_db(conn):

        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(20),
                last_name VARCHAR(30),
                email VARCHAR(254)
                );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients_phones(
                phone VARCHAR(11) PRIMARY KEY,
                client_id INTEGER REFERENCES client(id)
                );
            """)
        return


    def delete_db(conn):
        cur.execute("""
                DROP TABLE client, clients_phones CASCADE;
                """)



    def add_phone(conn, client_id, phone):
        cur.execute("""
                INSERT INTO clients_phones(phone, client_id)
                VALUES (%s, %s)
                """, (phone, client_id))
        return client_id



    def add_client(conn, first_name=None, last_name=None, email=None, phone=None):
        cur.execute("""
                INSERT INTO client(first_name, last_name, email)
                VALUES (%s, %s, %s)
                """, (first_name, last_name, email))
        cur.execute("""
                SELECT id from client
                ORDER BY id DESC
                LIMIT 1
                """)
        id = cur.fetchone()[0]
        if phone is None:
            return id
        else:
            add_phone(cur, id, phone)
            return id


    def update_client(conn, id, first_name=None, last_name=None, email=None):
        cur.execute("""
                SELECT * FROM client
                WHERE id = %s
                """, (id,))
        info = cur.fetchone()
        if first_name is None:
            first_name = info[1]
        if last_name is None:
            last_name = info[2]
        if email is None:
            email = info[3]
        cur.execute("""
                UPDATE client
                SET first_name = %s, last_name = %s, email =%s 
                where id = %s
                """, (first_name, last_name, email, id))
        return id


    def delete_phone(conn, phone):
        cur.execute("""
                DELETE FROM clients_phones 
                WHERE phone = %s
                """, (phone,))
        return phone


    def delete_client(conn, id):
        cur.execute("""
                DELETE FROM clients_phones
                WHERE client_id = %s
                """, (id,))
        cur.execute("""
                DELETE FROM client
                WHERE id = %s
               """, (id,))
        return id


    def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
        if first_name is None:
            first_name = '%'
        else:
            first_name = '%' + first_name + '%'
        if last_name is None:
            last_name = '%'
        else:
            last_name = '%' + last_name + '%'
        if email is None:
            email = '%'
        else:
            email = '%' + email + '%'
        if phone is None:
            cur.execute("""
                    SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM client c
                    LEFT JOIN clients_phones p ON c.id = p.client_id
                    WHERE c.first_name LIKE %s AND c.last_name LIKE %s
                    AND c.email LIKE %s
                    """, (first_name, last_name, email))
        else:
            cur.execute("""
                    SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM client c
                    LEFT JOIN clients_phones p ON c.id = p.client_id
                    WHERE c.first_name LIKE %s AND c.last_name LIKE %s
                    AND c.email LIKE %s AND p.phone like %s
                    """, (first_name, last_name, email, phone))
        return cur.fetchall()


    if __name__ == '__main__':
    
        with psycopg2.connect(database="client_management", user="postgres", password='12345') as conn:
            with conn.cursor() as cur:
                # Удаление таблиц перед запуском
                delete_db(cur)
                # 1. Cоздание таблиц
                create_db(cur)
                print("БД создана")
                # 2. Добавляем 5 клиентов
                print("Добавлен клиент id: ",
                      add_client(cur, "Иван", "Иванов", "ivan@gmail.com"))
                print("Добавлен клиент id: ",
                      add_client(cur, "Петр", "Петров",
                                    "petr@mail.ru", 79998887766))
                print("Добавлен клиент id: ",
                      add_client(cur, "Алексей", "Алексеев",
                                    "alex@outlook.com", 79997776655))
                print("Добавлен клиент id: ",
                      add_client(cur, "Василий", "Васильев",
                                    "vasil@mail.ru", 79996665544))
                print("Добавлен клиент id: ",
                      add_client(cur, "Сергей", "Сергеев",
                                    "serg@outlook.com"))
                print("Данные в таблицах")
                cur.execute("""
                        SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM client c
                        LEFT JOIN clients_phones p ON c.id = p.client_id
                        ORDER by c.id
                        """)
                pprint(cur.fetchall())
                # 3. Добавляем клиенту номер телефона(одному первый, одному второй)
                print("Телефон добавлен клиенту id: ",
                      add_phone(cur, 2, 79887776655))
                print("Телефон добавлен клиенту id: ",
                      add_phone(cur, 1, 79337776655))

                print("Данные в таблицах")
                cur.execute("""
                        SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM client c
                        LEFT JOIN clients_phones p ON c.id = p.client_id
                        ORDER by c.id
                        """)
                pprint(cur.fetchall())
                # 4. Изменим данные клиента
                print("Изменены данные клиента id: ",
                      update_client(cur, 4, "Иван", None, '123@outlook.com'))
                # 5. Удаляем клиенту номер телефона
                print("Телефон удалён c номером: ",
                      delete_phone(cur, '79337776655'))
                print("Данные в таблицах")
                cur.execute("""
                        SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM client c
                        LEFT JOIN clients_phones p ON c.id = p.client_id
                        ORDER by c.id
                        """)
                pprint(cur.fetchall())
                # 6. Удалим клиента номер 2
                print("Клиент удалён с id: ",
                      delete_client(cur, 2))
                cur.execute("""
                                    SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM client c
                                    LEFT JOIN clients_phones p ON c.id = p.client_id
                                    ORDER by c.id
                                    """)
                pprint(cur.fetchall())
                # 7. Найдём клиента
                print('Найденный клиент по имени:')
                pprint(find_client(cur, 'Иван'))

                print('Найденный клиент по email:')
                pprint(find_client(cur, None, None, 'alex@outlook.com'))

                print('Найденный клиент по имени, фамилии и email:')
                pprint(find_client(cur, "Василий", "Васильев",
                                   'vasil@mail.ru'))

                print('Найденный клиент по имени, фамилии, телефону и email:')
                pprint(find_client(cur, "Петр", "Петров",
                                   "petr@mail.ru", 79998887766))

                print('Найденный клиент по имени, фамилии, телефону:')
                pprint(find_client(cur, None, None, None, '79997776655'))
