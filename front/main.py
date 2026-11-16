from fastapi import FastAPI, Depends, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from database import SessionLocal, engine, Base
import models

app = FastAPI( 
    title="Animeroll API",
    version="1.0.0",
    description="API для аниме интернет-магазина"
)

Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    if db.query(models.Products).first() is None:
        products_data = [
            {"name": "Декимакура Genshin Impact - Diluc Ragnvindr / Дилюк Рагнвиндр", "price": 350, "description": "Декимакуры", "image_url": "image/Diluc_f.jpg"},
            {"name": "Брелок Attack on Titan - Levi Ackerman / Леви Аккерман", "price": 380, "description": "Брелоки", "image_url": "image/Levi_b.jpg"},
            {"name": "Манга The Apothecary Diaries / Монолог Фармацевта. Тома 1-4", "price": 5500, "description": "Манга", "image_url": "image/Monolog_m.jpg"},
            {"name": "Конструктор лего Naruto - ресторан рамена + Наруто и Джирая", "price": 750, "description": "Конструкторы", "image_url": "image/Ramen_k.jpg"},
            {"name": "Конструктор лего Naruto - дом Рока Ли", "price": 750, "description": "Конструкторы", "image_url": "image/RokLi_k.png"},
            {"name": "Магнит Howl's Moving Castle/Ходячий замок", "price": 250, "description": "Магнит", "image_url": "image/xodyachiy_mg.png"},
            {"name": "Подушка D.Gray-man/Ди Грей Мен", "price": 500, "description": "Подушка", "image_url": "image/Di_p.png"},
            {"name": "Брелок Bleach/Блич", "price": 270, "description": "Брелоки", "image_url": "image/Blich_b.png"},
            {"name": "Декимакура One Piece/Ван Пис", "price": 550, "description": "Декимакура", "image_url": "image/One_d.jpg"},
            {"name": "Кружка Girls und Panzer/Девушки и танки", "price": 450, "description": "Кружка", "image_url": "image/Devyshki_kr.png"},
            {"name": "Плакат Don’t Toy With Me, Miss Nagatoro/Не издевайся, Наготоро-сан", "price": 400, "description": "Плакат", "image_url": "image/Ne_pl.png"},
            {"name": "Фигурка Tokyo Ghoul/Токийский Гуль", "price": 600, "description": "Фигурка", "image_url": "image/Gyl_f.png"},
            {"name": "Значок Angels of Death/Ангел кроворолития", "price": 200, "description": "Значок", "image_url": "image/Angel_v.png"},
            {"name": "Брелокает Kobayashi-san Chi no Maid Dragonh/Дракон-горничная госпожи Кобаяси", "price": 360, "description": "Брелоки", "image_url": "image/Gorn_b.png"},
            {"name": "Значки Hakkenden: Eight Dogs of the East/Хаккэндэн: Легенда о восьми Псах Востока", "price": 480, "description": "Значок", "image_url": "image/Vosem_z.png"}
        ]
        for p in products_data:
            new_product = models.Products(
                name=p["name"],
                price=p["price"],
                description=p["description"],
                image_url=p["image_url"]
            )
            db.add(new_product)
        db.commit()
    db.close()

seed_db()

if os.path.exists("image"):
    app.mount("/image", StaticFiles(directory="image"), name="image")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def error_page(message: str):
    return HTMLResponse(content=f"""
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h1 style="color: #c0392b;">Ошибка</h1>
            <p style="font-size: 18px;">{message}</p>
            <br>
            <a href="/" style="padding: 10px 20px; background: #2b2d42; color: white; text-decoration: none; border-radius: 5px;">Вернуться на главную</a>
        </div>
    """, status_code=400)

@app.get("/")
def read_index():
    return FileResponse("index.html")

@app.get("/style.css")
def read_css():
    return FileResponse("style.css")

@app.get("/basket")
def read_basket():
    return FileResponse("basket.html")

@app.get("/account")
def read_account():
    return FileResponse("account.html")

@app.get("/registration")
def read_registration():
    return FileResponse("registration.html")

@app.get("/support")
def read_support():
    return FileResponse("support.html")

@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products

@app.post("/api/register")
def register_user(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    name_check = name.replace(" ", "").replace("-", "")
    if not name_check.isalpha():
        return error_page("Имя должно содержать только буквы.")

    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return error_page("Пользователь с таким email уже зарегистрирован.")
    
    new_user = models.User(email=email, password_hash=password, name=name)
    db.add(new_user)
    db.commit()
    
    return HTMLResponse(content=f"""
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h1 style="color: #2c4c3b;">Регистрация успешна</h1>
            <p>Добро пожаловать в Animeroll, {name}!</p>
            <a href="/" style="padding: 10px 20px; background: #2b2d42; color: white; text-decoration: none; border-radius: 5px;">На главную</a>
        </div>
    """)