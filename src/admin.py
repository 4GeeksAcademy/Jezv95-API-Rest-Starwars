import os
from flask_admin import Admin
from models import db, User,Planet,People,Favourites_Planet,Favourites_people
from flask_admin.contrib.sqla import ModelView

class FavoritePeopleAdmin(ModelView):
    column_list = ('id', 'user', 'people')
    form_columns = ('user', 'people')

class FavoritePlanetAdmin(ModelView):
    column_list = ('id', 'user', 'planet')
    form_columns = ('user', 'planet')




def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(FavoritePeopleAdmin(Favourites_people, db.session))
    admin.add_view(FavoritePlanetAdmin(Favourites_Planet, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))