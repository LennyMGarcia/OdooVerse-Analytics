import requests
def load_data(urls):
    responses = {}
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            responses[url] = response.json()
        else:
            print(f"Error getting data from {url}")
    
    return responses