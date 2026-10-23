import boto3
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import io

from database import engine, Base, get_db
from models import Product
from storage import upload_image, get_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/admin/products")
async def create_product(
    name: str = Form(...),
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    content = await photo.read()
    key = upload_image(content, photo.filename or "image.jpg")
    
    product = Product(name=name, image_key=key)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return {"status": "ok", "product_id": product.id}

@app.get("/products")
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).order_by(Product.created_at.desc()))
    products = result.scalars().all()
    return [{"id": p.id, "name": p.name} for p in products]

@app.get("/products/{product_id}/image")
async def product_image(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        return {"error": "Not found"}
    
    image_bytes = get_image(product.image_key)
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        return {"error": "Товар не найден"}

    try:
        from storage import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, BUCKET_NAME
        from botocore.client import Config
        
        s3 = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4"),
        )
        s3.delete_object(Bucket=BUCKET_NAME, Key=product.image_key)
    except Exception as e:
        print(f"Не удалось удалить картинку из MinIO: {e}")

    await db.delete(product)
    await db.commit()
    
    return {"status": "ok"}