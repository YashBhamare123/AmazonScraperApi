from fastapi import FastAPI
import uvicorn
import nodriver
from pydantic import BaseModel

from image_scraper import product_images

class UrlFormat(BaseModel):
    url : str

class ImageList(BaseModel):
    images : list


app = FastAPI()

@app.post("/product_images")
def get_images(url : UrlFormat):
    out = nodriver.loop().run_until_complete(product_images(url.url))
    images = ImageList(images = out)
    return images


if __name__ == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8000)
