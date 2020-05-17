from flask import Flask
meathook = Flask(__name__)


@meathook.route('/')
def main():
    return "Meat Hook"
