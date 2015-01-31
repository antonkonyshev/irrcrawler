SPIDER=irr
PROJECTDIR=uaz
SOURCES=uaz/uaz/pipelines.py uaz/uaz/processor.py uaz/uaz/settings.py uaz/uaz/models.py uaz/uaz/items.py uaz/uaz/handlers.py uaz/uaz/__init__.py uaz/uaz/spiders/__init__.py uaz/uaz/spiders/irr_spider.py
CONFIGS=.gitignore.default uaz/scrapy.cfg.default uaz/uaz/settings.py.default
LOGDIR=logs
LOGNAME=$(LOGDIR)/current.log

.PHONY: clean start deploy_configs test all

all: test

clean:
	rm -rf $(LOGDIR) $(PROJECTDIR)/$(PROJECTDIR)/*.pyc $(PROJECTDIR)/$(PROJECTDIR)/tests/*.pyc

$(LOGDIR):
	mkdir $(LOGDIR)
$(LOGNAME): $(LOGDIR)
	touch $(LOGNAME)

env: env/bin/activate
env/bin/activate: requirements.txt
	test -d env || virtualenv env
	. env/bin/activate; pip install -Ur requirements.txt
	touch env/bin/activate

start: $(SOURCES) $(LOGNAME) env
	. env/bin/activate; cd $(PROJECTDIR); nohup scrapy crawl $(SPIDER) &> ../$(LOGNAME) &

deploy_configs: $(CONFIGS)
	$(shell for config in $(CONFIGS); do cp -n "$${config}" "$${config%.default}"; done)

test: env
	. env/bin/activate; PYTHONPATH=$(PROJECTDIR) python -m unittest discover -v -s $(PROJECTDIR)
