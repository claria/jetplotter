# Declaration of variables
PLOTDIR = plots

# File names
SOURCES = $(wildcard $(PLOTDIR)/*.json)
TARGETS = $(SOURCES:.json=.png)

.PHONY : all
all : $(TARGETS)

# To obtain object files
%.png: %.json
	./plotter.py -l $< 

# To remove generated files
clean:
	rm -f $(EXEC) $(TARGETS)
