import click
import string

import db
import index
import learning


class CliBlackboard(object):
    def write(self, text):
        click.echo(text)


class CliPupil(object):
    def answer(self, text="Please, enter your answer"):
        return click.prompt(text)


@click.command()
@click.argument('text')
def learn(text):
    repository = db.RocksRepository()
    searcher = index.searcher()
    blackboard = CliBlackboard()
    teacher = learning.Teacher(searcher, repository)
    pupil = CliPupil()
    teacher.learn(text, pupil, blackboard)


if __name__ == "__main__":
    learn()
