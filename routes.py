from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile,Form, Request, APIRouter, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, PlainTextResponse
import models.person as person, models.reclamation as reclamation,models.transaction as transaction,models.wallet as wallet ,models.post as post, models.quote as quote, models.comment as comment
import os
import numpy as np



router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
@router.get("/favicon.ico")
async def get_favicon():
    return PlainTextResponse(content="", status_code=204)

#PERSONS
@router.get("/home", response_class=HTMLResponse)
async def read_root(request: Request):
    quotes = quote.find_all_quote()
    formatted_quotes = []
    for q in quotes:
        formatted_quotes.append({
            "celebrety": q['celebrety'],  # Corrected attribute name
            "quote": q['quote'],
            "image": q['image']
        })
#kinda zeyed, just print(formatted_quotes[i - 1]["celebrety"]) etc
    j= quote.count_all_quote()
    matrix = [[0 for _ in range(3)] for _ in range(j)]
    for i in range(1, j +1): 
        matrix[i - 1][0] = formatted_quotes[i - 1]["celebrety"]
        matrix[i - 1][1] = formatted_quotes[i - 1]["quote"]
        matrix[i - 1][2] = formatted_quotes[i - 1]["image"]
    n=quote.count_all_quote()
    return templates.TemplateResponse("home.html", {"request": request, "matrix":matrix})
@router.get("/persons", response_class=HTMLResponse)
async def get_all_persons(request: Request):
    persons = person.find_all_people()  # Call the function to fetch persons from the database
    return templates.TemplateResponse("Person/persons.html", {"request": request, "persons": persons})
@router.get("/addPerson", response_class=HTMLResponse)
async def add_new_person(request: Request):
    return templates.TemplateResponse("Person/addPerson.html", {"request": request})
@router.post("/submitNewPerson", response_class=HTMLResponse)
async def submit_new_person(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    age: int = Form(...),
):
    person.add_person(first_name, last_name, age)  # Call the add_person function
    persons = person.find_all_people()  # Call the function to fetch persons from the database
    return templates.TemplateResponse("Person/persons.html", {"request": request, "persons": persons})
@router.get("/updatePerson/{person_id}", response_class=HTMLResponse)
async def updatePerson(request: Request, person_id: str):
    person_data = person.get_person_by_id(person_id)
    return templates.TemplateResponse("Person/updatePerson.html", {"request": request, "person": person_data, "person_id": person_id})

@router.post("/updatePerson/{person_id}", response_class=HTMLResponse)
async def submit_updated_person(
    request: Request,
    person_id: str,
    first_name: str = Form(...),
    last_name: str = Form(...),
    age: int = Form(...),
):
    person_id_from_form = person_id
    person.UpdatePerson(person_id_from_form, first_name, last_name, age)
    persons = person.find_all_people()  # Call the function to fetch persons from the database
    return templates.TemplateResponse("Person/persons.html", {"request": request, "persons": persons})

@router.post("/deletePerson/{person_id}", response_class=HTMLResponse)
async def delete_person(request: Request, person_id: str):
    person.deletePerson(person_id)
    return Response(content="Person deleted", status_code=200)
#RECLAMATIONS
@router.get("/reclamations", response_class=HTMLResponse)
async def get_all_reclamations(request: Request):
    reclamations = reclamation.find_all_reclamations()
    return templates.TemplateResponse("Reclamation/reclamations.html", {"request": request, "reclamations": reclamations})

@router.get("/addReclamation", response_class=HTMLResponse)
async def add_new_Reclamation(request: Request):
    return templates.TemplateResponse("Reclamation/addReclamation.html", {"request": request})
@router.post("/submitNewReclamation", response_class=HTMLResponse)
async def submit_new_post(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    synopsis: str = Form(...),
):
    reclamation.add_Reclamation(title, author, synopsis)
    #return templates.TemplateResponse("home.html", {"request": request})
    reclamations = reclamation.find_all_reclamations()
    return templates.TemplateResponse("Reclamation/reclamations.html", {"request": request, "reclamations": reclamations})
@router.get("/updateReclamation/{reclamation_id}", response_class=HTMLResponse)
async def updateReclamation(request: Request, reclamation_id: str):
    reclamation_data = reclamation.get_reclamation_by_id(reclamation_id)
    return templates.TemplateResponse("Reclamation/updateReclamation.html", {"request": request, "reclamation": reclamation_data, "reclamation_id": reclamation_id})

@router.post("/updateReclamation/{reclamation_id}", response_class=HTMLResponse)
async def submit_updated_reclamation(
    request: Request,
    reclamation_id: str,
    title: str = Form(...),
    author: str = Form(...),
    synopsis: str = Form(...),
):
    reclamation_id_from_form = reclamation_id
    reclamation.UpdateReclamation(reclamation_id_from_form, title, author, synopsis)
    #return templates.TemplateResponse("home.html", {"request": request})
    reclamations = reclamation.find_all_reclamations()
    return templates.TemplateResponse("Reclamation/reclamations.html", {"request": request, "reclamations": reclamations})

@router.post("/deleteReclamation/{reclamation_id}", response_class=HTMLResponse)
async def delete_reclamation(request: Request, reclamation_id: str):
    reclamation.deleteReclamation(reclamation_id)
    return Response(content="Reclamation deleted", status_code=200)

#POSTS
@router.get("/posts", response_class=HTMLResponse)
async def get_all_posts(request: Request):
    try:
        posts = post.find_all_posts()  # Fetch posts in descending order
        return templates.TemplateResponse("Post/posts.html", {"request": request, "posts": posts})
    except Exception as e:
        # Log the error for debugging and return an error response
        router.logger.error(f"An error occurred: {str(e)}")
        return {"error": "An internal server error occurred."}
    



@router.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: str):
    post_data = post.get_post_by_id(post_id)  # Fetch the post details using the post_id
    return templates.TemplateResponse("Post/post.html", {"request": request, "post": post_data})

@router.get("/addPost", response_class=HTMLResponse)
async def add_new_Post(request: Request):
    return templates.TemplateResponse("Post/addPost.html", {"request": request})
@router.post("/submitNewPost", response_class=HTMLResponse)
async def submit_new_post(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    contenu: str = Form(...),
):
    post.add_Post(title, author, contenu)
    #return templates.TemplateResponse("home.html", {"request": request})
    posts = post.find_all_posts()  # Fetch posts in descending order
    return templates.TemplateResponse("Post/posts.html", {"request": request, "posts": posts})

@router.get("/updatePost/{post_id}", response_class=HTMLResponse)
async def updatePost(request: Request, post_id: str):
    post_data = post.get_post_by_id(post_id)
    return templates.TemplateResponse("Post/updatePost.html", {"request": request, "post": post_data, "post_id": post_id})

@router.post("/updatePost/{post_id}", response_class=HTMLResponse)
async def submit_updated_person(
    request: Request,
    post_id: str,
    title: str = Form(...),
    author: str = Form(...),
    contenu: str = Form(...),
):
    post_id_from_form = post_id
    post.UpdatePost(post_id_from_form, title, author, contenu)
    posts = post.find_all_posts()
    return templates.TemplateResponse("Post/posts.html", {"request": request, "posts": posts})

#QUOTES
@router.get("/quotes", response_class=HTMLResponse)
async def get_all_quotes(request: Request):
    quotes = quote.find_all_quote() 
    return templates.TemplateResponse("Quote/quotes.html", {"request": request, "quotes": quotes})

@router.get("/getQuotes")
async def get_quotes():
    quotes = quote.find_all_quote()  # Replace with your actual query
    formatted_quotes = []
    for q in quotes:
        formatted_quotes.append({
            "celebrety": q.celebrety,
            "quote": q.quote,
            "image": q.image
        })
    print(formatted_quotes)
    return JSONResponse(content={"quotes": formatted_quotes})



@router.get("/addQuote", response_class=HTMLResponse)
async def add_new_quote(request: Request):
    return templates.TemplateResponse("Quote/addQuote.html", {"request": request})

@router.post("/submitNewQuote", response_class=HTMLResponse)
async def submit_new_quote(
    request: Request,
    celebrety: str = Form(...),
    quotee: str = Form(...),
    image: UploadFile = File(...),
):
    # Construct the target file path
    target_directory = r'C:\Users\jemaa\OneDrive\Bureau\PIA\testMongo try fa\public\src'
    target_filepath = os.path.join(target_directory, image.filename)

    # Saving the uploaded image to the target directory
    with open(target_filepath, "wb") as file:
        file.write(image.file.read())

    # Construct the desired relative image path for the database
    relative_image_path = os.path.join("public", "src", image.filename)

    # Use the relative_image_path as needed
    image_path = relative_image_path

    # Save the relative image path to the database
    quote.add_quote(celebrety, quotee, image_path)

    #return templates.TemplateResponse("Quote/quotes.html", {"request": request})
    quotes = quote.find_all_quote() 
    return templates.TemplateResponse("Quote/quotes.html", {"request": request, "quotes": quotes})

@router.get("/getQuoteCount")
async def get_quote_count(request: Request):
    count = quote.count_all_quote()
    return JSONResponse(content={"quoteCount": count})



@router.get("/updateQuote/{quote_id}", response_class=HTMLResponse)
async def updateQuote(request: Request, quote_id: str):
    quote_data = quote.get_quote_by_id(quote_id)
    return templates.TemplateResponse("Quote/updateQuote.html", {"request": request, "quote": quote_data, "quote_id": quote_id})

@router.post("/updateQuote/{quote_id}", response_class=HTMLResponse)
async def submit_updated_quote(
    request: Request,
    quote_id: str,
    celebrety: str = Form(...),
    quote: str = Form(...),
    image: str = Form(...),
):
    quote_id_from_form = quote_id
    quote.UpdateQuote(quote_id_from_form, celebrety, quote, image)
    #return templates.TemplateResponse("home.html", {"request": request})
    quotes = quote.find_all_quote() 
    return templates.TemplateResponse("Quote/quotes.html", {"request": request, "quotes": quotes})

@router.post("/deleteQuote/{quote_id}", response_class=HTMLResponse)
async def delete_quote(request: Request, quote_id: str):
    quote.deleteQuote(quote_id)
    return Response(content="Quote deleted", status_code=200)
#Comment
@router.get("/addComment/{post_id}", response_class=HTMLResponse)
async def add_new_Comment(request: Request, post_id: str):
    return templates.TemplateResponse("Comment/addComment.html", {"request": request, "post_id": post_id})

@router.post("/submitNewComment", response_class=HTMLResponse)
async def submit_new_comment(
    request: Request,
    post_id: str = Form(...),
    author: str = Form(...),
    contenu: str = Form(...),
):
    comment.add_Comment(post_id, author, contenu)
    return templates.TemplateResponse("home.html", {"request": request})


#wallet
@router.get("/wallets", response_class=HTMLResponse)
async def get_all_wallets(request: Request):
    try:
        wallets = wallet.find_all_wallets()  # Call the function to fetch wallets from the database
        return templates.TemplateResponse("Wallet/wallets.html", {"request": request, "wallets": wallets})
    except Exception as e:
        # Log the error for debugging and return an error response
        router.logger.error(f"An error occurred: {str(e)}")
        return {"error": "An internal server error occurred."}
@router.get("/addWallet", response_class=HTMLResponse)
async def add_new_wallet(request: Request):
    return templates.TemplateResponse("wallet/addWallet.html", {"request": request})

@router.post("/submitNewWallet", response_class=HTMLResponse)
async def submit_new_wallet(
    request: Request,
    quantite: float = Form(...),
   
):
    wallet.add_Wallet(quantite)  # Call the add_wallet function
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/updateWallet/{wallet_id}", response_class=HTMLResponse)
async def updatewallet(request: Request, wallet_id: str):
    wallet_data = wallet.get_wallet_by_id(wallet_id)
    return templates.TemplateResponse("wallet/updateWallet.html", {"request": request, "wallet": wallet_data, "wallet_id": wallet_id})

@router.post("/updateWallet/{wallet_id}", response_class=HTMLResponse)
async def submit_updated_wallet(
    request: Request,
    wallet_id: str,
    quantite: float = Form(...),
):
    
    print("start of update post")
    print("wallet id while post: ", wallet_id)
    wallet_id_from_form = wallet_id
    result = wallet.UpdateWallet(wallet_id_from_form, quantite)
    return templates.TemplateResponse("home.html", {"request": request})

    #response = RedirectResponse(url="home.html", status_code=303)
    #return response    

@router.post("/deleteWallet/{wallet_id}", response_class=HTMLResponse)
async def delete_wallet(request: Request, wallet_id: str):
    try:
        result = wallet.deleteWallet(wallet_id)
        return Response(content="Wallet deleted", status_code=200)
    except Exception as e:
        router.logger.error(f"An error occurred while deleting the wallet: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


#transaction
@router.get("/transactions", response_class=HTMLResponse)
async def get_all_transactions(request: Request):
    try:
        transactions = transaction.find_all_transactions()  # Call the function to fetch transactions from the database
        return templates.TemplateResponse("transaction/transactions.html", {"request": request, "transactions": transactions})
    except Exception as e:
        # Log the error for debugging and return an error response
        router.logger.error(f"An error occurred: {str(e)}")
        return {"error": "An internal server error occurred."}
@router.get("/addTransaction", response_class=HTMLResponse)
async def add_new_transaction(request: Request):
    return templates.TemplateResponse("transaction/addTransaction.html", {"request": request})

@router.post("/submitNewTransaction", response_class=HTMLResponse)
async def submit_new_transaction(
    request: Request,
    amount: float = Form(...),
   type: str = Form(...),
   date: float= Form(...),
):
    transaction.add_Transaction(amount,type,date)  # Call the add_transaction function
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/updateTransaction/{transaction_id}", response_class=HTMLResponse)
async def updatetransaction(request: Request, transaction_id: str):
    transaction_data = transaction.get_transaction_by_id(transaction_id)
    return templates.TemplateResponse("transaction/updateTransaction.html", {"request": request, "transaction": transaction_data, "transaction_id": transaction_id})

@router.post("/updateTransaction/{transaction_id}", response_class=HTMLResponse)
async def submit_updated_transaction(
    request: Request,
    transaction_id: str,
    amount: float = Form(...),
   type: str = Form(...),
   date: str= Form(...),
):
    
    print("start of update post")
    print("transaction id while post: ", transaction_id)
    transaction_id_from_form = transaction_id
    result = transaction.UpdateTransaction(transaction_id_from_form,amount,type,date)
    return templates.TemplateResponse("home.html", {"request": request})

    #response = RedirectResponse(url="home.html", status_code=303)
    #return response    

@router.post("/deleteTransaction/{transaction_id}", response_class=HTMLResponse)
async def delete_transaction(request: Request, transaction_id: str):
    try:
        result = transaction.deleteTransaction(transaction_id)
        return Response(content="Transaction deleted", status_code=200)
    except Exception as e:
        router.logger.error(f"An error occurred while deleting the transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#prediction