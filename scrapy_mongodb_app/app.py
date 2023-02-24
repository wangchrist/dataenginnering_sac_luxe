from flask import Flask,render_template,request 
from flask_pymongo import PyMongo
from pymongo import MongoClient

###On se connect au MongoDB afin de l'utiliser dans l'application flask
client = MongoClient('mongodb://localhost:27017/')

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/sac_luxe'
mongo = PyMongo(app)
db=client["sac_luxe"]
collection_vc = db["sac_vc"]
collection_mt=db["sac_mt"]

###Home page
@app.route('/')
def home():
    return render_template('index.html')
####page lorsqu'on a fait une recherche
@app.route('/search', methods=['GET', 'POST'])
def search():
    results_vc = []
    results_mt=[]
    if request.method == 'POST':
        query= request.form['query']
        
        
        
        
        list_vc = collection_vc.find(
            
            {"$text": {"$search": query}})
        list_mt = collection_mt.find(
            
            {"$text": {"$search": query}})

        

            
    for sac in list_vc:
        results_vc.append(sac) 
    
    for bag in list_mt:
        results_mt.append(bag)
    
    return render_template('search.html',results1=results_vc,results2=results_mt, query=query)

if __name__ == '__main__': 
    app.run(debug=True) 