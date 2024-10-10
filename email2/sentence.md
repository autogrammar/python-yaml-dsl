## Cel Projektu

DSL builder oparty na specyfikacjach YAML. Specyfikacja YAML jest zapisywana w pliku `object.yaml`.

Ta implementacja obsługuje podstawowe reguły tworzenia zdań w oparciu o specyfikację YAML. Można ją rozszerzyć o bardziej zaawansowane reguły, jeśli to konieczne.

Ten skrypt implementuje następujące funkcjonalności:
- Wczytywanie specyfikacji YAML z plików `object.yaml`, `private.yaml` i `public.yaml`.
- Generowanie zdań na podstawie specyfikacji.
- Zapisywanie wygenerowanych zdań do pliku wyjściowego `sentences.yaml`

Skrypt można uruchomić z wiersza poleceń w następujący sposób:

```bash
python sentence.py object.yaml private.yaml public.yaml -n 5 -o sentences.yaml
```

Gdzie:
- `object.yaml` to plik ze specyfikacją obiektów i akcji
- `private.yaml` to plik z prywatnymi danymi
- `public.yaml` to plik z publicznymi danymi
- `-n 5` określa liczbę zdań do wygenerowania (domyślnie 5)
- `-o sentences.yaml` określa plik wyjściowy (domyślnie sentences.yaml)

Skrypt generuje zdania zgodnie z podaną specyfikacją, używając danych z plików public.yaml i private.yaml. 
Generowane zdania są zapisywane do pliku `sentences.yaml` w formacie YAML.

Parametr `{public}` w `sentence` oznacza, że musimy podać co najmniej jeden parametr z listy `public` zdefiniowanych w akcji, jest on obligatoryjny.

Przykłady:

```yaml
sentences:
    - connect to Account email "admin@domain.com", create Message with sender "bob@domain.com" content "default_string" subject "Important Announcement"
    - disconnect Account email "tom@domain.com"
```

Funkcje działają w oparciu o dane z plików i są generyczne, nie mają hardkodowanych zmiennych, dopasowują strukturę do reguł i danych z plików YAML.

## Plik `object.yaml`

To jest Domain-Specific Language (DSL) builder, który używa specyfikacji YAML do generowania zdań.

```yaml
Message:
  object:
    Account: connect
  action:
    create:
      sentence: "{action} {} with {public}"
      shell: "{}.sh {action} {public}"
      public:
        sender: string
        content: string
        subject: string
    read:
      sentence: "{action} {modifier} {} with {public}"
      shell: "{}.sh {modifier} {action} {public}"
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
      shell: "{}.sh {modifier} {action} {public}"
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

Generowanie zdań uwzględnia modyfikatory i obiekty zagnieżdżone.
Używane są wartości z pliku public.yaml, a w przypadku ich braku, generowane są wartości domyślne.

`{}` oznacza aktualny `object`, czyli oznacza to pattern:
- "{action} {} {public}"
przykład:
```yaml
sentences:
  - disconnect Account email "tom@domain.com"
```

Parametr `sentence` określa pattern w zdaniach, 
parametr `object` określa hierarchię w budowaniu zdań, podmiot i przedmiot.
Jeśli występuje, to konieczne jest użycie drugiego członu zdania po przecinku. W przypadku przykładu `Message` trzeba użyć jeszcze object `Account` z akcją `connect`, 
ponieważ konfiguracja dla action `connect` wymusza użycie object `Message`, ale dla `disconnect` już nie. Przykłady:

```yaml
sentences:
    - connect to Account email "admin@domain.com", create Message with sender "bob@domain.com" content "default_string" subject "Important Announcement"
    - disconnect Account email "tom@domain.com"
```

W obiekcie lub akcji może znajdować się deklaracja `object: Account`, co oznacza, że zdanie musi zawierać również zdanie wygenerowane na podstawie obiektu zależnego, jak w przykładzie Messages:

```yaml
sentences:
    - read Message with subject "Meeting", Account email "tom@domain.com" 
    - delete last 6 Message, Account email "tom@domain.com"
    - connect to Account email "tom@domain.com", delete last 95 Message with sender "admin@domain.com" subject "Important Announcement"
    - disconnect Account email "tom@domain.com"
```

## Sentence i opcjonalne parametry

W object `Account` znajduje się
`sentence: "({action} to) {} {public}"`
Przykład tej konfiguracji oznacza, że zawartość `({action} to)` jest opcjonalnie występująca w zdaniu, czyli jak w tym przykładzie action `connect`:
```yaml
sentences:
    - connect to Account email "tom@domain.com", create Message with sender "bob@domain.com" content "default_string" subject "Important Announcement"
    - disconnect Account email "tom@domain.com"
```
Zdanie `disconnect Account email "tom@domain.com"` nie ma nawiasów `()`, co oznacza, że nie ma tam opcjonalnej zawartości i zawiera `disconnect`.

## Inne poprawne przykłady 
```yaml
sentences:
    - create Message with sender "bob@domain.com" content "Important update" subject "Project Update"
    - connect to Account email "tom@domain.com", read all Message with sender "admin@domain.com" subject "Important Announcement"
```

## Błędne zastosowanie `sentence` pattern:

konfiguracja `object` `Action`
```yaml
Account:
  action:
    connect:
      object: Message
      sentence: "({action} to) {} {public}"
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
Przykład poprawny z obiektem Message 
```yaml
sentences:
- connect to Account email "bob@domain.com", create Message with sender "default_string" subject "default_string" content "default_string"
```
Istotne jest Uwzględnienie obowiązkowego obiektu Message dla akcji connect w Account.
Obsługa domyślnej akcji (default) dla obiektów, które ją mają zdefiniowaną.
Generowanie zdań zaczynając od losowo wybranego obiektu głównego, co powinno zapewnić większą różnorodność generowanych zdań.


## Błąd Action typu one
konfiguracja action i modyfikatorów one, all, last z podaniem wartosci typu integer w object `Message`

```yaml
Message:
  object: 
    Account: connect
  action:
    create:
      sentence: "{action} {} with {public}"
      shell: "{}.sh {action} {public}"
      public:
        sender: string
        content: string
        subject: string
    read:
      sentence: "{action} {modifier} {} with {public}"
      shell: "{}.sh {modifier} {action} {public}"
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
```
Akcja `create` nie może być użyta z modyfikatorem: `last` lub `all` bo go nie ma w sekcji action co oznacza, że poniższe zdanie jest błędne: 
```yaml
- connect to Account email "admin@domain.com", create last 8 Message with content "default_string"
```

Poprawne zdanie powinno wyglądać tak:
```yaml
- connect to Account email "admin@domain.com", create Message with content "default_string"
```


## Action disconnect


```yaml
sentences:
- disconnect Account email "admin@domain.com", delete all Message with sender "default_sender" subject "default_subject"
- read all Message last 6
```


Przykłady niepoprawne, ponieważ struktura definiowana przez poniższą konfigurację
```yaml
Account:
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
action w object `Account` disconnect konczy zdanie, poniewaz nie zawiera `object` `Message` co znaczy, że connect umożliwia dodawania kolejnych obiektów w zdaniu 

konfiguracja `object` `Action` dla object `Account`


## Generowanie przykładów

Funkcja generująca przykłady powinna generować `sentence` pattern generycznie i nie używać konkretnych nazw z pliku `object.yaml`, a bazować na hierarchii powiązań, aby uzyskać widoczny efekt.
Liczba mnoga słów powinna być rozpoznawana i zamieniana na pojedynczą. Należy stworzyć reguły odmiany liczby mnogiej dla języka angielskiego.

## Plik `public.yaml`

W pliku `public.yaml` są przechowywane wartości, które są używane w sentences oraz dane generowane w trakcie połączenia z usługami, pobierane do cache.
```yaml
Account:
  email:
    - "tom@domain.com"
    - "jane@domain.com"
    - "admin@domain.com"

Message:
  sender:
    - "alice@domain.com"
    - "bob@domain.com"
    - "tom@domain.com"
    - "admin@domain.com"
  content:
    - "Hello, World!"
    - "Important update"
    - "Meeting summary"
    - "Project status report"
    - "Reminder: Team building event"
  subject:
    - "Meeting"
    - "Project Update"
    - "Important Announcement"
    - "Team Notification"
    - "Weekly Report"
  from:
    - "2023-01-01"
    - "2023-06-15"
    - "2023-12-31T01:59:59Z"
  to:
    - "2023-12-31"
    - "2024-06-30"
    - "2023-12-31T23:59:59Z"

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




