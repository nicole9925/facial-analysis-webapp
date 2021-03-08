
## Introduction

This is a web application that accepts an image of a face, analyzes the image, and creates corresponding explainable AI visualizations in order to teach the general public about machine learning algorithms. In addition, it discusses and visualizes the implications of biased models. You can see a static, conceptual version of this application [here](https://nicole9925.github.io/facial-analysis-frontend/).

## Usage

note: Make sure you have Python 3.7

Optional but recommended:
1. Create a virtual environment with the command: `conda create -n virtual_env_name python=3.7` or `virtualenv -p python3 virtual_env_name`
2. Activate your virtual environment by typing: `source activate virtual_env_name`

To run:
3. Make sure you have [node.js](https://www.npmjs.com/get-npm) installed. For mac users, you can just do `brew install node`
4. Download python dependencies using `pip install -r requirements.txt`
5. Run `npm install` to download dependencies in repository directory in command line
6. Run `npm start`
7. In another tab (cd to the repo) and start the server by running `python3 src/api/index.py` 
