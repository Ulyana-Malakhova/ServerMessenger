import sqlite3
import json
import datetime

def nicknameVerification(client):
    global clients
    try:
        msg = client.recv(1024)
    except Exception as e:
        print(f"Error: {e}")
        return False
    else:
        print(f"Message -  {msg}")
        json_msg = json.loads(msg)
        for data in json_msg:
            for key, value in data.items():
                if key=='nickname':
                    nickname = value
                    con = sqlite3.connect('messengerDatabase.db')
                    cursor = con.cursor()
                    cursor.execute('SELECT nickname FROM user WHERE nickname = ?',(nickname,))
                    nicknames = cursor.fetchall()
                    if len(nicknames)!=0:
                        print("Nickname are already using")
                        return False
        clients[client]=nickname
        con.close()
        userRegistration(json_msg)
        return True


def userRegistration(json_msg):
    con = sqlite3.connect('messengerDatabase.db')
    cursor = con.cursor()
    for data in json_msg:
        for key, value in data.items():
            if key=='role_name':
                role_name = value
            if key=='given_name':
                given_name = value
            if key=='family_name':
                family_name = value
            if key=='middle_name':
                middle_name = value
            if key=='nickname':
                nickname = value
            if key=='university_name':
                university_name = value
            if key=='group_name':
                group_name = value
    cursor.execute('SELECT id FROM university WHERE name = ?',(university_name,))
    name_universitys = cursor.fetchall()
    checking_table=0
    if len(name_universitys)!=0:
        id_university=name_universitys
    else:
        cursor.execute('INSERT INTO university (name) VALUES (?)', (university_name,))
        con.commit()
        checking_table+=1
    cursor.execute('SELECT id FROM group WHERE name = ?',(group_name,))
    name_groups = cursor.fetchall()
    if len(name_groups)!=0:
        id_group = name_groups
    else:
        cursor.execute('INSERT INTO group (name) VALUES (?)', (group_name,))
        con.commit()
        checking_table+=2
    if checking_table == 1:
        cursor.execute('SELECT id FROM university WHERE name = ?',(university_name,))
        id_universitys = cursor.fetchone()
        cursor.execute('INSERT INTO university_groups (university_id,group_id) VALUES (?,?)', (id_universitys,id_group,))
        con.commit()
    if checking_table == 2:
        cursor.execute('SELECT id FROM group WHERE name = ?',(group_name,))
        id_groups = cursor.fetchone()
        cursor.execute('INSERT INTO university_groups (university_id,group_id) VALUES (?,?)', (id_university,id_groups,))
        con.commit()
    if checking_table == 3:
        cursor.execute('SELECT id FROM group WHERE name = ?',(group_name,))
        id_groups = cursor.fetchone()
        cursor.execute('SELECT id FROM university WHERE name = ?',(university_name,))
        id_universitys = cursor.fetchone()
        cursor.execute('INSERT INTO university_groups (university_id,group_id) VALUES (?,?)', (id_universitys,id_groups,))
        con.commit()

    cursor.execute('INSERT INTO user (given_name,family_name,middle_name,nickname,isActive) VALUES (?,?,?,?,?)', (given_name,family_name,middle_name,nickname,True,))
    con.commit()
    cursor.execute('SELECT id FROM user WHERE given_name =?,family_name=?,middle_name=?,nickname=?,isActive=?',(given_name,family_name,middle_name,nickname,True,))
    id_user = cursor.fetchone()
    cursor.execute('SELECT id FROM group WHERE name =?',(group_name,))
    id_group = cursor.fetchone()
    cursor.execute('INSERT INTO group_users (group_id,user_id) VALUES (?,?)', (id_user,id_group,))
    con.commit()

    cursor.execute('SELECT id FROM role WHERE name = ?',(role_name,))
    name_role = cursor.fetchall()
    checking_table=0
    if len(name_role)==0:
        cursor.execute('INSERT INTO role (name) VALUES (?)', (role_name,))
        con.commit()
        checking_table+=1
    if checking_table == 1:
        cursor.execute('SELECT id FROM role WHERE name = ?',(role_name,))
        id_roles = cursor.fetchone()
        cursor.execute('INSERT INTO user_role (user_id,role_id) VALUES (?,?)', (id_user,id_roles,))
        con.commit()

def createTable():
    con = sqlite3.connect('messengerDatabase.db')
    cursor = con.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS role (
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      name VARCHAR
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_role (
      user_id INTEGER,
      FOREIGN KEY(user_id) REFERENCES user(id),
      role_id INTEGER,
      FOREIGN KEY(role_id) REFERENCES role(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      given_name VARCHAR,
      family_name VARCHAR,
      middle_name VARCHAR,
      nickname VARCHAR,
      isActive BOOLEAN
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS university (
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      name VARCHAR
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS group (
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      name VARCHAR,
      ts DATETIME
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS message (
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      content VARCHAR,
      user_id INTEGER,
      ts DATETIME
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS group_messages (
      group_id INTEGER,
      FOREIGN KEY(group_id) REFERENCES group(id),
      message_id INTEGER,
      FOREIGN KEY(message_id) REFERENCES message(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS group_users (
      group_id INTEGER,
      FOREIGN KEY(group_id) REFERENCES group(id),
      user_id INTEGER,
      FOREIGN KEY(user_id) REFERENCES user(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_to_user_messages (
      user_recipient_id INTEGER,
      FOREIGN KEY(user_recipient_id) REFERENCES user(id),
      message_id INTEGER,
      FOREIGN KEY(message_id) REFERENCES message(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS university_groups (
      university_id INTEGER,
      FOREIGN KEY(university_id) REFERENCES university(id),
      group_id INTEGER,
      FOREIGN KEY(group_id) REFERENCES group(id)
    );
    ''')
    con.close()

def readingMessage():
    global msg
    global nickname
    global group_name
    global message_content
    global json_msg
    json_msg = json.loads(msg)
    for data in json_msg:
        for key, value in data.items():
            if key=='nickname':
                nickname = value
            if key=='group_name':
                group_name = value
            if key=='message_content':
                message_content = value
    con = sqlite3.connect('messengerDatabase.db')
    cursor = con.cursor()
    cursor.execute('SELECT id FROM group WHERE name = ?', (group_name,))
    group_id = cursor.fetchone()
    cursor.execute('SELECT id FROM user WHERE nickname = ?', (nickname,))
    user_id = cursor.fetchone()
    datetime_now= datetime.datetime.now()
    cursor.execute('INSERT INTO message (content,user_id,ts) VALUES (?,?,?)', (message_content,user_id,datetime_now,))
    con.commit()
    cursor.execute('SELECT id FROM message WHERE content = ? AND user_id= ? AND ts = ?', (message_content,user_id,datetime_now,))
    message_id = cursor.fetchone()
    cursor.execute('INSERT INTO group_message (group_id,message_id) VALUES (?,?)', (group_id,message_id,))
    con.commit()
    con.close()

def sendingMessage():
    global msg
    con = sqlite3.connect('messengerDatabase.db')
    cursor = con.cursor()
    json_msg = json.loads(msg)
    for data in json_msg:
        for key, value in data.items():
            if key=='nickname':
                nickname = value
            if key=='group_name':
                group_name = value
            if key=='message_content':
                message_content = value
    cursor.execute('SELECT id FROM group WHERE name = ?', (group_name,))
    group_id = cursor.fetchone()
    cursor.execute('SELECT user_id FROM group_users WHERE group_id = ?', (group_id,))
    users_id = cursor.fetchall()
    for user in users_id:
        cursor.execute('SELECT nickname FROM user WHERE id = ?', (user,))
        users_nickname = cursor.fetchone()
        for name_socket, nickname_socket in clients:
            if nickname_socket==users_nickname:
                name_socket.send(json_msg)