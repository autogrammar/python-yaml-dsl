# Skrypt run.py do obsługi kont email


Skrypt `run.py` jest głównym komponentem systemu do zarządzania kontami email i wiadomościami. Obsługuje on pojedyncze komendy, wykorzystując funkcje zdefiniowane w plikach `Account.py` i `Message.py`.

It now handles all the actions mentioned in the object.yaml file: connect and disconnect for Account, and create, read, and delete for Message.
The execute_command function has been expanded to handle these new actions.
For the connect action in Account, it now passes all the required private data (server, username, password, port) along with the email.
The script now expects the Account and Message classes to have the appropriate methods (connect, disconnect, create, read, delete) as described in the documentation.
It still uses the private.yaml file to fetch the private connection data for email accounts.
The overall structure and flow of the script remain the same, maintaining compatibility with the existing query.yaml format.
This script should now be able to handle a wider range of commands as specified in the object.yaml file, while still maintaining the security of private data by reading it from the private.yaml file.

## Ogólny schemat działania

Skrypt `run.py` działa w następujący sposób:

1. Wczytuje komendy z pliku `query.yaml`.
2. Przetwarza każdą komendę, wywołując odpowiednie funkcje z `Account.py` lub `Message.py`.
3. Wykorzystuje dane logowania z pliku `private.yaml` do nawiązywania połączeń z kontami email.

## Struktura projektu

- `run.py`: Główny skrypt wykonawczy
- `Account.py`: Klasa do zarządzania kontami email
- `Message.py`: Klasa do tworzenia i zarządzania wiadomościami
- `query.yaml`: Plik z komendami do wykonania
- `private.yaml`: Plik z danymi logowania do kont email

## Jak używać

Aby uruchomić skrypt, należy użyć następującej komendy w terminalu:

```
python run.py query.yaml
```

## PLik `query.yaml`

```yaml
query:
  python:
    - Account.py connect --email "admin@domain.com"
    - Message.py create --sender "bob@domain.com" --content "Meeting summary" --subject "Team Notification"
    - Account.py disconnect --email "admin@domain.com"
```

Stworz funkcje: Account.py i Message.py oraz uzyj zmiennych potrzebnych do polaczenie servera z pliku `private.yaml`
w zaleznosci od uzytego konta, tak jak w przykladzie powinno byc uzywane dane logowania "admin@domain.com" z pliku:

```bash
server: "server3.domain.com"
username: "user3"
password: "pass3"
port: 3333
```    

## Plik `private.yaml`

Prywatne dane potrzebne do uruchomienia usług przez skrypt w Pythonie są przechowywane w pliku `private.yaml`.
```bash
Account:
  email:
    "tom@domain.com":
      server: "server1.domain.com"
      username: "user1"
      password: "pass1"
      port: 1111
    "jane@domain.com":
      server: "server2.domain.com"
      username: "user2"
      password: "pass2"
      port: 2222
    "admin@domain.com":
      server: "server3.domain.com"
      username: "user3"
      password: "pass3"
      port: 3333
```


connect() w klasie Account przyjmuje argumenty w `public` jak email jako publiczne argumenty  `private` są prywatne i pobierane przez skrypt główny `run.py` w Account to: username, password i port

```aiignore
  public:
    email: string
  private:
    server: string
    password: string
    username: string
    port: number
```
zgodnie z plikiem `object.yaml`

```yaml
Message:
  object:
    Account: connect
  action:
    create:
      sentence: "{action} {} with {public}"
      shell: "{}.sh {action} {public}"
      python: "{}.py {action} {public}"
      sql: "{}.sql {action} {public}"
      public:
        sender: string
        content: string
        subject: string
    read:
      sentence: "{action} {modifier} {} with {public}"
      shell: "{}.sh {action} {modifier} {public}"
      python: "{}.py {action} {modifier} {public}"
      sql: "{}.sql {action} {modifier} {public}"
      public:
        from: datetime
        to: datetime
        sender: string
        content: string
        subject: string
      modifier:
        last: integer
        all: ''
        one: ''
    delete:
      sentence: "{} {modifier} {action} where {public}"
      shell: "{}.sh {action} {modifier} {public}"
      python: "{}.py {action} {modifier} {public}"
      sql: "{}.sql {action} {modifier} {public}"
      api: "{}.curl {action} {modifier} {public}"
      public:
        from: datetime
        to: datetime
        sender: string
        content: string
        subject: string
      modifier:
        last: integer
        all: ''
        one: ''


Account:
  action:
    connect:
      object: Message
      sentence: "({action} to) {} {public}"
      shell: "{}.sh {action} {public}"
      python: "{}.py {action} {public}"
      sql: "{}.sql {action} {public}"
      public:
        email: string
      private:
        server: string
        password: string
        username: string
        port: number

    disconnect:
      sentence: "{action} {} {public}"
      shell: "{}.sh {action} {public}"
      python: "{}.py {action} {public}"
      sql: "{}.sql {action} {public}"
      public:
        email: string
      private:
        server: string
        password: string
        username: string
        port: number

```