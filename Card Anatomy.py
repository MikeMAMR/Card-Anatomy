import random
import sqlite3
import sys
dataBase = {}
# CREATE DATA BASE card #
# .execute('consulta') Executes some SQL query
# .commit After doing some chance in DB don't forget to commit them
# .fetchone returns the first row from the resonse 
# .fetchall returns all rows from the response 
 
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""
create table card(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);
""")
conn.commit() 

def verificarCard(cad):
    tmp = cad[:(len(cad) - 1)]
    if str(Luhn(tmp)) == cad[len(cad) - 1]:
        return True
    return False
def Luhn(cad):
    arr = {}
    cont = 0
    sum = 0
    for i in cad:
        arr[cont] = int(i)
        cont += 1
    for i in arr:
        if (i+1) % 2 != 0:
            arr[i] = arr[i] * 2
    for i in arr:
        if arr[i] > 9:
            arr[i] = arr[i] - 9
        sum += arr[i]    
    if sum % 10 == 0:
        return 0
    return ((int(sum/10) + 1) * 10) - sum 

def createCard():
    dig = '0123456789'
    card = '400000'
    for i in range(9):
        card += random.choice(dig)
    
    card += str(Luhn(card)) 

    return card

def createPin():
	pin = ''
	dig = '0123456789'
	for i in range(4):
		pin += random.choice(dig)
	return pin
def menu():
	print("1. Create an account")
	print("2. Log into account")
	print("0. Exit")
	
def menuCard():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transder")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


while True :
    menu()
    n = input('>')
    if n == '1':
        print()
        card = createCard()
        pin = createPin()
        # INSERT DATABASE
        cur.execute("insert into card (number, pin) values ('"+card+"', '"+ pin+"');")
        conn.commit()
        #dataBase[card] = pin
        print('Your card has been created')
        print('Your card number:')
        print(card)
        print('Your card PIN:')
        print(pin)
        print()
    elif n == '0' :
        print()
        print('Bye!')
        break
    elif n == '2' :
        print()
        print('Enter your card number:')
        NCard = input('>')
        print('Enter your PIN:')
        NPin = input('>')
        # CHECK
        cur.execute("select * from card where number='"+NCard+"' and pin='"+NPin+"';")
        if cur.fetchone() != None:
            print()
            print('You have successfully logged in!')
            while True:
                print()
                menuCard()
                m = input('>')
                if m == '0':
                    print()
                    print('Bye!')
                    sys.exit()
                elif m == '1':
                    print()
                    cur.execute("select * from card where number='"+NCard+"' and pin='"+NPin+"';")
                    Mtmp = cur.fetchone()
                    print('Balance:', Mtmp[3])
                elif m == '2':
                    #Add money
                    cur.execute("select * from card where number='"+NCard+"' and pin='"+NPin+"';")
                    Mtmp = cur.fetchone()
                    print('Enter income:')
                    money = int(input('>'))
                    money = money + Mtmp[3]
                    sql = "update card set balance="+str(money)+" where id ="+str(Mtmp[0])+";"
                    cur.execute(sql, "")
                    conn.commit()
                    print('Income was added!')
                elif m == '3':
                    #Transfer
                    cur.execute("select * from card where number='"+NCard+"' and pin='"+NPin+"';")
                    Mtmp = cur.fetchone()
                    print()
                    print('Tranfer')
                    print('Enter card number:')
                    OtherCard = input('>')
                    cur.execute("select * from card where number='"+OtherCard+"';")
                    MtmpOther = cur.fetchone()
                    if Mtmp[1] == OtherCard:
                        print("You can't transfer money to the same account")
                    elif verificarCard(OtherCard) == False:
                        print('Probably you made a mistake in the card number. Please try again!')
                    elif MtmpOther == None:
                        print('Such a card does not exist.')
                    else:
                        print('Enter how much money you want to transfer:')
                        nMoney = int(input('>'))
                        if nMoney > Mtmp[3]:
                            print('Not enough money!')
                        else:
                            sql1 = "update card set balance="+str(Mtmp[3] - nMoney)+" where id ="+str(Mtmp[0])+";"
                            sql2 = "update card set balance="+str(MtmpOther[3] + nMoney)+" where id ="+str(MtmpOther[0])+";"
                            cur.execute(sql1,"")
                            cur.execute(sql2,"")
                            conn.commit()
                            print('Success!')
                elif m == '5':
                    print()
                    print('You have successfully logged out!')
                    print()
                    break
                elif m == '4':
                    print()
                    cur.execute("select * from card where number='"+NCard+"' and pin='"+NPin+"';")
                    Mtmp = cur.fetchone()
                    sql = "delete from card where id =" + str(Mtmp[0]) + ";"
                    cur.execute(sql,"")
                    conn.commit()
                    print('The account has been closed!')
                    print()
                    break
        else:
            print()
            print('Wrong card number or PIN!')