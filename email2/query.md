# Dokumentacja projektu Shell Script Generator

## Cel projektu

Celem projektu jest stworzenie generatora skryptów powłoki shell na podstawie specyfikacji YAML. Generator będzie korzystał z tych samych plików wejściowych co projekt DSL builder, ale zamiast generować zdania, będzie tworzył odpowiadające im polecenia shell.
- Należy zwrócić uwagę na bezpieczeństwo przy generowaniu i wykonywaniu poleceń shell.

Projektu, który generuje komendy do skrypt powłoki shell na podstawie wzorców z pliku object.yaml. 
- skrypt do parsowania i przyporządkowania wygenerowanych zdań
Dokumentacja projektu Shell Script Generator
Celem projektu jest stworzenie generatora skryptów powłoki shell na podstawie specyfikacji YAML. Generator będzie korzystał z tych samych plików wejściowych co projekt DSL builder, ale zamiast generować zdania, będzie tworzył odpowiadające im polecenia shell.

## Pliki wejściowe
Projekt korzysta z następujących plików wejściowych:
object.yaml - zawiera specyfikację obiektów, akcji i wzorców dla poleceń shell
public.yaml - zawiera publiczne dane używane do generowania poleceń
private.yaml - zawiera prywatne dane (nie używane bezpośrednio w generowanych poleceniach)

## Plik wyjściowy
Generator tworzy plik query.yaml, który zawiera wygenerowane polecenia shell wraz z odpowiadającymi im zdaniami.
Struktura pliku query.yaml
Przykład generowania poleceń shell
Na podstawie wzorca z pliku object.yaml:
Generator stworzy wpis w pliku query.yaml:

## Funkcjonalności
Parsowanie plików YAML (object.yaml, public.yaml, private.yaml)
Generowanie zdań zgodnie z regułami z object.yaml
Generowanie odpowiadających poleceń shell na podstawie wzorców z object.yaml
Obsługa zagnieżdżonych obiektów i akcji
Obsługa modyfikatorów i opcjonalnych części poleceń
Zapisywanie wygenerowanych zdań i poleceń do pliku query.yaml


## Implementacja
main() - główna funkcja obsługująca argumenty wiersza poleceń i koordynująca proces generowania
Rozszerzenia
Projekt można rozszerzyć o następujące funkcjonalności:
Walidacja wygenerowanych poleceń shell
Dodanie możliwości wykonywania wygenerowanych poleceń
Interaktywny tryb generowania poleceń
Obsługa bardziej złożonych wzorców poleceń shell
Ta dokumentacja powinna pomóc w zrozumieniu celu i struktury projektu generatora skryptów shell. Możesz ją dostosować lub rozszerzyć w zależności od konkretnych potrzeb i wymagań projektu.



## Sposób uruchomienia
Run the script from the command line, specifying the YAML files 

```bash
python query.py query.yaml object.yaml private.yaml public.yaml
```

1. `sentences.yaml` - zawiera wcześniej wygenereowane zdania, które bedą zmieniane na query w shell.yaml
2. `object.yaml` - zawiera specyfikację obiektów, akcji i wzorców dla poleceń shell
3. `public.yaml` - zawiera publiczne dane używane do generowania poleceń
4. `private.yaml` - zawiera prywatne dane (nie używane bezpośrednio w generowanych poleceniach)
5. `query.yaml` - zawiera wygenerowane zdania z query, to plik wyjściowy z atrybutem -o

## Plik wyjściowy

Generator tworzy plik `query.yaml`, który zawiera wygenerowane polecenia shell wraz z odpowiadającymi im zdaniami.

## Struktura pliku `query.yaml`

```yaml
query:
  sentences:
    - connect to Account email "admin@domain.com", create Message with sender "tom@domain.com" content "Meeting summary" subject "Weekly Report"
    - read one Message with from "2023-01-01" to "2023-12-31" sender "alice@domain.com"
    - read all Message with from "2023-12-31T01:59:59Z" to "2023-12-31" subject "Weekly Report"
    - disconnect Account email "admin@domain.com"
  shell:
    - Account.sh connect email "admin@domain.com"
    - Message.sh create sender "tom@domain.com" content "Meeting summary" subject "Weekly Report"
    - Message.sh read one from from "2023-01-01" to "2023-12-31" sender "alice@domain.com"
    - Message.sh read all from "2023-12-31T01:59:59Z" to "2023-12-31" subject "Weekly Report"
    - Account.sh disconnect email "admin@domain.com"

```


## Struktura pliku `sentences.yaml`
```yaml
sentences:
  - connect to Account email "admin@domain.com", create Message with sender "tom@domain.com" content "Meeting summary" subject "Weekly Report"
  - read one Message with from "2023-01-01" to "2023-12-31" sender "alice@domain.com"
  - read all Message with from "2023-12-31T01:59:59Z" to "2023-12-31" subject "Weekly Report"
  - disconnect Account email "admin@domain.com"
```



## Plik `object.yaml`

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
      shell: "{}.sh {action} {modifier} {public}"
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

`{}` - oznacza aktualny `object` czyli ioznacza to pattern:
- "{action:disconnect} {} {public}"
przykład:
- disconnect Account email "tom@domain.com"



## Plik `public.yaml`

W pliku `public.yaml` są przechowywane wartości, które są używane w `sentences.yaml` oraz dane generowane w trakcie polaczenia z uslugami, pobierane do cache
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
  content:
    - "Hello, World!"
    - "Important update"
  subject:
    - "Meeting"
    - "Project Update"
    - "Important Announcement"
```


## Plik `private.yaml`

Prywatne dane potrzebne do uruchomienia uslug przez skrypt w python w pliku `private.yaml`
```bash
Account:
  server:
    - "server1.domain.com"
    - "server2.domain.com"
  username:
    - "user1"
    - "user2"
  password:
    - "pass1"
    - "pass2"
  port:
    - 8080
    - 9090
```    
