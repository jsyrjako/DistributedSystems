# DistributedSystems
Distributed Systems course


| Name             | Student ID | Email                      |
| ---------------- | ---------- | -------------------------- |
| Janne Yrjänäinen | Y58554010  | jyrjanai20@student.oulu.fi |
| Joona Syrjäkoski | Y58172266  | jsyrjako20@student.oulu.fi |
| Joonas Ojanen    | 2305882    | jojanen20@student.oulu.fi  |
| Lasse Rapo       | Y58553703  | lrapo20@student.oulu.fi    |


## Virtual environment
### Create virtual environment

```bash
python3 -m venv venv
```

### Activate virtual environment

Linux / macOS
```bash
source venv/bin/activate
```
or on Windows (CMD)
```bash
venv\Scripts\activate.bat
```
or on Windows (PowerShell)
```bash
venv\Scripts\Activate.ps1
```

### Deactivate virtual environment

```bash
deactivate
```

### Install dependencies

```bash
pip install -r requirements.txt
```


## Running the application

### Start the server

cd to the server folder and run the following command:

```bash
docker-compose up
```

### Start the client

cd to the client folder and run the following command:

```bash
docker-compose up
```

Play Manually:

prerequisites:
- server is running
- venv is activated

```bash
python client.py --kayttaja
```

