from fastapi import FastAPI, Depends, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

app = FastAPI(title="Animeroll API", version="1.0.0", description="API для аниме интернет-магазина")

Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    if not db.query(models.Products).first():
        products = [
            ("Декимакура Genshin Impact - Diluc Ragnvindr / Дилюк Рагнвиндр", 350, "Декимакуры", "image/Diluc_f.jpg"),
            ("Брелок Attack on Titan - Levi Ackerman / Леви Аккерман", 380, "Брелоки", "image/Levi_b.jpg"),
            ("Манга The Apothecary Diaries / Монолог Фармацевта. Тома 1-4", 5500, "Манга", "image/Monolog_m.jpg"),
            ("Конструктор лего Naruto - ресторан рамена + Наруто и Джирая", 750, "Конструкторы", "image/Ramen_k.jpg"),
            ("Конструктор лего Naruto - дом Рока Ли", 750, "Конструкторы", "image/RokLi_k.png"),
            ("Магнит Howl's Moving Castle/Ходячий замок", 250, "Магнит", "image/xodyachiy_mg.png"),
            ("Подушка D.Gray-man/Ди Грей Мен", 500, "Подушка", "image/Di_p.png"),
            ("Брелок Bleach/Блич", 270, "Брелоки", "image/Blich_b.png"),
            ("Декимакура One Piece/Ван Пис", 550, "Декимакура", "image/One_d.jpg"),
            ("Кружка Girls und Panzer/Девушки и танки", 450, "Кружка", "image/Devyshki_kr.png"),
            ("Плакат Don’t Toy With Me, Miss Nagatoro/Не издевайся, Наготоро-сан", 400, "Плакат", "image/Ne_pl.png"),
            ("Фигурка Tokyo Ghoul/Токийский Гуль", 600, "Фигурка", "image/Gyl_f.png"),
            ("Значок Angels of Death/Ангел кроворолития", 200, "Значок", "image/Angel_v.png"),
            ("Брелокает Kobayashi-san Chi no Maid Dragonh/Дракон-горничная госпожи Кобаяси", 360, "Брелоки", "image/Gorn_b.png"),
            ("Значки Hakkenden: Eight Dogs of the East/Хаккэндэн: Легенда о восьми Псах Востока", 480, "Значок", "image/Vosem_z.png")
        ]
        for name, price, desc, img in products:
            db.add(models.Products(name=name, price=price, description=desc, image_url=img))
        db.commit()
    db.close()

seed_db()
app.mount("/image", StaticFiles(directory="image"), name="image")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def error_page(msg: str):
    return HTMLResponse(content=f"""
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h1 style="color: #c0392b;">Ошибка</h1>
            <p style="font-size: 18px;">{msg}</p>
            <br>
            <a href="/" style="padding: 10px 20px; background: #2b2d42; color: white; text-decoration: none; border-radius: 5px;">Вернуться на главную</a>
        </div>
    """, status_code=400)

@app.get("/")
def index(): 
    return FileResponse("index.html")

@app.get("/style.css")
def css(): 
    return FileResponse("style.css")

@app.get("/basket")
def basket(): 
    return FileResponse("basket.html")

@app.get("/account")
def account(): 
    return FileResponse("account.html")

@app.get("/registration")
def registration(): 
    return FileResponse("registration.html")

@app.get("/support")
def support(): 
    return FileResponse("support.html")

@app.get("/api/products")
def products(db: Session = Depends(get_db)):
    return db.query(models.Products).all()

@app.post("/api/register")
def register(email: str = Form(...), password: str = Form(...), name: str = Form(...), db: Session = Depends(get_db)):
    if not name.replace(" ", "").replace("-", "").isalpha():
        return error_page("Имя должно содержать только буквы.")
    if db.query(models.User).filter(models.User.email == email).first():
        return error_page("Пользователь с таким email уже зарегистрирован.")
    
    db.add(models.User(email=email, password_hash=password, name=name))
    db.commit()
    
    return HTMLResponse(content=f"""
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h1 style="color: #2c4c3b;">Регистрация успешна</h1>
            <p>Добро пожаловать в Animeroll, {name}!</p>
            <a href="/" style="padding: 10px 20px; background: #2b2d42; color: white; text-decoration: none; border-radius: 5px;">На главную</a>
        </div>
    """)