.PHONY: help book clean serve

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  book        to convert the content/ folder into Jekyll markdown in _build/"
	@echo "  clean       to clean out site build files"
	@echo "  deploy      copy to the lab website"


book:
	jupyter-book build ./
	cp -r lectures _build/html/
	cp -r images _build/html/
	cp -r data _build/html/
	cp -r scripts _build/html/
	cp -r chapters/02/images _build/html/chapters/02/
	cp -r chapters/03/images _build/html/chapters/03/
	cp -r chapters/05/images _build/html/chapters/05/
	cp -r chapters/06/images _build/html/chapters/06/
	cp -r chapters/07/images _build/html/chapters/07/
# 	cp -r chapters/19/images _build/html/chapters/19/
	cp chapters/24/zipall.ipynb _build/html/chapters/24/
	cp -r chapters/24/images _build/html/chapters/24/
clean:
	jb clean .

deploy:
	rsync -va _build/html/ gureckis_lab@gureckislab.org:/home/gureckis_lab/gureckislab.org/courses/spring21/labincp/