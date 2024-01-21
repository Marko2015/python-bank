# This is a sample Python script.
import csv
import re
import os
import random
import getpass

def acc_Num(dinDev):
    #generise random broj racuna
    segment1 = ''.join(str(random.randint(0, 9)) for _ in range(3))
    segment2 = ''.join(str(random.randint(0, 9)) for _ in range(5))
    if dinDev == 'RSD':
        segment3 = '55'
    else:
        segment3 = '44'
    accNum = f"{segment1}-{segment2}-{segment3}"
    return accNum
def is_valid_email(email):
    #proverava da li je validan email
    pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return re.match(pattern, email)
def does_email_exist(email):
    #proverava da li je vec registrovan email
    with open('data/general/users.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0 and row[1] == email:
                return True
    return False
def does_user_exist(email, password):
    #proverava da li postoji korisnik sa unetim emailom i passworsom i vraca user_id ako postoji
    with open('data/general/users.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        num_of_rows = len(rows)
        if num_of_rows == 1:
            return 0
        for row in rows:
            if len(row) >1 and row[1] == email and row[2] == password:
                user = row[0]
                return user
        return -1
def login():
    #trazi od korisnika email i password i poziva funkciju does_user_exist
    check = -1
    while check == -1:
        while True:
            email = input("Email: ")
            if is_valid_email(email):
                break
            else:
                print("Nepravilan unos. Unesite ispravnu email adresu.")
        password = getpass.getpass("Password: ")
        check = does_user_exist(email, password)
        if check == -1:
            print("Neispravan email ili password. Pokusajte ponovo.")
        elif check == 0:
            print("Morate da napravite nalog prvo.")
            ch = input("Press enter to continue: ")
            user = intro()
            return user
        else:
            return check
    #print("Login successful.")
def get_user_info():
    #vraca podatke od korisnika
    name = input("Ime: ")
    surname = input("Prezime: ")
    phone = input("Broj telefona: ")
    while True:
        email = input("Unesite vasu email adresu: ")
        if is_valid_email(email):
            if does_email_exist(email):
                print("Email vec postoji. Pokusajte ponovo.")
                continue
            else:
                break
        else:
            print("Nepravilan unos. Unesite ispravnu email adresu.")
    while True:
        password = getpass.getpass("Unesite sifru(mora sadrzati bar 8 karaktera): ")
        if len(password) >= 8:
            break
        else:
            print("Sifra mora sadrzati bar 8 karaktera.")
    print("Uspesna registracija!")
    return email, password, name, surname, phone
def user_input():
    #trazi od korisnika da unese broj od 1 do 4
    while True:
        try:
            user_input = int(input("Unesite broj od 1 do 4: "))
            if 1 <= user_input <= 4:
                print(f"Uneli ste {user_input}.")
                break
            else:
                print("Unesite vazeci broj od 1 do 4.")
        except ValueError:
            print("Nepravilan unos. Unesite vazeci broj.")
    return user_input
def new_user(email, password, name, surname, phone):
    #unosi podatke od korisnika u odgovarajuce csv fajlove
    with open('data/general/users.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lines = list(csv_reader)
        if len(lines) != 0:
            reversed_lines = reversed(lines)
            for line in reversed_lines:
                i = int(line['USER_ID'])
                break
        else:
            i = 0
        csv_file.close()
    dict1 = {'USER_ID': '00' + str(i + 1), 'EMAIL': email, 'PASSWORD': password}
    with open('data/general/users.csv', 'a') as csv_file:
        fieldnames = ['USER_ID', 'EMAIL', 'PASSWORD']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow(dict1)
        csv_file.close()
    dict2 = {'USER_ID': '00' + str(i + 1), 'NAME': name, 'SURNAME': surname, 'PHONE': phone, 'EMAIL': email,
             'PASSWORD': password}
    folder_name = "data/users/00" + str(i + 1)
    folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = "data.csv"
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'a') as csv_file:
            fieldnames = ['USER_ID', 'NAME', 'SURNAME', 'PHONE', 'EMAIL', 'PASSWORD']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(dict2)
            user = dict2['USER_ID']
            #return user
    else:
        with open(file_path, 'w', newline='') as file:
            #print(f"File '{file_path}' created.")
            fieldnames = ['USER_ID', 'NAME', 'SURNAME', 'PHONE', 'EMAIL', 'PASSWORD']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerow(dict2)
            user = dict2['USER_ID']
            #return user
    dinDev = input("Da li zelite da otvorite dinarski ili devizni racun?[RSD/EUR]: ")
    user = new_account(user, dinDev)
    return user
def new_account(user, dinDev):
    #unosi podatke o racunu korisnika u odgovarajuci csv fajl
    folder_name = "data/users/" + user
    folder_path = os.path.join(os.getcwd(), folder_name)
    file_name = "account.csv"
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        dict = {'ACCOUNT_NUMBER': acc_Num(dinDev), 'CURRENCY': dinDev, 'BALANCE': 0, 'main': 0}
        with open(file_path, 'a') as csv_file:
            fieldnames = ['ACCOUNT_NUMBER', 'CURRENCY', 'BALANCE', 'main']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(dict)
    else:
        dict = {'ACCOUNT_NUMBER': acc_Num(dinDev), 'CURRENCY': dinDev, 'BALANCE': 0, 'main': 1}
        with open(file_path, 'w', newline='') as file:
            print(f"File '{file_path}' created.")
            fieldnames = ['ACCOUNT_NUMBER', 'CURRENCY', 'BALANCE', 'main']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerow(dict)
    print("Racun je uspesno otvoren.")
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lines = list(csv_reader)
        if len(lines) != 0:
            reversed_lines = reversed(lines)
            for line in reversed_lines:
                i = str(line['ACCOUNT_NUMBER'])
                break
    print("Vas broj racuna je: " + i)
    return user
def print_account_number():
    #ispisuje sve racune koje korisnik ima u banci
    folder_name = "data/users/" + user
    file_name = "account.csv"
    file_path = os.path.join(os.getcwd(), folder_name, file_name)
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader, None)
        for index, row in enumerate(csv_reader, start=1):
            if row:
                print(f"{index}. {row[0]}")
    return index
def get_user_choice(rows):
    #vraca izbor racuna korisnika
    while True:
        try:
            user_input = int(input(f"Enter a number (1-{rows}): "))
            if 1 <= user_input <= rows:
                return user_input
            else:
                print(f"Please enter a number between 1 and {rows}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
def get_account_number(num):
    #vraca odgovarajuci racun u zavisnosti od korisnikovog izbora
    folder_name = "data/users/" + user
    file_name = "account.csv"
    file_path = os.path.join(os.getcwd(), folder_name, file_name)
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader, None)
        for row_number, row in enumerate(csv_reader, start=1):
            if row_number == num:
                return row[0]
def deposit_withdraw(user, accnum, op,):
    #upisuje/oduzima unetu vrednost na/sa odgovarajuce mesto u csv fajlu
    folder_name = "data/users/" + user
    file_name = "account.csv"
    file_path = os.path.join(os.getcwd(), folder_name, file_name)
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['ACCOUNT_NUMBER'] == accnum:
            if op == '+':
                current_value = int(row['BALANCE'])
                i = int(input("Unesite kolicinu koju zelite da uplatite: "))
                updated_value = current_value + i
                row['BALANCE'] = str(updated_value)
                print("Uplata uspesna!")
            elif op == '-':
                current_value = int(row['BALANCE'])
                while True:
                    i = int(input("Unesite kolicinu koju zelite da podignete: "))
                    if i <= current_value:
                        updated_value = current_value - i
                        row['BALANCE'] = str(updated_value)
                        print("Uspenso!")
                        break
                    else:
                        print("Trenutno nije moguce isplatiti tu kolicinu.")
    with open(file_path, 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
def balance(accnum):
    #ispisuje vrednost iz csv fajla koja se odnosi na kolicinu novca
    folder_name = "data/users/" + user
    file_name = "account.csv"
    file_path = os.path.join(os.getcwd(), folder_name, file_name)
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['ACCOUNT_NUMBER'] == accnum:
            print(row['CURRENCY']+""+row['BALANCE'])
def modify_acc(user, c):
    #izmenjuje podatke u odgovarajucim csv fajlovima u zavisnosti od korisnickog izbora
    if c == 3:
        new_phone = input("Enter new phone number: ")
        folder_name = "data/users/" + user
        file_name = "data.csv"
        file_path = os.path.join(os.getcwd(), folder_name, file_name)
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        if len(rows) == 1:
            temp = rows[0]
            temp['PHONE'] = new_phone
            with open(file_path, 'w', newline='') as file:
                fieldnames = ['USER_ID', 'NAME', 'SURNAME', 'PHONE', 'EMAIL', 'PASSWORD']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print("User information updated successfully.")
    elif c == 2:
        while True:
            new_password = getpass.getpass("Unesite novu sifru(mora sadrzati bar 8 karaktera): ")
            if len(new_password) >= 8:
                break
            else:
                print("Sifra mora sadrzati bar 8 karaktera.")
        folder_name = "data/users/" + user
        file_name = "data.csv"
        file_path = os.path.join(os.getcwd(), folder_name, file_name)
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        if len(rows) == 1:
            temp = rows[0]
            temp['PASSWORD'] = new_password
            with open(file_path, 'w', newline='') as file:
                fieldnames = ['USER_ID', 'NAME', 'SURNAME', 'PHONE', 'EMAIL', 'PASSWORD']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        with open('data/general/users.csv', 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        found_user = False
        for row in rows:
            if row['USER_ID'] == str(user):
                row['PASSWORD'] = new_password
                found_user = True
                break
        if found_user:
            with open('data/general/users.csv', 'w', newline='') as csv_file:
                fieldnames = ['USER_ID', 'EMAIL', 'PASSWORD']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print("User information updated successfully.")
    else:
        while True:
            new_email = input("Unesite novu email adresu: ")
            if is_valid_email(new_email):
                if does_email_exist(new_email):
                    print("Email vec postoji. Pokusajte ponovo.")
                    continue
                else:
                    break
            else:
                print("Nepravilan unos. Unesite ispravnu email adresu.")
        folder_name = "data/users/" + user
        file_name = "data.csv"
        file_path = os.path.join(os.getcwd(), folder_name, file_name)
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        if len(rows) == 1:
            temp = rows[0]
            temp['EMAIL'] = new_email
            with open(file_path, 'w', newline='') as file:
                fieldnames = ['USER_ID', 'NAME', 'SURNAME', 'PHONE', 'EMAIL', 'PASSWORD']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        with open('data/general/users.csv', 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        found_user = False
        for row in rows:
            if row['USER_ID'] == str(user):
                row['EMAIL'] = new_email
                found_user = True
                break
        if found_user:
            with open('data/general/users.csv', 'w', newline='') as csv_file:
                fieldnames = ['USER_ID', 'EMAIL', 'PASSWORD']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print("User information updated successfully.")
def remove_acc(user, accnum):
    #brise sve iz reda vezanog za izabrani broj racuna
    folder_name = "data/users/" + user
    file_name = "account.csv"
    file_path = os.path.join(os.getcwd(), folder_name, file_name)
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        lines = list(reader)
        found = False
        for index, row in enumerate(lines):
            if row and row[0] == accnum:
                lines.pop(index)
                found = True
                break
        if found:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)
def intro():
    #ispisuje pocetni ekran i trazi od korisnika da unese opciju
    print("\t\t\t\t**********************")
    print("\t\t\t\tBANK MANAGEMENT SYSTEM")
    print("\t\t\t\t**********************")
    print("\t1. LOG IN")
    print("\t2. SIGN UP")
    print("\t3. INFO")
    print("\t4. EXIT")
    c = user_input()
    if c == 2:
        user_email, user_password, user_name, user_surname, user_phone = get_user_info()
        user = new_user(user_email, user_password, user_name, user_surname, user_phone)
    elif c == 1:
        user = login()
    elif c == 3:
        print("Info")
        ch = input("Press enter to continue ")
        intro()
    elif c == 4:
        print("Exiting the program!")
        exit()
    else:
        print("Invalid input. Please try again.")
    return user


"""Par stvari jos treba da uradim, pola je na srpskom, pola na engleskom, dodam proveru na nekim mestima,
ne radi mi da sakrijem unos sifre, ne znam sta da radim sa main opcijom u account fajlu i hocu da dodam
brisanje konzole nakon odredjenih izbora 
Grafik nisam siguran kako da uradim jos, i ne znam sta treba da stavi kod info opcije na pocetnom ekranu
i nzm sta da stavim u readme fajl"""
if __name__ == '__main__':
    user = intro()
    ch = ''
    while ch != 8:
        print("\tMAIN MENU")
        print("\t1. OTVORI NOVI RACUN")
        print("\t2. UPLATA NA RACUN")
        print("\t3. ISPLATA SA RACUNA")
        print("\t4. STANJE NA RACUNU")
        print("\t5. GRAFIK")
        print("\t6. ZATVORI RACUN")
        print("\t7. PROMENI PODATKE")
        print("\t8. EXIT")
        print(user)
        ch = input("\tUnesite broj od 1 do 8: ")

        if ch == '1':
            dinDev = input("Da li zelite da otvorite dinarski ili devizni racun?[RSD/EUR]: ")
            new_account(user, dinDev)
            ch = input("Press enter to continue ")
        elif ch == '2':
            rows = print_account_number()
            num = get_user_choice(rows)
            accnum = get_account_number(num)
            op = '+'
            deposit_withdraw(user, accnum, op)
            ch = input("Press enter to continue ")
        elif ch == '3':
            rows = print_account_number()
            num = get_user_choice(rows)
            accnum = get_account_number(num)
            op = '-'
            deposit_withdraw(user, accnum, op)
            ch = input("Press enter to continue ")
        elif ch == '4':
            rows = print_account_number()
            num = get_user_choice(rows)
            accnum = get_account_number(num)
            balance(accnum)
            ch = input("Press enter to continue ")
        elif ch == '6':
            rows = print_account_number()
            num = get_user_choice(rows)
            accnum = get_account_number(num)
            remove_acc(user, accnum)
            ch = input("Press enter to continue ")
        elif ch == '7':
            print("1. EMAIL")
            print("2. PASSWORD")
            print("3. PHONE NUMBER")
            print("4. BACK")
            c = user_input()
            if c == 4:
                continue
            else:
                modify_acc(user, c)
        elif ch == '8':
            print("\tHvala sto ste koristili aplikaciju!")
            break
        else:
            print("Invalidan izbor")




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
