import subprocess
import sys
import importlib.metadata as metadata

def check_and_install_package(package_name, desired_version):
    try:
        installed_version = metadata.version(package_name)
        if installed_version != desired_version:
            print(f"Versão {installed_version} de {package_name} encontrada, mas a versão {desired_version} é necessária.")
            subprocess.run([sys.executable, "-m", "pip", "install", f"{package_name}=={desired_version}"])
            subprocess.run([sys.executable, "-m", "pip", "install", "bcrypt"])
            subprocess.run([sys.executable, "-m", "pip", "install", "mysqlclient"])
        else:
            print(f"{package_name} está instalado e na versão correta.")
    except metadata.PackageNotFoundError:
        print(f"{package_name} não está instalado. Instalando a versão {desired_version}.")
        subprocess.run([sys.executable, "-m", "pip", "install", f"{package_name}=={desired_version}"])
        subprocess.run([sys.executable, "-m", "pip", "install", "bcrypt"])
        subprocess.run([sys.executable, "-m", "pip", "install", "mysqlclient"])

        





def create_database():
    porta_alternativa = "3308"
    senha = "mysqlfatec"  # Substitua pela sua senha real

    subprocess.run(["C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysql", "-u", "root", "-pmysqlfatec", "-P", porta_alternativa, "-e", "CREATE DATABASE lanches;"])
    subprocess.run(["python", r"C:\Users\aluno\Downloads\ecommercedjango\ecommerce\manage.py", "migrate"])
    #subprocess.run(["C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysql", "-u", "root", "-p" + senha, "-P", porta_alternativa, "-e", "INSERT INTO lanches.useradmin (email_cifrado, senha_hash) VALUES ('admin2', SHA2('Admin2', 256));"])
    subprocess.run(["C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysql", "-u", "root", "-p" + senha, "-P", porta_alternativa, "-e", "INSERT INTO useradmin (email_cifrado, senha_hash, last_login) VALUES ('admin', SHA2('Admin123', 256), NOW());"])





if __name__ == "__main__":
     check_and_install_package("django", "3.2.12")
     create_database()


