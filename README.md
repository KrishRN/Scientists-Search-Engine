# Scientists-Search-Engine
![GitHub repo size](https://img.shields.io/github/repo-size/KrishRN/Scientists-Search-Engine?color=red&style=plastic)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/KrishRN/Scientists-Search-Engine?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/KrishRN/Scientists-Search-Engine?color=brightgreen&style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/KrishRN/Scientists-Search-Engine?color=blueviolet&style=plastic)

This Repository includes the implementaion for a search query. The search engine could be used after configuring elastcisearch. After configruing the elasticsearch, the sample search engine is used to try the query searches.

Description
---
There are about 100 Scientists' Data scraped from "https://ta.wikipedia.org/". The File Structure of this repo is as following:

```
 ├── analyzers : Custom filters (Stemmers,synonyms,Stopwords)
 ├── Data : data scraped from the [website](https://ta.wikipedia.org/) 
     ├── Processed_Data.xlsx : Final Processed Data 
     ├── raw_famous_people_data.xlsx : original Data scraped       
 ├── WebScraping.ipynb : script used to data collection.
 ├── indexUpload.py : Python file that converts xlsx file to a bulkdata and uploads to ElasticSearch Bulk API (configurations for indexing)
 ├── preprocess.py : Preprocesing Steps Done
```

Demo
---
* Install ElasticSearch 
* Add 'Analyzers' folder in config of Elasticsearch
* Run ElasticSearch
* Run 'indexUpload.py' to add index
* Go to http://localhost/5601
* Go to Web tools
* Search for Scientists' Data

Sample queries
---
```
*** Match query ***
GET /scientists/_search
{
   "query":{
      "match" : {
		    "துறை": "இயற்பியல்"
      }
   }
}

GET /scientists/_search
{
   "query":{
      "multi_match" : {
       
		    "query":"உயிரியல்",
			"fields": ["துறை"]
      }
   }
}

*** Query String Query ***
GET /scientists/_search
{
   "query":{
      "query_string":{
         "query":"உயிரியல்"
      }
  }
}

*** Term Level Queries ***
GET /scientists/_search
{
   "query":{
      "term":{"துறை": "இயற்பியல்"}
   }
}

*** Range queries ***
GET /scientists/_search
{
   "query":{
      "range":{
		    "பிறந்தஆண்டு":{
            "gte":1900,
            "lte":1950
         }
      }
   }
}

*** get Area of work Physics and born between 1900 and 1950 (AND Operator)***
GET /scientists/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "bool": {
            "must": [
              { "match": { "துறை": "இயற்பியல்" } },
              { "range": { "பிறந்தஆண்டு":{
						              	"gte":1900,
						              	"lte":1950
				      } 
				    }}
            ]
          }
        }
      ]
    }
  }
}

*** get area of work not be Biology or  known for Radio(OR Operator)***
GET /scientists/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "bool": {
            "must": [
              { "match": {  "துறை": "உயிரியல்" } }
            ]
          }
        },
        {
          "bool": {
            "must": [
              { "match": { "பங்களிப்புகள்":"வானொலி" } }
            ]
          }
        }
      ]
    }
  }
}

*** Get awards for noble prize and not in the field of Physics ***
GET /scientists/_search
{
   "query": {
    "bool": {
      "must": [
        {"match": {"விருதுகள்": "நோபல் பரிசு"}}

      ] ,
	  "must_not": [
        {"match": {"துறை": "இயற்பியல்"}}

      ]
    }
  }
}
  
*** delete data from index ***
POST /scientists/_delete_by_query
{
 "query": {
   "bool": {
      "must": [
        { "match": { "பெயர்":"தியாடர் சுலட்ஸ்" } }
       
      ]
    }
  }
}  

```
