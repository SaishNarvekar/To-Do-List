from flask import Flask

app = Flask(__name__)
app.secret_key = "82bfce4d0166155f1dd8524112584fb1"

import todolist.routes
import todolist.connection
import todolist.session
import todolist.auth