# flask-app
Flask App for CIS4930 Project



# Set up instructions
### Linux / Mac
Open a terminal and cd (change directory) into the directory where you would like to save the project
On github.com, copy the ssh link on the repos main site. 
then in terminal type
```
git clone {paste the link you previous copied here}
```
now type
```
cd /flask-app

pip install --upgrade pip
pip install requirements.txt

export FLASK_APP=web
export FLASK_ENV=development

flask init-db
flask run
```

### Windows
#### If you do not have python3 and pip installed on your computer please follow instructions online to install it
Download github desktop if you don't have it
On github.com, click "Clone with github desktop" and follow the instructions to clone the repo
Now open command prompt on windows and cd (change directory) into the directory where you cloned the repo
You should be in a directory like some/directory/path/flask-app
Now type
```
set FLASK_APP=web
set FLASK_ENV=development

pip install --upgrade pip 
pip install requirements.txt

flask init-db
flask run
```


### Note
#### I am trying to set up a docker environment so that you guys do not need to install anything, but I keep running into errors.
#### Once I do that, I will let you know and it will make the set up much easier.
