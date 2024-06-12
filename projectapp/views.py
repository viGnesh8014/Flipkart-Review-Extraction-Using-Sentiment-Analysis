import re
import string

import joblib
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def index(request):
    return render(request, "index.html")


def register(request):
    return render(request, "register.html")

def login1(request):
    return render(request, "login.html")

def user_home(request):

    return render(request, "user_home.html")

def admin_login(request):
    return render(request,"admin_login.html")

def admin_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/adminhome/")
    else:
        return redirect("/admin_login/")





def saveRegister(request):
    df = tbl_register()
    df.username = request.POST.get('name')
    df.email = request.POST.get('email')
    df.password = request.POST.get('password')
    df.confirmpassword = request.POST.get('confirmpassword')
    df.save()
    return redirect('/login/')


def checklogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if tbl_register.objects.filter(email =email,password=password).exists():
            us = tbl_register.objects.get(email = email,password = password)
            request.session['userid']=us.id
            return redirect("/user_home/")
        else:
            return redirect("/login/")

def adminhome(request):
    return render(request,"adminhome.html")

def create_product(request):
    return render(request,"create_product.html")


def save_product(request):
    if request.method == 'POST':
        # Get form data from POST request
        product_name = request.POST.get('productName')
        product_description = request.POST.get('productDescription')
        product_price = request.POST.get('productPrice')
        product_image = request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(product_image.name,product_image)
        url=fs.url(file)
        # Create and save Product instance
        product = tbl_Product(
            name=product_name,
            description=product_description,
            price=product_price,
            image=url
        )
        product.save()

        return redirect('/product_details/')  # Redirect to a product detail page or any other desired page

    return render(request, 'create_product.html')

def product_details(request):
    d=tbl_Product.objects.all()
    return render(request,"product_details.html",{"d":d})

def check_product(request):
    p_link=request.POST.get("p_link")
    ### Product url
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    # User-Agent and Accept-Language headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-us,en;q=0.5'
    }
    customer_names = []
    review_title = []
    ratings = []
    comments = []

    for i in range(1, 44):
        # Construct the URL for the current page
        url = p_link + str(
            i)

        # Send a GET request to the page
        page = requests.get(url, headers=headers)

        # Parse the HTML content
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract customer names
        names = soup.find_all('p', class_='_2sc7ZR _2V5EHH')
        for name in names:
            customer_names.append(name.get_text())

        # Extract review titles
        title = soup.find_all('p', class_='_2-N8zT')
        for t in title:
            review_title.append(t.get_text())

        # Extract ratings
        rat = soup.find_all('div', class_='_3LWZlK _1BLPMq')
        for r in rat:
            rating = r.get_text()
            if rating:
                ratings.append(rating)
            else:
                ratings.append('0')  # Replace null ratings with 0

        # Extract comments
        cmt = soup.find_all('div', class_='t-ZTKy')
        for c in cmt:
            comment_text = c.div.div.get_text(strip=True)
            comments.append(comment_text)

    # Ensure all lists have the same length
    min_length = min(len(customer_names), len(review_title), len(ratings), len(comments))
    customer_names = customer_names[:min_length]
    review_title = review_title[:min_length]
    ratings = ratings[:min_length]
    comments = comments[:min_length]

    # Create a DataFrame from the collected data

    ## comments
    import pandas as pd
    data = {
        'Customer Name': customer_names,
        'Review Title': review_title,
        'Rating': ratings,
        'Comment': comments
    }

    df = pd.DataFrame(data)
    # df['Rating'].fillna(0, inplace=True)

    # Save the DataFrame to a CSV file
    df.to_csv('pdt.csv', index=False)

    ProductReview.objects.all().delete()

    for i in range(min_length):
        # Check if a review with the same attributes already exists

        review_obj = ProductReview.objects.create(
            customer_name=customer_names[i],
            review_title=review_title[i],
            rating=ratings[i],
            comment=comments[i]
        )
        review_obj.save()

    d=ProductReview.objects.all()
    review=df['Review Title']
    comment=df['Comment']


    model=joblib.load("product_review_model_ML.pkl")

    from sklearn.feature_extraction.text import CountVectorizer

    vectorization = joblib.load('vectorizer.joblib')
    zip_obj=zip(review,comment)

    # Preprocess the input text

    Review_result.objects.all().delete()
    for i,j in zip_obj:
        processed_text = wordopt(i)# i is reviews

        vectorized_text = vectorization.transform([processed_text])

        result = model.predict(vectorized_text)

        obj = Review_result.objects.create(
            review=i,
            result=result,
            comment=j

        )
        obj.save()

    return redirect("/review/")
def wordopt(text):
    # Creating a function to process text
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

def review(request):
    d1=Review_result.objects.all()[:50]
    p=Review_result.objects.filter(result=[2]).count()
    n=Review_result.objects.filter(result=[0]).count()
    nu=Review_result.objects.filter(result=[1]).count()
    return render(request,"user_home.html",{"d1":d1,"p":p,"n":n,"nu":nu})