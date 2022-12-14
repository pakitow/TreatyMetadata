from imports import *

def run():
    url = Request(links['wto'], headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(url).read()
    # create initial hash
    currentHash = hashlib.sha224(response).hexdigest()
    print("running")
    time.sleep(10)
    while True:
        try:
            response = urlopen(url).read()
            currentHash = hashlib.sha224(response).hexdigest()
            time.sleep(30)
            response = urlopen(url).read()
            newHash = hashlib.sha224(response).hexdigest()
            if newHash == currentHash: continue
            else: 
                print("something changed")
                response = urlopen(url).read()
                currentHash = hashlib.sha224(response).hexdigest()
                time.sleep(30)
                continue
        except Exception as e: print('error')