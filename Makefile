IW_REPO="https://tangingw@bitbucket.org/tangingw/python_winprint.git"

install_ubuntu:
	apt-get update
	apt-get install -y python-pip git
	pip install --upgrade pip
	pip install redis pyPDF2 requests

install: install_ubuntu
	git clone $(IW_REPO)

clean:
	rm *.pyc