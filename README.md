# MEI - Sistema Inteligente (Frontend)

Desktop application to follow a process of collaborative teamwork and face-to-face dialogue following the Interpretative Structural Modeling algorithm by John Warfield.

## Table of contents

* [Client Details](#client-details)
* [Environment URLS](#environment-urls)
* [Team](#team)
* [Management resources](#management-tools)
* [Setup the project](#setup-the-project)
* [Running the Flask server](#running-the-flask-server)
* [Running the Electron app](#running-the-electron-app)


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

* [Github repo](https://github.com/ProyectoIntegrador2018/mei_frontend)
* [Backlog](https://github.com/ProyectoIntegrador2018/mei_frontend/projects/1)
* [Heroku](https://crowdfront-staging.herokuapp.com/)
* [Documentation](https://drive.google.com/open?id=16-13j8v9uVM7V9z2Gq5vwgKBxlPyn1k9)

## Development

### Setup the project

1. Clone this repository into your local machine

```bash
$ git git@github.com:ProyectoIntegrador2018/mei_frontend.git
```

2. Step into the ElectronFlaskTest directory
```bash
$ cd ElectronFlaskTest
```

### Running the Flask server

1. Set the FLASK_APP environment variable

#### OSX
```bash
$ export FLASK_APP=hello.py
```

#### Windows
```bash
$ set FLASK_APP=hello.py
```

This means the project is up and running.

2. Start the server
```bash
$ flask run
```

You should see the following output:
```bash
 * Serving Flask app "hello"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

This means that the server is up and running.

**Take note that if you kill this process you will kill the web service, and you will probably need to lift it up again.**

### Running the Electron app
```bash
$ npm start
```
