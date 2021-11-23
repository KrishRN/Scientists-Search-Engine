from elasticsearch import Elasticsearch, helpers
import pandas as pd

client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'scientists'

df = pd.read_excel('Data\Processed_Data.xlsx')
print(df.columns)
df2 = df.to_dict('records')
print(df2[0])


def generator(df2):
    for c, line in enumerate(df2):
        yield {
            '_index': INDEX,
            '_type': '_doc',
            '_id': c,
            '_source': {
                'பெயர்': line.get('name', None),
                'பிறந்தஆண்டு': line.get('birth_year', None),
                'துறை': line.get('area_work', None),
                'பங்களிப்புகள்': line.get('known_for', None),
                'விருதுகள்': line.get('awards', None),
                'சுருக்கம்': line.get('summary', None),
                'உள்ளடக்கம்': line.get('content', None),
				'உரலி': line.get('url_page', None),
            }
        }


settings = {
    'settings': {
        'analysis': {
            'analyzer': {
                'my_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': [
                        'tamil_synonym',
                        'tamil_stopwords',
                        'tamil_stemmer'
                    ]
                }
            },
            'filter': {
                'tamil_synonym': {
                    'type': 'synonym',
                    'synonyms_path': 'analyzer/synonym.txt'
                },
                "tamil_stop": {
                    "type": "stop",
                    "stopwords": 'analyzer/TamilStopWords.txt'
                },
                "tamil_stemmer": {
                    "type": "stemmer",
                    "rules_path": "analyzer/stemmer.txt"
                }
            }
        },
        'number_of_shards': 1,
        'number_of_replicas': 0
    },
    'mappings': {
        'properties': {
            'பெயர்': {
                'type': 'text'
            },
            'பிறந்தஆண்டு': {
                'type': 'short'
            },
            'துறை': {
                'type': 'text'
            },
            'பங்களிப்புகள்': {
                'type': 'text'
            },
            'விருதுகள்': {
                'type': 'text'
            },
            'சுருக்கம்': {
                'type': 'text'
            },
            'உள்ளடக்கம்': {
                'type': 'text'
            },
            'உரலி': {
                'type': 'text'
            }
        }
    }
}

response = client.indices.create(index=INDEX, ignore=[400, 404], body=settings)
print(response)

try:
    res = helpers.bulk(client, generator(df2))
    print('Working')
except Exception as e:
    print(e)
    pass
