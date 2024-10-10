- skrypt do parsowania i przyporządkowania wygenerowanych zdań
Rozumiem, że chcesz stworzyć dokumentację dla projektu, który będzie generował skrypty powłoki shell na podstawie wzorców z pliku object.yaml. Oto propozycja dokumentacji dla takiego projektu:
Dokumentacja projektu Shell Script Generator
Cel projektu
Celem projektu jest stworzenie generatora skryptów powłoki shell na podstawie specyfikacji YAML. Generator będzie korzystał z tych samych plików wejściowych co projekt DSL builder, ale zamiast generować zdania, będzie tworzył odpowiadające im polecenia shell.
Pliki wejściowe
Projekt korzysta z następujących plików wejściowych:
1. object.yaml - zawiera specyfikację obiektów, akcji i wzorców dla poleceń shell
public.yaml - zawiera publiczne dane używane do generowania poleceń
private.yaml - zawiera prywatne dane (nie używane bezpośrednio w generowanych poleceniach)
Plik wyjściowy
Generator tworzy plik query.yaml, który zawiera wygenerowane polecenia shell wraz z odpowiadającymi im zdaniami.
Struktura pliku query.yaml
Przykład generowania poleceń shell
Na podstawie wzorca z pliku object.yaml:
Generator stworzy wpis w pliku query.yaml:
Funkcjonalności
1. Parsowanie plików YAML (object.yaml, public.yaml, private.yaml)
Generowanie zdań zgodnie z regułami z object.yaml
Generowanie odpowiadających poleceń shell na podstawie wzorców z object.yaml
Obsługa zagnieżdżonych obiektów i akcji
Obsługa modyfikatorów i opcjonalnych części poleceń
Zapisywanie wygenerowanych zdań i poleceń do pliku query.yaml
Użycie
Gdzie:
object.yaml - plik ze specyfikacją obiektów i akcji
private.yaml - plik z prywatnymi danymi
public.yaml - plik z publicznymi danymi
-n 5 - liczba poleceń do wygenerowania (domyślnie 5)
-o query.yaml - nazwa pliku wyjściowego (domyślnie query.yaml)
Implementacja
Główne funkcje do zaimplementowania:
load_yaml(file_path: str) -> Dict[str, Any] - wczytywanie plików YAML
generate_shell_command(object_spec: Dict[str, Any], action: str, object_name: str, public_data: Dict[str, Any]) -> str - generowanie pojedynczego polecenia shell
generate_commands(spec: Dict[str, Any], public_data: Dict[str, Any], num_commands: int) -> List[Dict[str, str]] - generowanie listy poleceń i odpowiadających im zdań
main() - główna funkcja obsługująca argumenty wiersza poleceń i koordynująca proces generowania
Rozszerzenia
Projekt można rozszerzyć o następujące funkcjonalności:
Walidacja wygenerowanych poleceń shell
Dodanie możliwości wykonywania wygenerowanych poleceń
Interaktywny tryb generowania poleceń
Obsługa bardziej złożonych wzorców poleceń shell
Ta dokumentacja powinna pomóc w zrozumieniu celu i struktury projektu generatora skryptów shell. Możesz ją dostosować lub rozszerzyć w zależności od konkretnych potrzeb i wymagań projektu.

# Dokumentacja projektu DSL Builder i Shell Script Generator

## Cel projektu

Projekt składa się z dwóch głównych komponentów:
1. DSL (Domain-Specific Language) Builder - generator zdań na podstawie specyfikacji YAML.
2. Shell Script Generator - generator skryptów powłoki shell na podstawie tych samych specyfikacji YAML.

Oba komponenty korzystają z tych samych plików wejściowych, ale generują różne wyjścia.

## Pliki wejściowe

Projekt korzysta z następujących plików wejściowych:

1. `object.yaml` - zawiera specyfikację obiektów, akcji, wzorców zdań i poleceń shell.
2. `public.yaml` - zawiera publiczne dane używane do generowania zdań i poleceń.
3. `private.yaml` - zawiera prywatne dane (używane głównie przez skrypty shell, nie bezpośrednio w generowanych zdaniach).

## Komponenty projektu

### 1. DSL Builder (sentence.py)

#### Cel
Generowanie zdań na podstawie specyfikacji YAML.

#### Użycie




python query.py object.yaml private.yaml public.yaml -n 5 -o query.yaml






bash
python query.py object.yaml private.yaml public.yaml -n 5 -o query.yaml


#### Plik wyjściowy
`query.yaml` - będzie zawierał wygenerowane polecenia shell wraz z odpowiadającymi im zdaniami.

#### Proponowana struktura pliku wyjściowego




yaml
sentence: <wygenerowane zdanie>
shell: <odpowiadające polecenie shell>
sentence: <kolejne wygenerowane zdanie>
shell: <kolejne odpowiadające polecenie shell>

#### Główne funkcje do zaimplementowania
- `generate_shell_command(object_spec: Dict[str, Any], action: str, object_name: str, public_data: Dict[str, Any]) -> str`: Generowanie pojedynczego polecenia shell.
- `generate_commands(spec: Dict[str, Any], public_data: Dict[str, Any], num_commands: int) -> List[Dict[str, str]]`: Generowanie listy poleceń i odpowiadających im zdań.

## Struktura projektu


```bash
email2/
├── sentence.py
├── query.py (do zaimplementowania)
├── object.yaml
├── public.yaml
├── private.yaml
├── sentences.yaml (generowany)
└── query.yaml (do zaimplementowania)
```
## Uwagi

- Projekt jest w trakcie rozwoju. Shell Script Generator wymaga implementacji.
- Należy zwrócić uwagę na bezpieczeństwo przy generowaniu i wykonywaniu poleceń shell.
- Warto rozważyć dodanie obsługi błędów i logowania dla lepszej diagnostyki.


Ta dokumentacja powinna zostać poprawnie zapisana do pliku doc.md. Zawiera ona ogólny przegląd projektu, opis obu komponentów (istniejącego DSL Builder i planowanego Shell Script Generator), strukturę projektu, oraz sugestie dotyczące przyszłych rozszerzeń.




## Sposób uruchomienia
Run the script from the command line, specifying the YAML files 

```bash
python shell.py sentences.yaml object.yaml private.yaml public.yaml
```

```yaml
sentences:
- connect to Account email "admin@domain.com", create Message with sender "tom@domain.com"
  content "Meeting summary" subject "Weekly Report", disconnect Account email "admin@domain.com"
```
## Przykłady plików `query.yaml`

```yaml
query:
  - sentence: connect to Account email "admin@domain.com"
    shell: 
      - Account.sh connect email "admin@domain.com"
  - sentence: disconnect Account email "admin@domain.com"
    shell: 
      - Account.sh disconnect email "admin@domain.com"
  - sentence: read all Message with from "2023-12-31T01:59:59Z" to "2023-12-31" sender "alice@domain.com" subject "Weekly Report", Account email "admin@domain.com"
    shell:
      - Message.sh read all from "2023-12-31T01:59:59Z" to "2023-12-31" sender "alice@domain.com" subject "Weekly Report"
      - Account.sh email "admin@domain.com"
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

Samo `{action}` oznacza dowolne `action` z listy, ale `{action:disconnect}` oznacza tylko wybrane `action` czyli jak w przykładzie `disconnect`

parametr `object` określa w `patterns` zagnieżdzenie innego obiektu 
W ten sposób można stworzyć hierarchię budowania zdania, podmiot i przedmiot.




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
