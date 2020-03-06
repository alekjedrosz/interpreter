# Programming language interpreter
A simple tree-walk programming language interpreter. The language includes variable scopes, data types, built-in functions, string / numerical / boolean expressions and control flow.

## Installing dependencies
This program is written in Python 3.7. Please use [pip](https://pip.pypa.io/en/stable/) package manager to install the necessary dependencies (it is recommended to install them in a virtual environment like venv).

Installation using pip:
```bash
cd [project_directory]
pip install -r requirements.txt
```

## Grammar 
A context-free grammar for this language is included in grammar.txt.

## Sample programs 
Examples of usage can be found in the examples directory.

## Running a program
To run a program please execute the following command.

```bash
python interpreter.py [program_filename].txt
```