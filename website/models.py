from . import db
from sqlalchemy.sql import func

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    release_date = db.Column(db.Date)
    genres = db.Column(db.String(255))
    platforms = db.relationship('GamePlatform', backref='game', lazy=True)

    def __repr__(self):
        return f"Game(id={self.id}, title={self.title})"

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255))
    games = db.relationship('GamePlatform', backref='platform', lazy=True)

    def __repr__(self):
        return f"Platform(id={self.id}, name={self.name})"

class GamePlatform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=False)
    price = db.Column(db.Float)

    def __repr__(self):
        return f"GamePlatform(id={self.id}, game_id={self.game_id}, platform_id={self.platform_id}, price={self.price})"
