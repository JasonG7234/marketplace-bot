from flask import Flask, render_template, request

app = Flask(__name__)

import json
# read JSON
# Opening JSON file
f = open('listings.json')
  
# returns JSON object as 
# a dictionary
listings = json.load(f)['listings']
    
import random

@app.route("/", methods=['POST', 'GET'])
def index():
    
    items = random.sample(range(0, len(listings)-1), 2) # Choose 2 random items
    
    if request.form.get('action1') == 'Item 1 is better!':
        listings[items[0]]["positiveVotes"] += 1 # Item 1 wins
        listings[items[1]]["negativeVotes"] += 1 # Item 2 loses
    elif request.form.get('action2') == 'Item 2 is better!':
        listings[items[1]]["positiveVotes"] += 1 # Item 2 wins
        listings[items[0]]["negativeVotes"] += 1 # Item 1 loses
    else:
        with open("listings.json", "w") as final:
            final.write('{"listings":[\n')
            for listing in listings:
                json.dump(listing, final)
                final.write('\n,')
            final.write(']}')
            
    return render_template('index.html', o1 = listings[items[0]], o2 = listings[items[1]])

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
