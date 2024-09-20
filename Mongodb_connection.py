from pymongo import MongoClient
from pydantic import BaseModel
import pandas as pd
from fastapi import FastAPI
import os 
app = FastAPI()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['New_database']
collection = db['ExcellData']

# Read the Excel file into a DataFrame

# Define the Pydantic model
class Dataset(BaseModel):
    Valid: bool
    Time: str
    Latitude: float
    Longitude: float
    Altitude: int
    Speed: str
    Address: str
    Attributes: str
@app.post("/root")
def host(file_name:str):
    file_path = os.path.join(os.getcwd(), file_name)
    df = pd.read_excel(file_path)
    df = pd.DataFrame(df)

    # Loop through the DataFrame and insert each row into MongoDB
    for i, row in df.iterrows():
            # Convert the row to a dictionary and validate it with the Pydantic model
            data = Dataset(
                Valid=row['Valid'],
                Time=row['Time'],
                Latitude=row['Latitude'],
                Longitude=row['Longitude'],
                Altitude=row['Altitude'],
                Speed=row['Speed'],
                Address=row['Address'],
                Attributes=row['Attributes']
            )

            collection.insert_one(data.dict())
            return("Successfully completed")

