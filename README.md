# Run
Run any language code with input and output file.


## Currently supported languages
- C
- C++
- Python


## Pre-requisites
- Python 3

Download latest version of python from [here](https://www.python.org/downloads/)


## Installation with git clone
```bash
$ git clone https://github.com/shhossain/run
$ cd run
$ python setup.py
```

## Installation with zip file
**Steps**:
1. Download the zip file from [here](https://github.com/shhossain/run/archive/refs/heads/main.zip)
2. Extract the zip file
3. Open terminal and go to the extracted folder
4. Run the following command
```bash
$ python setup.py
```


## Usage

### Install a language
```bash
$ run install <language>
```

```bash
$ run install python 3.11.0
```


### Run a code
```bash
$ run hello.py
```

```bash
$ run hello.cpp
```

__Note: Supported python, c++, c__



### Run a code with input file [Any text file is supported]
```bash
$ run hello.py -i input.tx
```

```bash
$ run hello.cpp -i input.txt
```


### Run a code with output file [Any text file is supported]
```bash
$ run hello.py -o output.txt
```


### Run a code with input and output file [Any text file is supported]
```bash
$ run hello.py -i input.txt -o output.txt
```


### Run a code with expected output file [Any text file is supported]
```bash
$ run hello.py -e expected.txt
```


### Run a code with time limit [in seconds]
```bash
$ run hello.py -t 2
```
__Note: `2` here is in seconds__ 



