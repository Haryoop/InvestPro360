from fastapi import FastAPI
from routes import router
from fastapi.staticfiles import StaticFiles
import numpy as np
import models.quote as quote


app = FastAPI()
app.include_router(router, prefix="")
app.mount("/public", StaticFiles(directory="public"), name="public")


#print(formatted_quotes)
#second_celebrity = formatted_quotes[1]["celebrety"]
#print(second_celebrity)


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
print(matrix)


