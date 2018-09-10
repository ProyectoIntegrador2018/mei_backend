# MEI - Sistema Inteligente (Backend)

Desktop application to follow a process of collaborative teamwork and face-to-face dialogue following the Interpretative Structural Modeling algorithm by John Warfield.

## Table of contents

* [Client Details](#client-details)
* [Environment URLS](#environment-urls)
* [Team](#team)
* [Management tools](#management-tools)
* [Requirements](#requirements)
* [Setup the project](#setup-the-project)
* [Running the Flask server](#running-the-flask-server)


### Client Details

| Name               | Email             | Role |
| ------------------ | ----------------- | ---- |
| Graciela Caffarel Rodríguez | graciela.caffarel@itesm.mx | Product Owner |
| Luis Humberto González Guerra | lhgonzalez@itesm.mx | Client |


### Environment URLS

* **Production** - [TBD](TBD)
* **Development** - [TBD](TBD)

### Team

| Name           | Email             | Role        |
| -------------- | ----------------- | ----------- |
| Gerardo Andrés Gálvez Vallejo | A00513062@itesm.mx | Development |
| Luis Fernando Hernández Sánchez | A00815356@itesm.mx | Development |
| Barbara Berenice Valdez Mireles | A01175920@itesm.com | Development |
| David Orlando de la Fuente Garza | A00817582@itesm.mx | Development |

### Management tools

* [Github repo](https://github.com/ProyectoIntegrador2018/mei_backend)
* [Backlog](https://github.com/ProyectoIntegrador2018/mei_frontend/projects/1)
* [Heroku](https://crowdfront-staging.herokuapp.com/)
* [Documentation](https://drive.google.com/open?id=16-13j8v9uVM7V9z2Gq5vwgKBxlPyn1k9)

### Requirements
* [pip](https://pip.pypa.io/en/stable/installing/)<br/>
pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from python.org.
* [python-dotenv](https://github.com/theskumar/python-dotenv)
```bash
$ pip install --user python-dotenv
```
* [Flask](https://pypi.org/project/Flask/)
```bash
$ pip install --user Flask
```
* [flask-mysql](https://firebase.google.com/docs/admin/setup)
```bash
$ pip install --user flask-mysql
```

### Setup the project

1. Clone this repository into your local machine

```bash
$ git clone git@github.com:ProyectoIntegrador2018/mei_backend.git
```

2. Step into the ElectronFlaskTest directory
```bash
$ cd ElectronFlaskTest
```

3. Create a file called `.env` inside the ElectronFlaskTest directory and fill it with the following environment variables set to the MySQL configuration of your liking.
```
MYSQL_DATABASE_USER=example
MYSQL_DATABASE_PASSWORD=example
MYSQL_DATABASE_DB=example
MYSQL_DATABASE_HOST=example
```

### Running the Flask server

1. Start the server
```bash
$ python hello.py
```

You should see the following output:
```bash
 * Serving Flask app "hello"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

This means that the server is up and running.

**Take note that if you kill this process you will kill the web service, and you will probably need to lift it up again.**
