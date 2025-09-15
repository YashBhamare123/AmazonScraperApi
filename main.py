from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

from product_images_scraper import getImage
app = FastAPI()

class ImageUrls(BaseModel):
    urls : list

class ProductInformation(BaseModel):
    url: str

@app.post('/product/images')
def get_images(info : ProductInformation) -> ImageUrls:
    images = getImage(info.url)
    out = ImageUrls(urls = images)
    return out


if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port= 8000)
