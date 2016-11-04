########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

def bing_search(q):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '9c6d434bb0a74372908eeaef8e751394',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'q': q,
        'count': '10',
        'offset': '0',
        'mkt': 'en-us',
        'safesearch': 'Moderate',
    })

    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        
        with open('./templates/result.html','wb')as file:
            file.write(data)
        
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__=='__main__':
    bing_search('bill')