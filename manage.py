from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from jobs_board.core import create_app, db

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
