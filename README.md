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

### Start the database

cd to the database folder and run the following command:

```bash
docker-compose up
```

### Start the server

prerequisites:
- Database is running

cd to the server folder and run the following command:

```bash
docker-compose up
```

### Start the client

prerequisites:
- Database is running
- Server is running

cd to the client folder and run the following command:

```bash
docker-compose up
```

Play Manually:

Activate the virtual environment and run the following command:

```bash
python client.py --player
```

Build & Run the automated client container:

1. cd to the client folder and run the following command:

2. build the client container with the command:

```bash
docker build -t client .
```

3. run the automated client container with the command:

```bash
docker run -it client
```


