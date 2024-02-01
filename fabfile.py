from fabric import Connection, Config
from fabric.tasks import task
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.server_env')
load_dotenv(dotenv_path)



# PASSPHRASE
kwargs = {'passphrase': os.getenv("LOCAL_PASSPHRASE"),}


# CONFIGURATION
config = Config(overrides={'sudo': {'password': os.getenv("SERVER_SUDO_PASSWORD")}})

# LOCAL DIRECTORIES
local_project_root = os.path.dirname(os.path.abspath(__file__))
local_project_dir = os.path.join(local_project_root, os.getenv("LOCAL_PROJECT_DIR_NAME"))
local_project_env = os.path.join(local_project_root, 'ENV/bin/activate')

# SERVER CONNECTION
server_ip = os.getenv("SERVER_IP")
server_user = os.getenv("SERVER_USER")

# SERVER DIRECTORIES
production_project_div = os.getenv("PRODUCTION_PROJECT_DIR")
production_project_env = os.getenv("PRODUCTION_PROJECT_ENV_ACTIVATION_PATH")
staging_project_dir = os.getenv("STAGING_PROJECT_DIR")
staging_project_env = os.getenv("PRODUCTION_PROJECT_ENV_ACTIVATION_PATH")
frontend_project_div = os.getenv('FRONTEND_PROJECT_DIR')
# LOCAL

@task()
def local_pull(c):
    """Pulls the latest code from the repository, installs requirements and migrates the database
    Command: fab local-pull
    """
    with c.cd(local_project_root):
        with c.prefix(f"source {local_project_env}"):
            c.run('git pull')
            c.run('pip install -r requirements.txt')
            with c.cd(local_project_dir):
                c.run('python manage.py migrate')


@task()
def local_push(c):
    """Adds everything in requirements.txt, and pushes the latest code to the repository
    Command: fab local-push
    """
    with c.cd(local_project_root):
        with c.prefix(f"source {local_project_env}"):
            c.run('pip freeze > requirements.txt')
            c.run('git add -A')
            commit_message = input("Enter a commit message: ")
            print(f"Commit message: {commit_message}")
            c.run(f'git commit -m "{commit_message}" ')
            c.run('git push')


# SERVER 
@task
def staging_deploy(c):
    """
    deploys local to production
    Command: fab staging-deploy
    """
    con = Connection(f'{server_user}@{server_ip}', connect_kwargs=kwargs, config=config)
    with con.cd(f"{staging_project_dir}"):
        con.run("git pull origin staging", pty=True)

        with con.prefix(f"source {staging_project_env}"):
            con.run("pip install --upgrade pip")
            con.run("pip install -r ../requirements.txt")
            con.run("python manage.py migrate")
            con.run("python manage.py collectstatic --noinput")

    con.sudo("systemctl restart gunicorn-staging", pty=True)
    con.sudo("systemctl reload nginx", pty=True)


@task
def production_deploy(c):
    """
    deploys local to production
    Command: fab production-deploy
    """
    con = Connection(f'{server_user}@{server_ip}', connect_kwargs=kwargs, config=config)
    print(f"{production_project_div}")
    with con.cd(f"{production_project_div}"):
        con.run("git pull origin main", pty=True)

        with con.prefix(f"source {production_project_env}"):
            con.run("pip install --upgrade pip")
            con.run("pip install -r ../requirements.txt")
            con.run("python manage.py migrate")
            con.run("python manage.py collectstatic --noinput")

    con.sudo("systemctl restart gunicorn", pty=True)
    con.sudo("systemctl reload nginx", pty=True)

@task 
def frontend_deploy(c):
    con = Connection(f'{server_user}@{server_ip}', connect_kwargs=kwargs, config=config)
    print("Deploying frontend")
    with con.cd(f"{frontend_project_div}"):
        con.run("git pull origin main", pty=True)
        con.run("npm install")
        con.run("npm run build")
    con.sudo("systemctl reload nginx", pty=True)


@task
def restartservers(c):
    print("Restarting servers")
    con = Connection(f'{server_user}@{server_ip}', connect_kwargs=kwargs, config=config)
    con.sudo("systemctl restart gunicorn", pty=True)
    con.sudo("systemctl reload nginx", pty=True)