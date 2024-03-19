from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create a manager instance
manager = Manager(app)

# Add Flask-Migrate commands to the manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
