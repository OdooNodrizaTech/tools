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
#!/bin/bash
git_branch=$1
git_url=$2
git_repository="$(echo $git_url | sed -r 's/.+\/([^.]+)(\.git)?/\1/')"
odoo_path=$3
odoo_restart=$4
folders_exclude_string=$5
odoo_url_finish=$6
#echo
echo "USER: "$USER
echo "Git branch: "$git_branch
echo "Git url: "$git_url
echo "Git repository: "$git_repository
echo "Odoo path: "$odoo_path
echo "Odoo restart: "$odoo_restart
echo "Odoo url_finish: "$odoo_url_finish
#define
odoo_path_repository="$odoo_path/$git_repository"
#enter odoo_path
cd $odoo_path
#remove odoo_path_repository
rm -rf $odoo_path_repository
echo "Removing folder $odoo_path_repository"
#ssh
eval "$(ssh-agent -s)"
ssh-add /home/ubuntu/.ssh/odoo
#git
git clone -b $git_branch $git_url
echo "Cloning $git_url $git_branch"
#change to ubuntu
#chown ubuntu: $odoo_path_repository
#echo "Change chwon to ubuntu $odoo_path_repository"
#remove folders
if [ $folders_exclude_string ]
then
for folder_exclude in $(echo $folders_exclude_string | tr "," "\n")
do
odoo_path_repository_exclude="$odoo_path_repository/$folder_exclude"
rm -rf $odoo_path_repository_exclude
echo "Removing folder $odoo_path_repository_exclude" 
done
fi
#retart_odoo
if [ $odoo_restart = "True" ]
then 
echo "Restarting odoo"
sudo service odoo restart
fi
#curl odoo_url_finish
if [ $odoo_url_finish ]
then
curl -s $odoo_url_finish > /dev/null
echo "Curl $odoo_url_finish"
fi
```


Fuente: https://www.pixelstech.net/article/1562943243-Resolve-git-issue-git%40github-com%3A-Permission-denied-%28publickey%29

Fuente: https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
