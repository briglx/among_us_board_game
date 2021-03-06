# Among us board game Simulator

Project to simulate the board game Among Us. The project has a simulator and a genetic algorithm used to optimize game play.

# Rule Questions

- Can an imposter kill when not their turn?
    - On a crews turn they draw a room where the imposter is. Can the imposter kill as soon as they enter the room or wait until the imposters turn.
    - Answer: Yes. If a crew walks into a room where the imposter the imposter can kill 

# Sample Trials

```
Sample Trials

[
   1., 1., 0., 1.,  # 14 players
   0., 1., 1.,      # 7 imposters
   0., 0., 0.,      # Default 1 body
   0., 1., 0.,      # 5 Rooms
   1., 1., 0., 1.,  # 14
   0.,0., 0.,       # 0 duplicate rooms
   1.,              # Ladder
   1., 0.,          # 2
   0., 0., 1., 0.,  # 7 chances
   1., 0., 0., 0.,  # 1 reward
   1., 0., 0., 0.,  # 1 risk
   0., 1., 0., 1.,  # 10 reward
   0., 0., 0., 0.   # 0  risk

] = .982


[ 
    0., 1., 0., 0.,  # 5 players      
    1., 1., 0.,      # 4 imposters
    1., 0., 0.,      # 2 bodies
    0., 1., 0.,      # 5 rooms
    0., 1., 0., 0.,  # 5 cards
    1., 0., 1.,      # 5 duplicate rooms
    0.,              # Even
    0., 0.,          # 1
    1., 0., 1., 1.,  # 13 chances
    1., 1., 1., 0.,  # 7 reward
    0., 0., 0., 0.,  # 0 risk
    0., 1., 0., 0.,  # 2 reward
    1., 1., 1., 0.   # 7 risk
    ] = 0.68446739
```

# Development

The development environment is to manages two types of environments:

- Python Generator Code
- Azure Resources

## Python Generator code

Setup your dev environment by creating a virtual environment

```bash
# virtualenv \path\to\.venv -p path\to\specific_version_python.exe
python3 -m venv .venv
source .venv/bin/activate

deactivate
```

## Style Guidelines

This project enforces quite strict [PEP8](https://www.python.org/dev/peps/pep-0008/) and [PEP257 (Docstring Conventions)](https://www.python.org/dev/peps/pep-0257/) compliance on all code submitted.

We use [Black](https://github.com/psf/black) for uncompromised code formatting.

Summary of the most relevant points:

- Comments should be full sentences and end with a period.
- [Imports](https://www.python.org/dev/peps/pep-0008/#imports) should be ordered.
- Constants and the content of lists and dictionaries should be in alphabetical order.
- It is advisable to adjust IDE or editor settings to match those requirements.


### Use new style string formatting

Prefer [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) over ``%`` or ``str.format``.

```python
#New
f"{some_value} {some_other_value}"
# Old, wrong
"{} {}".format("New", "style")
"%s %s" % ("Old", "style")
```

One exception is for logging which uses the percentage formatting. This is to avoid formatting the log message when it is suppressed.

```python
_LOGGER.info("Can't connect to the webservice %s at %s", string1, string2)
```

### Testing

```bash
pip3 install -r requirements_dev.txt

# Install this module for development
pip3 install -e .
```

Now that you have all test dependencies installed, you can run linting and tests on the project:

```bash
isort .
codespell --skip=".venv"
black main.py among_us tests setup.py
flake8 main.py among_us tests setup.py
pylint main.py among_us tests setup.py
pydocstyle main.py among_us tests setup.py
python -m pytest --cov-report term-missing --cov=among_us
pytest tests


```

# References
- Genetic Algorithm https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/
- An Introduction to Genetic Algorithms By Melanie Mitchell https://www.boente.eti.br/fuzzy/ebook-fuzzy-mitchell.pdf
- Error threshold (Evolution) https://en.wikipedia.org/wiki/Error_threshold_(evolution)
