- skrypt do parsowania i przyporządkowania wygenerowanych zdań

## Sposób uruchomienia
Run the script from the command line, specifying the YAML files 

```bash
python parser.py sentences.yaml object.yaml private.yaml public.yaml
```

## Plik `sentences.yaml`


```yaml
sentences:
- delete last 95 Message with date sender "admin@domain.com" subject "Important Announcement"
- connect to Account email "admin@domain.com" and create Message with sender "bob@domain.com" content  "default_string" subject "Important Announcement" and disconnect Account email "tom@domain.com"
- disconnect Account email "admin@domain.com"
- create Message with sender "bob@domain.com" content "Important update" subject "Project Update"  
- connect to Account email "tom@domain.com" and read all Message with sender "admin@domain.com" subject "Important Announcement"
```
Based on generated sentences in `sentences.yaml` used with `object.yaml` create commands in shell in `script.sh`


## Plik `object.yaml`

```yaml
Message:
  patterns:
    - "{action} {many} {} with {public}"
    - "{action} {} with {public} and {object}"
    - "{action:create} {} on {public} on {object}"
  public:
    date: datetime
    sender: string
    content: string
    subject: string
  action:
    many:
      - read
      - delete
    one:
      - create
    default:
      - read
  many:
    - last: integer
    - all
  object:
    - Account

Account:
  patterns:
    - "{action:disconnect} {} {public}"
    - "{action:connect} to {} {public} and {object}"
  public:
    email: string
  private:
    server: string
    password: string
    username: string
    port: number
  action:
    one:
      - connect
      - disconnect
    default:
      - connect
    end:
      - connect
  object:
    - Message
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
