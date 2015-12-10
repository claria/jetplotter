# Declaration of variables
PLOTDIR = plots
CONFIGDIR = configs

# File names
SOURCES = $(wildcard $(CONFIGDIR)/*.json)
TARGETS = $(SOURCES:.json=.png)

REMOTE = sieber@ekplx77.physik.uni-karlsruhe.de
REMOTE_DIR = public_html/private/plots/
FOLDERNAME := $(shell date "+%Y_%m_%d_%H_%M")


.PHONY : all clean web
all : $(TARGETS)

# To obtain object files
%.png: %.json
	./plot.py -l $< 

%.json: 
	./plot.py -l $@ 

%.py: 
	./plot.py -l $@ 


web:
	ssh $(REMOTE) "mkdir -p $(REMOTE_DIR)/$(FOLDERNAME)"
	scp $(TARGETS) "$(REMOTE):$(REMOTE_DIR)/$(FOLDERNAME)/"
	ssh $(REMOTE) "$(REMOTE_DIR)/prep_gallery.py"
	@echo "go to web gallery."


# To remove generated files
clean:
	rm -f $(EXEC) $(TARGETS)
