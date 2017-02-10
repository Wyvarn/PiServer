from flask_script import Server, Manager, Shell
import os
from app import create_app

cov = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage

    # this will start running all the modules inside app, to check if all the applicaiton is being
    # sufficiently tested
    cov = coverage.coverage(branch=True, include="app/*")
    cov.start()

# create the application based on the configuration in the environment
# if the configuration is not set, it will use default setting
app = create_app(os.getenv("FLASK_CONFIG") or "default")

# pass the application object to manager and create a manager instance, to enable running the application
manager = Manager(app)
# set up a server to run at a specific port and host
server = Server(host="127.0.0.1", port=5000)


def make_shell_context():
    """
    Enables us to make a shell context within the application and run certain commands
    :return: A dictionary with the variables that will be in the shell context
    :rtype: dict
    """
    return dict(app=app)


# add the commands that will be used in the application
# run these commands with python manage.py shell/runserver/etc...
manager.add_command("shell", Shell(make_context=make_shell_context()))
manager.add_command("runserver", server)


@manager.command
def test(cover=False):
    """
    Will run tests in the application. Will run both unit tests and functional tests
    and will create a coverage report
    :param cover variable will be set to False, this will be used to coverage reports
    """
    if cover and not os.environ.get("FLASK_COVERAGE"):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    # discover the tests package
    tests = unittest.TestLoader().discover('tests')

    # run all the tests
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'coverage')

        # generate html report
        cov.html_report(directory=covdir)

        # generate xml report
        cov.xml_report()

        print('HTML version: file://%s/index.html' % covdir)
        print("XML version: file://%s" % basedir)
        cov.erase()


if __name__ == "__main__":
    manager.run()
