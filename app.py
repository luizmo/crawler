
import requests
from bs4 import BeautifulSoup
import urllib
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


class NewsSearch(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('term', required=True,
                            help='Um termo precisa ser passado')
        args = parser.parse_args()

        formattedSearchTerm = urllib.urlencode({'term': args.term})

        r = requests.get('https://www.google.com/search?q={formattedSearchTerm}&tbm=nws')

        soup = BeautifulSoup(r.text, 'html.parser')

        resultsRow = soup.find_all('div')

        results = resultsRow

        for resultRow in resultsRow:
            uri = resultRow.get('a', { 'class' : 'top' })
            link = uri.get('href')
            results.append({
                'uri': uri,
                'link': link
            })

        return results


api.add_resource(NewsSearch, '/news')

if __name__ == '__main__':
    app.run(debug=True)
