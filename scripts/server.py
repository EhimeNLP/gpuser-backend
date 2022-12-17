import subprocess


def main():
    cmd = ["python", "manage.py", "runserver", "0.0.0.0:8001"]
    subprocess.run(cmd)
