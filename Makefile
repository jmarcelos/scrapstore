create: createenv

createenv:
	test -d env_scrapstore/bin/activate || virtualenv env_scrapstore
	env_scrapstore/bin/pip install -Ur requirements.txt
	touch ./env_scrapstore/bin/activate

install-amazon:
	sudo yum install -y gcc libcurl-devel openssl-devel libxml2 libxml2-devel libxslt libxslt-devel

sitemap-all: sitemap-acom sitemap-sub sitemap-extra sitemap-netshoes

sitemap-acom:
	python scrapper/sitemap.py sitemap-read Americanas

sitemap-sub:
	python scrapper/sitemap.py sitemap-read Submarino

sitemap-extra:
	python scrapper/sitemap.py sitemap-read Extra

sitemap-netshoes:
	python scrapper/sitemap.py sitemap-read Netshoes

home-read-acom:
	python scrapper/sitemap.py product-read Americanas

clean:
	@find . -name \*.pyc -delete
	@find . -name \*.orig -delete


creategit:
	git init
	echo "# Virtualenv\n.Python\n.ini\n*.pyc\nenv_scrapstore/\n[Bb]in\n[Ii]nclude\n[Ll]ib\n[Ll]ocal\n# MacOSX\n.DS_Store" >> .gitignore


remotegit:
	git remote add web ssh://54.233.91.213/home/ec2-user/desenv

push-amazon:
	git push web +master:refs/heads/master
