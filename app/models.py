from app.manage import db,app

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
    
class Conversations(db.Model):
    __tablename__ = 'conversations'

    cookie = db.Column(db.String(1024), primary_key=True)
    currentBernard = db.Column(db.String(1024))
    currentRobert = db.Column(db.String(1024))
    currentJacques = db.Column(db.String(1024))
    

    def __repr__(self):
        return '<Cookie %r>' % (self.cookie)
