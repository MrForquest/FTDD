import sqlite3
from data_file import weapons
from game_classes.Game_things import Weapon, Potion


def save(pl):
    con = sqlite3.connect("data/other/save.db")
    cursor = con.cursor()
    cursor.execute(f"""UPDATE saves
                              SET money = {pl.money}""")
    cursor.execute(f"""UPDATE saves
                              SET mana = {pl.mana}""")
    cursor.execute(f"""UPDATE saves
                              SET hp = {pl.hp}""")
    txt = ''
    for i in pl.inventory:
        for j in pl.inventory[i]:
            print(j)
            txt += str(weapons.index(j))
    try:
        cursor.execute(f"""UPDATE saves SET inventory = {int(txt)}""")
    except Exception:
        cursor.execute(f"""UPDATE saves 
                                     SET inventory = {-1}""")
    con.commit()


def sql_load(pl):
    print(weapons)
    con = sqlite3.connect("data/other/save.db")
    cursor = con.cursor()
    data = cursor.execute('SELECT * FROM saves').fetchall()
    pl.hp = data[0][2]
    pl.money = data[0][0]
    pl.mana = data[0][1]
    if data[0][3] != -1:
        for i in str(data[0][3]):
            if isinstance(weapons[int(i)], Weapon):
                pl.inventory['weapons'].append(weapons[int(i)])
            elif isinstance(weapons[int(i)], Potion):
                pl.inventory['magicshit'].append(weapons[int(i)])
