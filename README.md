# bayut_data
Collecting bayut real estate data (Dubai)

RENT:
    PLACE: 
        DUBAI
    RENT TYPE:
        Yearly - 500 pages - 24*500
        Monthly - 100 pages
        Weekly - 100 pages
        Daily - 100 pages
    PLACE TYPE:
        RESIDENTIAL
        COMMERCIAL
BUY:
    PLACE: 
        DUBAI
    BUY TYPE:
        READY
        OFF PLAN
    PLACE TYPE:
        RESIDENTIAL
        COMMERCIAL
        
This code sends HTTP requests to the Algolia search API to retrieve real estate rental listings in Dubai that are updated on a daily basis. It sends a total of 9 requests (for 216 rental listings in total), with 24 listings per request.

It uses the requests module to send HTTP requests to the Algolia search API and the json module to encode/decode JSON data. It also imports the pymongo module to work with MongoDB databases.

Each request contains a data dictionary with a list of search queries for three indices (bayut-production-locations-en, bayut-production-ads-en, and bayut-production-agencies-en) in the Algolia search API.

The first query returns the location data for Dubai, the second query returns the rental listings in Dubai that are updated on a daily basis, and the third and fourth queries return agency data.

The params dictionary contains additional parameters to be sent with each HTTP request, including the Algolia application ID and API key.

REQUEST FOR RENT AND BUY

The first dictionary contains a single request that queries the "bayut-production-ads-en" index and retrieves 24 hits per page. The query filters the results to include only ads with specific object IDs. The attributes to be retrieved include information about the properties, such as agency, area, baths, price, rooms, and more.

The second dictionary contains two requests. The first request queries the "bayut-production-locations-en" index and retrieves one hit per page. The query filters the results to include only the location with the slug "/dubai". The attributes to be retrieved include all available information about the location.

The second request queries the "bayut-production-ads-en" index and retrieves 24 hits per page. The query does not include any specific filters, but retrieves properties based on the page number. The attributes to be retrieved include information about the properties, such as agency, area, baths, price, rooms, and more.
