# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)

# Cookie Cutter

## Data Science

cd RioTinto # riotinto
cookiecutter -c v1 https://github.com/drivendata/cookiecutter-data-science

## Lambda Functions

mkdir aws_lambda
cd aws_lambda
cookiecutter https://github.com/hypoport/cookiecutter-aws-lambda --no-input \
    project_name="RioTintoLambda" project_slug="riotinto_lambda" \
    lambda_function="process_data" aws_region="ca-central-1"
https://github.com/idea-bank/aws-lambda-basic-handler
cd ..

## Flask API

mkdir flask_app
cd flask_app
cookiecutter https://github.com/cookiecutter-flask/cookiecutter-flask
https://github.com/savak1990/cookiecutter-python-terraform-aws-template/
https://github.com/miketheman/cookiecutter-fastapi-serverless
cd ..

# Virtual Environment

cd riotinto
virtualenv -p python3.9 osx309venv

# GitHub

cd /Volumes/500GssdXFAT/kinito/Medfar/RioTinto
git remote set-url origin https://github.com/enriqueescobar-it/riotinto-cleaner.git
git add .
git commit -m "Override with new version"
git push --force origin main
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
git remote set-url origin https://kinito@dev.azure.com/kinito/Medfar/_git/RioTinto
