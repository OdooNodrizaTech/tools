Permite la integración con github para copiar los repositorios

Se añade en Configuración > Técnico > Git el apartado de Repositorios y Autores.
En 1º lugar deberíamos añadir un autor (por ejemplo ONT) para luego crear un repositorio de ese autor y definir datos como:

Url: 	git@github.com:OdooNodrizaTech/website.git
Path: /home/ubuntu/odoo_addons/ont/website
Branch: 10.0

De esta forma, usando las URLS públicas se guardará un log de la acción correspondiente y se realizará el git clone del repositorio en cuestión.

## Requisitos:

### 1-Creación de SSH Key

Ejecutaremos el siguiente comando en consola
```
ssh-keygen -t rsa -b 2048 -C "your@email.com"
```

Definiremos la ruta /home/ubuntu/.ssh/odoo en el paso siguiente para después NO definir ninguna contraseña

### 2-Creación de SSH en Github

Iremos a github.com al apartado Profile > SSH y pulsaremos en New SSH Key con los siguientes datos:
Title: odoo
Key: (el contenido del archivo /home/ubuntu/.ssh/odoo.pub creado en el paso anterior)

### 3-Copiar archivo odoo_git.sh
Crearemos el archivo odoo_git.sh en /home/ubuntu/odoo_addons/odoo_git.sh con el siguiente contenido.

## odoo_git.sh
```
#!/bin/sh
git_branch=$1
git_url=$2
odoo_path=$3
odoo_restart=$4
#echo
echo "Git branch: "$git_branch
echo "Git url: "$git_url
echo "Odoo path: "$odoo_path
echo "Odoo restart: "$odoo_restart
#create_dir (previously_remove)
rm -rf $odoo_path
mkdir $odoo_path
chown ubuntu: $odoo_path
cd $odoo_path
#ssh
eval "$(ssh-agent -s)"
ssh-add /home/ubuntu/.ssh/odoo
#git
git clone -b $git_branch $git_url
#retart_odoo
if [ $odoo_restart = "True" ]
then 
echo "Restarting odoo"
sudo service odoo restart
fi
```


Fuente: https://www.pixelstech.net/article/1562943243-Resolve-git-issue-git%40github-com%3A-Permission-denied-%28publickey%29

Fuente: https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
