## Projekt do wykonania

Create DSL builder based on yaml specifications Save YAML specification in a `object.yaml` file
The main purpose of this project is to help users define their YAML specifications in a file and  then generate a specified number of sentences based on those specifications as separated file: `sentences.yaml`

## Sposób uruchomienia
Run the script from the command line, specifying the YAML file and optionally the number of sentences: 

```bash
python dsl.py object.yaml private.yaml public.yaml -n 5 -o sentences.yaml
```

## Plik `object.yaml`

This is a Domain-Specific Language (DSL) builder that uses YAML specifications to generate sentences.

```yaml
Message:
  object:
    - Account
  action:
    create:
      sentence: "{action} {} with {public}"
      shell: "{}.sh {action} {public}"
      public:
        sender: string
        content: string
        subject: string
    read:
      sentence: "{action:read} {many} {} with {public}"
      shell: "{}.sh {many} {action} {public}"
      public:
        from: datetime
        to: datetime
        sender: string
        content: string
        subject: string
      modifier:
        - last: integer
        - all
        - one
    delete:
      sentence: "{}.sh {modifier} {action} {public}"
      shell: "{}.sh {modifier} {action} {public}"
      public:
        from: datetime
        to: datetime
        sender: string
        content: string
        subject: string
      modifier:
        - last: integer
        - all
        - one


Account:
  default: connect
  action:
    connect:
      object:
        - Message
      sentence: "{action} to {} {public}"
      shell: "{}.sh {action} {public}"
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
      public:
        email: string
      private:
        server: string
        password: string
        username: string
        port: number

```

`{}` - oznacza aktualny `object` czyli ioznacza to pattern:
- "{action:disconnect} {} {public}"
przykład:
- disconnect Account email "tom@domain.com"


parametr `object` określa w `sentence` zagnieżdzenie innego obiektu 
W ten sposób można stworzyć hierarchię budowania zdania, podmiot i przedmiot.

## Przykłady poprawne
```yaml
sentences:
    - read Message with subject "Meeting" from Account email "tom@domain.com" 
    - delete last 6 Message from Account email "tom@domain.com"
    - create Message on Account email "tom@domain.com"
    - disconnect Account email "tom@domain.com"
    - delete last 95 Message with date sender "admin@domain.com" subject "Important Announcement"
    - connect to Account email "admin@domain.com", create Message with sender "bob@domain.com" content  "default_string" subject "Important Announcement", disconnect Account email "tom@domain.com"
    - disconnect Account email "admin@domain.com"
    - create Message with sender "bob@domain.com" content "Important update" subject "Project Update"
    - connect to Account email "tom@domain.com", read all Message with sender "admin@domain.com" subject "Important Announcement"
```


## Błedne zastosowanie `sentence` pattern:

konfiguracja `object` `Action`
```yaml
  action:
    connect:
      object:
        - Message
      sentence: "{action} to {} {public}"
      shell: "{}.sh {action} {public}"
      public:
        email: string
      private:
        server: string
        password: string
        username: string
        port: number
```
Przykłady poniżej jest niepoprawne, ponieważ jest zastosowany drugi `sentence` pattern, gdzie kolejnym elementem zdania po przecinku musi być {object} Message wraz z całą regułą `sentence` z Message w zależności od `action`
```yaml
sentences:
- connect to Account email "bob@domain.com"
```
Przykłady poprawne nr 1
```yaml
sentences:
- connect Account email "bob@domain.com"
```
Przykłady poprawne nr 2 z obiektem Message 
```yaml
sentences:
- connect to Account email "bob@domain.com", create Message with sender "default_string" subject "default_string" content "default_string"
```

## Błąd Action typu one
konfiguracja action i modyfikatorów one i many:

```yaml
    read:
      sentence: "{action:read} {many} {} with {public}"
      shell: "{}.sh {many} {action} {public}"
      public:
        from: datetime
        to: datetime
        sender: string
        content: string
        subject: string
      modifier:
        - last: integer
        - all
        - one
```
Akcja `create` nie może być użyta z modyfikatorem many: `last` lub `all` bo go nie ma w sekcji action co oznacza, że poniższe zdanie jest błędne: 
```yaml
- connect to Account email "admin@domain.com", create last 8 Message with content "default_string"
```

Poprawne zdanie powinno wyglądać tak:
```yaml
- connect to Account email "admin@domain.com", create Message with content "default_string"
```


## Action disconnect

Przykłady niepoprawne, ponieważ struktura definiowana przez poniższą konfigurację Account, gdzie action disconnect konczy zdanie i nie umożliwia dodawanie kolejnych obiektów w zdaniu
```yaml
    disconnect:
      sentence: "{action} {} {public}"
      shell: "{}.sh {action} {public}"
      public:
        email: string
      private:
        server: string
        password: string
        username: string
        port: number
```

Przykład konfiguracji `default: connect` oznacza, że gdy nie jest określona akcja w zdaniu, to domyślnie jest zdefiniowana w `default` czyli w tym przykładzie action `connect`

```yaml
sentences:
- disconnect Account email "admin@domain.com", delete all Message with sender "default_sender" subject "default_subject"
- read all Message last 6
```


Funkcja generująca przykłady powinna generować `sentence` pattern generycznie i nie używać konkretnych nazw z pliku `object.yaml` a bazować na hierarchii powiązań, aby uzyskać widoczny efekt
Liczba mnoga słowa powinna być rozpoznawana i zamieniana na pojedynczą, stwórz reguły odmiany liczby mnogje dla jezyka angielskiego. 


## Plik `public.yaml`

W pliku `public.yaml` są przechowywane wartości, które są używane w sentences oraz dane generowane w trakcie polaczenia z uslugami, pobierane do cache
```yaml
Message:
  sender:
    - "alice@domain.com"
    - "bob@domain.com"
    - "tom@domain.com"
    - "admin@domain.com"
  content:
    - "Hello, World!"
    - "Important update"
    - "default_string"
  subject:
    - "Meeting"
    - "Project Update"
    - "Important Announcement"

Account:
  email:
    - "tom@domain.com"
    - "jane@domain.com"
    - "admin@domain.com"

```


## Plik `private.yaml`

Prywatne dane potrzebne do uruchomienia uslug przez skrypt w python w pliku `private.yaml`
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




