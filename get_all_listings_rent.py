import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
import json

class BayutScraper:
    def __init__(self):
        self.url = 'https://ll8iz711cs-3.algolianet.com/1/indexes/*/queries'
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.bayut.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'X-Algolia-Agent': 'Algolia for JavaScript (3.35.1); Browser (lite)',
            'X-Algolia-Application-Id': 'LL8IZ711CS',
            'X-Algolia-API-Key': '802406b04be9b83e3a59dbb7e61e2778',
        }
        self.params = {
            'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser (lite)',
            'x-algolia-application-id': 'LL8IZ711CS',
            'x-algolia-api-key': os.getenv("API_KEY"),
        }

    def _get_request_data(self, page_num):
        data ={ "requests":[{"indexName":"bayut-production-locations-en","params":"page=0&hitsPerPage=1&query=&optionalWords=&facets=%5B%5D&maxValuesPerFacet=100&attributesToHighlight=%5B%5D&attributesToRetrieve=*&filters=(slug%3A%22%2Fdubai%22)&numericFilters="},{"indexName":"bayut-production-ads-en","params":"page="+str(page_num)+"&hitsPerPage=24&query=&optionalWords=&facets=%5B%5D&maxValuesPerFacet=10&attributesToHighlight=%5B%5D&attributesToRetrieve=%5B%22agency%22%2C%22area%22%2C%22baths%22%2C%22category%22%2C%22contactName%22%2C%22externalID%22%2C%22id%22%2C%22location%22%2C%22objectID%22%2C%22phoneNumber%22%2C%22coverPhoto%22%2C%22photoCount%22%2C%22price%22%2C%22product%22%2C%22productLabel%22%2C%22purpose%22%2C%22geography%22%2C%22permitNumber%22%2C%22referenceNumber%22%2C%22rentFrequency%22%2C%22rooms%22%2C%22slug%22%2C%22slug_l1%22%2C%22slug_l2%22%2C%22title%22%2C%22title_l1%22%2C%22title_l2%22%2C%22createdAt%22%2C%22updatedAt%22%2C%22ownerID%22%2C%22isVerified%22%2C%22propertyTour%22%2C%22verification%22%2C%22completionStatus%22%2C%22furnishingStatus%22%2C%22-agency.tier%22%2C%22requiresLogin%22%2C%22coverVideo%22%2C%22videoCount%22%2C%22description%22%2C%22description_l1%22%2C%22description_l2%22%2C%22floorPlanID%22%2C%22panoramaCount%22%2C%22hasMatchingFloorPlans%22%2C%22hasTransactionHistory%22%2C%22state%22%2C%22photoIDs%22%2C%22reactivatedAt%22%2C%22hidePrice%22%2C%22extraFields%22%2C%22projectNumber%22%2C%22locationPurposeTier%22%2C%22ownerAgent%22%5D&filters=purpose%3A%22for-sale%22%20AND%20(location.slug%3A%22%2Fdubai%22)%20AND%20category.slug%3A%22residential%22&numericFilters="},{"indexName":"bayut-production-agencies-en","params":"page=0&hitsPerPage=0&query=&optionalWords=&facets=%5B%5D&maxValuesPerFacet=100&attributesToHighlight=%5B%5D&attributesToRetrieve=*&filters=&numericFilters="},{"indexName":"bayut-production-agencies-en","params":"page=0&hitsPerPage=0&query=&optionalWords=&facets=%5B%5D&maxValuesPerFacet=100&attributesToHighlight=%5B%5D&attributesToRetrieve=%5B%22agents%22%5D&filters=&numericFilters="}]}
        response = requests.post(self.url, headers=self.headers, params=self.params, data=json.dumps(data))
        response_json = response.json()

        for hit in response_json['results'][1]['hits']:
            try:
                self.save_to_db(hit)
            except DuplicateKeyError:
                print('Duplicate key error, skipping insertion')

    def save_to_db(self, data):
        uri = os.getenv("MONGO URI")
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['bayut']
        collection = db['listings']

        result = collection.insert_one(data)
        print(f"Inserted listing with id {result.inserted_id}")
        
scraper = BayutScraper()
data = scraper._get_request_data(1)
