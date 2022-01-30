# This is a clone of [R3DACTED v3.0](https://github.com/BVNCodeTech/R3DACTED/)

## Installation

In case you want to run a development server on your local machine, then follow the following steps. You'll require a MongoDB Atlas cluster to set it up locally.

### Get the repository

Clone the repository

```
git clone https://github.com/Reiter21/MatrixMindcraft.git

cd MatrixMindcraft
```

### Installing Virtual Environment

Be sure to have python >=3.6 installed in your machine and added to `$PATH` for *nix and to `environment variables` in Windows. Next create a virtual environment by installing and using `virtualenv`

```
pip install virtualenv
```

And then create a virtual environment

```
virtualenv env
```

Finally, activate the env

```
source env/bin/activate #For mac os and linux

env\Scripts\activate #For Windows; use backslash
```

### Installing Requirements

Use pip to install all the modules and libraries required for medSCHED in the required.txt

```
pip install -r requirements.txt
```

### Run Flask Server

Before running make sure that port 5000 is free or you can use any other port by passing the `port number` in the run function. You can start the development server like so

```
python3 main.py # For nix

python main.py # For Windows
```

## Developers
|<img src="https://github.com/pancham1603.png" alt="Pancham Agarwal" height="80" width="80">|<img src="https://github.com/im-NL.png" alt="Aryan Sharma" height="80" width="80">|<img src="https://github.com/ashish4arora.png" alt="Ashish Arora" height="80" width="80">|<img src="https://github.com/suyash-singh14.png" alt="Suyash Singh" height="80" width="80">|
|---|---|---|---|
|[Pancham Agarwal](https://github.com/pancham1603)|[Aryan Sharma](https://github.com/im-NL/)|[Ashish Arora](https://github.com/ashish4arora)|[Suyash Singh](https://github.com/suyash-singh14)
