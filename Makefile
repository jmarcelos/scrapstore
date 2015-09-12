create: createenv

createenv:
	virtualenv env_scrapstore
	pip install -r requirements.txt

creategit:
	git init
	echo "# Virtualenv\n.Python\n[Bb]in\n[Ii]nclude\n[Ll]ib\n[Ll]ocal\n# MacOSX\n.DS_Store" >> .gitignore
