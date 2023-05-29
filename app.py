from flask import Flask,render_template, request,jsonify
import requests 
from bs4 import BeautifulSoup as bs 
from urllib.request import urlopen
import pymongo
app = Flask(__name__)
a=0
@app.route("/",methods=['GET'])
def home_page():
    return render_template("index.html")

@app.route("/review",methods=['POST','GET'])
def index():
    b=0
    if request.method=='POST':
        searchString=request.form["content"].replace(" ","")
        rl_search="https://www.reliancedigital.in/search?q=" + searchString + ":relevance&page="+str(a)
        rl_product_url=urlopen(rl_search)
        rl_product_url_read=rl_product_url.read()
        rl_product_url.close()
        rl_product_url_html=bs(rl_product_url_read,"html.parser")
        rl_all_pages=rl_product_url_html.find_all("div",{"class":"page-act-row"})[0].find_all("div",{"class","pagination"})[0].text
        total_pages=int(str(rl_all_pages[-2])+str(rl_all_pages[-1]))
        reviews = []
        for i in range(total_pages+1):
            rl_product_url=urlopen(rl_search)
            rl_product_url_read=rl_product_url.read()
            rl_product_url.close()
            rl_product_url_html=bs(rl_product_url_read,"html.parser")
            rl_all_product=rl_product_url_html.find_all("li",{"class":"grid pl__container__sp blk__lg__3 blk__md__4 blk__sm__6 blk__xs__6"})
            for j in rl_all_product:
                j.encoding='utf-8'
                product_number=b+1
                page_number=i+1
                name=(j.div.div.p.text)
                price=(j.div.find_all("div",{"class":"slider-text"})[0].span.text)
                mydict = {"ProductNumber" : product_number,"PageNumber" : page_number,"Product": searchString, "Name": name, "Price": price}
                reviews.append(mydict)
                b+=1

        client = pymongo.MongoClient("mongodb+srv://harshitsalecha0796:harshit07@mongodblearn.vycebmm.mongodb.net/?retryWrites=true&w=majority")
        db=client['Reliance_Digit_Webscrapping']
        connection_reliance=db['rl_digital_web']
        connection_reliance.insert_many(reviews)

        return render_template('result.html', reviews=reviews[0:(len(reviews))])
    else:
        return render_template("index.html")
    
if __name__=="__main__":
    app.run(host="0.0.0.0")