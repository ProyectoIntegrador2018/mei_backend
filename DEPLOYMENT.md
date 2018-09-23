# Deployment
[PythonAnywhere](https://www.pythonanywhere.com) will be used to host our backend services. You'll to create an account to deploy the API.

## Steps
1. In the Dashboard open a console and create a virtual environment usnig Python 3.6
```bash
$ mkvirtualenv --python=/usr/bin/python3.6 my-virtualenv
```

2. Install all the dependencies
```bash
$ pip install flask python-dotenv flask-mysql flask-bcrypt flask-cors
```

3. Go to the the **Web tab** and select **Add a new web app** > **Manual Configuration**, and choose **Python 3.6**
4. Go to the the **File tab** and upload `hello.py`. It will be placed in */home/yourusername/mysite/hello.py*
5. Go to the web app dashboard and under the **Code** section select the WSGI configuration file and place the following contents:
```python
import sys
import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('/home/gerardogalvez/mysite')
load_dotenv(os.path.join(project_folder, '.env'))

path = '/home/gerardogalvez/mysite'

if path not in sys.path:
   sys.path.append(path)

from hello import app as application
```

6. Go to the **Databases** section and type in a password if prompted. Then create a new MySQL database and start a console on it.
7. Once in the MySQL console type in the contents of the `db.sql` file (or copy & paste them) to create the database.
8. Create the `.env` file in */home/yourusername/mysite/* and include the following variables. Under the **Databases tab** you'll find the **Database host address** (MYSQL_DATABASE_HOST) and the **Username** (MYSQL_DATABASE_USER). MYSQL_DATABASE_DB should be set to `[your username]$[database name]` and MYSQL_DATABASE_PASSWORD is the password you typed in step 6.
```
MYSQL_DATABASE_USER=example
MYSQL_DATABASE_PASSWORD=*********
MYSQL_DATABASE_DB=example
MYSQL_DATABASE_HOST=example
```
Your backend servide should now be up and running!

* Note: On your [`main.js`](https://github.com/ProyectoIntegrador2018/mei_frontend/blob/production/ElectronsFlaskTest/js/main.js) you'll need to set the `server_url` variable to your Python Anywhere webapp. For example:
```js
let server_url = 'http://gerardogalvez.pythonanywhere.com'

