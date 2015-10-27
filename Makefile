create: createenv

createenv:
	test -d env_scrapstore/bin/activate || virtualenv env_scrapstore
	env_scrapstore/bin/pip install -Ur requirements.txt
	touch ./env_scrapstore/bin/activate

install-amazon:
	sudo yum install -y gcc libcurl-devel openssl-devel libxml2 libxml2-devel libxslt libxslt-devel



sitemap-all: sitemap-americanas sitemap-sub sitemap-extra sitemap-netshoes

sitemap-americanas:
	python scrapper/sitemap.py sitemap-read Americanas

sitemap-sub:
	python scrapper/sitemap.py sitemap-read Submarino

sitemap-extra:
	python scrapper/sitemap.py sitemap-read Extra

sitemap-netshoes:
	python scrapper/sitemap.py sitemap-read Netshoes

home-read-all: home-read-americanas home-read-submarino home-read-netshoes home-read-extra

home-read-americanas:
	python scrapper/sitemap.py product-read Americanas

home-read-submarino:
	python scrapper/sitemap.py product-read Submarino

home-read-netshoes:
	python scrapper/sitemap.py product-read Submarino

home-read-extra:
	python scrapper/sitemap.py product-read Submarino

update-product-all: update-product-americanas update-product-submarino update-product-extra update-product-netshoes

update-product-americanas:
	python scrapper/sitemap.py product-update Americanas

update-product-submarino:
	python scrapper/sitemap.py product-update Submarino

update-product-extra:
	python scrapper/sitemap.py product-update Extra

update-product-netshoes:
	python scrapper/sitemap.py product-update Netshoes


clean:
	@find . -name \*.pyc -delete
	@find . -name \*.orig -delete

creategit:
	git init
	echo "# Virtualenv\n.Python\n*.log\n*.ini\n*.pyc\nenv_scrapstore/\n[Bb]in\n[Ii]nclude\n[Ll]ib\n[Ll]ocal\n# MacOSX\n.DS_Store" >> .gitignore

remotegit:
	#http://www.jeffhoefs.com/2012/09/setup-git-deploy-for-aws-ec2-ubuntu-instance/
	git remote add deploy ssh://54.94.137.137/home/ec2-user/desenv

deploy-amazon:
	git push deploy +master:refs/heads/master
