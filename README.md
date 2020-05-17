# Guruguru Cli

guruguru cli is a command line tool to use guruguru https://www.guruguru.ml/ conveniently.

## Requirements

* Python: 3.6, 3.7, 3.8
* requests
* pandas
* tabulate

## Installation

Installation is easy using `pip` and will install all required libraries.

```bash
pip install guruguru
```

After install, you can use `guruguru` command from your terminal.

```bash
guruguru --version
```

## Usage

### Authorization

The first time you perform a process that requires authentication, you need to use the `auth` command to obtain authentication information.

```bash
$ guruguru auth -h
usage: guruguru auth [-h] {login} ...

positional arguments:
  {login}

optional arguments:
  -h, --help  show this help message and exit
```

### Submission

In order to post your submission, you must have 

* run `auth login` command 
* created a team for the competition on the guruguru website.

```bash
$ guruguru submit create -h
usage: guruguru submit create [-h] -c COMPETITION --file FILE

optional arguments:
  -h, --help            show this help message and exit
  -c COMPETITION, --competition COMPETITION
                        Competition to submit (default: None)
  --file FILE           Path to submission file. (default: None)
```

### Competition LeaderBoard

```bash
guruguru competition lb -h

usage: guruguru competition lb [-h] -c COMPETITION [--private] [--n_top N_TOP]

optional arguments:
  -h, --help            show this help message and exit
  -c COMPETITION, --competition COMPETITION
                        Competition Id show LB (default: None)
  --private             fetch private lb (default: False)
  --n_top N_TOP         maximum number of teams to show. (default: 20)
```

## FAQ

* Q: What is the atmaCup?
    * A: The atmaCup is an onsite data competition hosted by atma Inc.
* Q: How do I enter the atmaCup?
    * A: we will send out information about the competition, so please refer to it. 

