import psycopg2


def create_db(connection):
    cur = connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(user_id SERIAL PRIMARY KEY,
        last_name VARCHAR(80) NOT NULL,
        first_name VARCHAR(80) NOT NULL,
        email VARCHAR(128) UNIQUE NOT NULL);
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
        phone_id SERIAL PRIMARY KEY,
        phone_number BIGINT NOT NULL);
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS userphone(
        id SERIAL PRIMARY KEY,
        id_ph INTEGER NOT NULL REFERENCES phone(phone_id),
        id_user INTEGER NOT NULL REFERENCES client(user_id));
    """)
    cur.close()
    connection.commit()
    print('Таблицы успешно созданы')


def add_client(conn, l_name, f_name, mail, phonenum=None):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO client(last_name, first_name, email) VALUES(%s,%s,%s) RETURNING user_id;
    """, (l_name, f_name, mail))
    a = cur.fetchone()
    cur = conn.cursor()
    if type(phonenum) == int:
        print(phonenum)
        cur.execute("""INSERT INTO phone(phone_number) VALUES(%d) RETURNING phone_id;""" % (phonenum))
        b = cur.fetchone()
        cur.execute("""INSERT INTO userphone(id_ph, id_user) VALUES(%d,%d);""" % (b[0], a[0]))
    cur.close()
    conn.commit()
    print('Запись создана')


def add_phone(conn, client_id, phonenum):
    cur = conn.cursor()
    cur.execute("""INSERT INTO phone(phone_number) VALUES(%d) RETURNING phone_id;""" % (phonenum))
    a = cur.fetchone()
    cur.execute("""INSERT INTO userphone(id_ph, id_user) VALUES(%d,%d);""" % (a[0], client_id))
    cur.close()
    conn.commit()
    print('Запись создана')


def change_client(conn, client_id, l_name=None, f_name=None, mail=None):
    cur = conn.cursor()
    cur.execute("""SELECT last_name FROM client
        WHERE user_id = %d;""" % (client_id))
    a = cur.fetchone()
    cur.execute("""SELECT first_name FROM client
            WHERE user_id = %d;""" % (client_id))
    b = cur.fetchone()
    cur.execute("""SELECT email FROM client
                WHERE user_id = %d;""" % (client_id))
    c = cur.fetchone()
    if type(l_name) == str:
        a = l_name
        cur.execute("""UPDATE client SET last_name = %s WHERE user_id = %s;""", (a, client_id))
    if type(f_name) == str:
        b = f_name
        cur.execute("""UPDATE client SET first_name = %s WHERE user_id = %s;""", (b, client_id))
    if type(mail) == str:
        c = mail
        cur.execute("""UPDATE client SET email = %s WHERE user_id = %s;""", (c, client_id))
    cur.close()
    conn.commit()
    print('Запись скорректирована!')


def phone_delete(conn, client_id, phonenum):
    cur = conn.cursor()
    cur.execute("""
    SELECT phone_id FROM phone WHERE phone_number =%d""" % (phonenum))
    a = cur.fetchone()
    cur.execute("""
    DELETE  FROM userphone WHERE id_ph = %d""" % (a[0]))
    cur.execute("""
    DELETE FROM phone WHERE phone_id = %d""" % (a[0]))
    cur.close()
    conn.commit()
    print('Номер удален!')


def client_delete(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
    DELETE  FROM userphone WHERE id_user = %d""" % (client_id))
    cur.execute("""
    DELETE FROM client WHERE user_id = %d""" % (client_id))
    cur.close()
    conn.commit()
    print('Клиент удален!')


def find_client(conn, l_name=None, f_name=None, mail=None, phonenum=None):
    cur = conn.cursor()
    a = 'Не найдено'
    if type(l_name) == str:
        print('Y')
        cur.execute("""
        SELECT user_id,last_name,first_name,e-mail FROM client WHERE last_name =%s;""",(l_name))
        a = cur.fetchone()
        print(a)





with psycopg2.connect(database="client_db", user="postgres", password="19derParol83") as conn:

    # создаем таблицы
    # create_db(conn)

    # Заполнение таблицы 'клиент' и при наличии телефон:
    # l_name = 'Иванов'
    # f_name = 'Иоанн'
    # mail = 'random@mail.ru'
    # phonenum = 89199997707
    # add_client(conn, 'Иванов', 'Иоанн', 'random@mail.ru', 89199997707)

    # Добавление телефона:
    # client_id = 1
    # phonenum = 89199997779
    # add_phone(conn, 1, 89199997779)

    # Изменение данных клиента:
    # client_id = 1
    # l_name = 'Иванов'
    # f_name = 'Иван'
    # mail = 'notrandom@mail.ru'
    # change_client(conn, 1, 'Иванов', 'Иван' , 'notrandom@mail.ru')

    # Удаление телефона
    # phone_delete(conn, 1, 89199997779)

    # Удаление клиента
    # client_delete(conn, 1)


    # find_client(conn)
    l_name = 'Иванов'
    cur=conn.cursor()
    cur.execute("""
    SELECT * FROM client WHERE last_name = 'Иванов' """)
    print(cur.fetchall())
conn.close()
