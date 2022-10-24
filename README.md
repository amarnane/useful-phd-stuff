# useful-phd-stuff
Tips and tricks for working with python for the phd. 

See `docs` for some markdown files explaining different concepts. Currently only one on remote working.
I will add one on saving your code as source code and how to access it anywhere by making your own python packag using setuptools.

(this repo is an example but I will write a guide explaining steps soon)

I have added some functions I wrote that I find really useful for creating experiments, plotting and moving files around.
I'll also try a guide explaining when I use these functions and why I find them helpful.
## Python helper functions
To install package use 
```bash
pip install .
```

You can then import these helper functions in your code using
```Python
import useful_phd as usp

usp.set_science_style()
usp.create_experiment()
```


If you want to change the functions install in developer mode 
```
pip install -e .
```
