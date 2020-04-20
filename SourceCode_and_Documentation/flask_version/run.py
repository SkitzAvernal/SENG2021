from routes import app

from app import app, db 
from models import User 

@app.shell_context_processor 
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True, port = 5000)
