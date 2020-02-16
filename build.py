import os
import sys
import shutil
import sqlite3
from zipfile import ZipFile


def get_arg1():
    try:
        arg = sys.argv[1]
    except:
        print("please specify arg!")
        exit()
    return arg.lower()


def get_arg2():
    try:
        arg = sys.argv[2]
    except:
        print("please specify the package name!")
        exit()
    return arg


def get_arg3():
    try:
        arg = sys.argv[3]
    except:
        print("please specify the package version!")
        exit()
    return arg



def archive():
    try:
        os.mkdir(f"archives")
    except:
        pass
    try:
        os.mkdir(f"archives/{get_arg2()}")
    except:
        pass

    try:
        with ZipFile(f'archives/{get_arg2()}/{get_arg2()}-{get_arg3()}.zip', 'w') as zipObj:
            for folderName, __, filenames in os.walk("dist"):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath)
            for folderName, __, filenames in os.walk("build"):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath)
            for folderName, __, filenames in os.walk(f"PYRMC/{get_arg2()}"):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath)

    except Exception as e:
        print(e)


def clean():
    try:
        shutil.rmtree(f"{get_arg2()}.egg-info")
        shutil.rmtree(f"dist")
        shutil.rmtree(f"build")
    except:
        pass
    if get_arg1() == "cleanall":
        try:
            shutil.rmtree("cache")
            shutil.rmtree("__pycache__")
        except:
            pass


def build():
    try:
        os.remove(".setupinfo.db3")
    except:
        pass
    conn = sqlite3.connect(".setupinfo.db3")
    c = conn.cursor()
    c.execute(f'CREATE TABLE info (name text, version text)')
    c.execute(f'INSERT INTO info VALUES ("{get_arg2()}","{get_arg3()}")')
    conn.commit()
    c.close

    archive()
    clean()
    os.system("python3 -m pip install --user --upgrade setuptools wheel")
    os.system("python3 setup.py sdist bdist_wheel")
    os.system("python3 -m pip install --user --upgrade twine")
    os.system("python3 -m twine upload dist/* --verbose")
    if "publishac" in get_arg1():
        clean()
        try:
            os.remove(".setupinfo.db3")
        except:
            pass


def main():
    if get_arg1() == "help":
        print(
            """\npublish+ package_name+version: to publish\n\n
            clean + package_name: to clean\n\n
            cleanall+ package_name: clean all \"cache\" and \"__pycache__\"\n\n
            archive +package_name+ version: archive your code to make it easy to rollback\n\n
            publishAC+ package_name+version: archive your code publish and clean the scrap after""")
    elif "clean" in get_arg1():
        clean()
    elif "publish" in get_arg1():
        build()
    elif "archive" in get_arg1():
        archive()


if __name__ == '__main__':
    main()
