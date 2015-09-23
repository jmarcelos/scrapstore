create: createenv

createenv:
	test -d env_scrapstore/bin/activate || virtualenv env_scrapstore
	env_scrapstore/bin/pip install -Ur requirements.txt
	touch ./env_scrapstore/bin/activate


creategit:
	git init
	echo "# Virtualenv\n.Python\n.ini\n*.pyc\nenv_scrapstore/\n[Bb]in\n[Ii]nclude\n[Ll]ib\n[Ll]ocal\n# MacOSX\n.DS_Store" >> .gitignore
