create: createenv

createenv:
	test -d env_scrapstore/bin/activate || virtualenv env_scrapstore
	env_scrapstore/bin/pip install -Ur requirements.txt
	touch ./env_scrapstore/bin/activate

sitemap-acmm:
	python scrapper/sitemap.py sitemap-read Americanas

sitemap-sub:
	python scrapper/sitemap.py sitemap-read Submarino

sitemap-extra:
	python scrapper/sitemap.py sitemap-read Extra

sitemap-netshoes:
	python scrapper/sitemap.py sitemap-read Netshoes

clean:
	@find . -name \*.pyc -delete
	@find . -name \*.orig -delete


creategit:
	git init
	echo "# Virtualenv\n.Python\n.ini\n*.pyc\nenv_scrapstore/\n[Bb]in\n[Ii]nclude\n[Ll]ib\n[Ll]ocal\n# MacOSX\n.DS_Store" >> .gitignore
