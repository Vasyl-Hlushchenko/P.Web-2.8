from models import Authors, Qoutes
import connection as connection
import json


def load_json(file):
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def post_authors(file):
    data = load_json(file)

    for author in data:
        post_author = Authors(
            fullname=author["fullname"],
            born_date=author["born_date"],
            born_location=author["born_location"],
            description=author["description"],
        )
        post_author.save()


def post_qoutes(file):
    data = load_json(file)

    for qoute in data:
        post_qoute = Qoutes(
            tags=qoute["tags"],
            author=[
                author.id
                for author in Authors.objects()
                if author.fullname == qoute["author"]
            ][0],
            qoute=qoute["qoute"],
        )
        post_qoute.save()


if __name__ == "__main__":
    post_authors("authors.json")
    post_qoutes("qoutes.json")
