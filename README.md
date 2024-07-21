# Telegram Bot Hujjati
  
![TgBot](https://github.com/user-attachments/assets/f8c481b5-af74-48cf-bed1-bb5979add444)
   
        
## Umumiy ma'lumot  
  
Ushbu Telegram bot foydalanuvchilarni ma'lumotlar bazasida ro'yxatdan o'tkazadi, administrator uchun barcha foydalanuvchilar ro'yxatini ko'rsatadi va administrator tomonidan yuborilgan rasm va sarlavhani barcha foydalanuvchilarga yuboradi.

## Talablar
 
- Python 3.x 
- `aiogram` kutubxonasi
- `python-dotenv` kutubxonasi 
- `sqlite3` kutubxonasi (Python standarti kutubxonasining bir qismi)

## O'rnatish

1. **Bog'liqliklarni o'rnatish**:
    ```bash
    pip install aiogram python-dotenv
    ```
 
2. **Atrof-muhitni sozlash**:
    Loyihangizning ildiz katalogida `.env` faylini yarating va quyidagi parametrlarni qo'shing:
    ```
    BOT_TOKEN=your-telegram-bot-token
    DB_URL=path/to/your/database.db
    ADMIN=your-telegram-user-id
    ```

## Foydalanish

### Foydalanuvchilarni boshqarish

Foydalanuvchilar botni boshlaganida yoki boshqa amallarni bajarganida ma'lumotlar bazasida ro'yxatdan o'tkaziladi.

### Buyruqlar

#### `/start`

Foydalanuvchini botga xush kelibsiz deydi va foydalanuvchi ma'lumotlar bazasida ro'yxatdan o'tmagan bo'lsa, uni qo'shadi.

```python
@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer(f"Welcome! {msg.from_user.full_name}")
    if not db.user_exists(msg.from_user.id):
        db.add(msg.from_user.id, msg.from_user.full_name)
    else:
        await msg.answer(f"siz {msg.from_user.full_name} avval ham botga tashrif buyurgansiz ")  # noqa
```

#### `/users`
Administrator uchun barcha foydalanuvchilar ro'yxatini ko'rsatadi.
```python
@dp.message(Command('users'))
async def get_users(msg: Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        users = db.get_all_users()
        for x in users:
            await msg.answer(f"UserID: {x[0]} Fullname: {x[1]}")
```
#### `:msg`
```python
@dp.message(Command('msg', prefix=':'))
async def send_meg(msg: Message):
    await msg.answer("Rasm va rasm sarlavhasini kiriting! ")  # noqa
    if msg.chat.type == "private":
        if msg.from_user.id == int(os.getenv("ADMIN")):
            @dp.message()
            async def upload_img(msg: Message):
                image = msg.json()
                img_link = json.loads(image)
                photo = img_link['photo'][0]['file_id']
                capt = img_link['caption']
                users = db.get_all_users()
                for row in users:
                    user_id = row[0]
                    try:
                        await bot.send_photo(chat_id=user_id, photo=photo, caption=capt)
                        await bot.send_message(msg.from_user.id, f"Done message all users")
                    except TelegramForbiddenError:
                        logging.warning(f"User {user_id} blocked the bot. Removing user.")
                        db.remove_users(user_id)
                    except Exception as e:
                        logging.error(f"Failed to send photo to {user_id}: {e}")

```
## Asosiy dastur
### Botni ishga tushirish uchun asosiy dastur:

```python
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

```


# Database Klassi Hujjati

## Umumiy ma'lumot

`Database` klassi SQLite ma'lumotlar bazasi bilan ishlash uchun interfeys taqdim etadi. Ushbu klass foydalanuvchilarni
boshqarish uchun usullarni o'z ichiga oladi, masalan, foydalanuvchilar jadvalini yaratish, foydalanuvchilarni qo'shish,
barcha foydalanuvchilarni olish, foydalanuvchining mavjudligini tekshirish va foydalanuvchilarni o'chirish.


```python
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self._create_users_table()

    def _create_users_table(self):
        with self.connection:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    full_name TEXT NOT NULL
                )
            ''')

    def add(self, user_id: int, user_fullname: str):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO users (user_id, full_name) VALUES (?, ?)",
                (user_id, user_fullname)
            )

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, full_name FROM users").fetchall()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def remove_users(self, user_id: int):
        with self.connection:
            self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self.connection.commit()

```

## ORM dan Foydalanish

### Initsializatsiya

```python
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DB_URL')

database = Database(DB_URL)

# Foydalanuvchini qo'shish
database.add(123456789, 'John Doe')

# Foydalanuvchi mavjudligini tekshirish
exists = database.user_exists(123456789)
print(f"Foydalanuvchi mavjud: {exists}")

# Barcha foydalanuvchilarni olish
users = database.get_all_users()
print(f"Barcha foydalanuvchilar: {users}")

# Foydalanuvchini o'chirish
database.remove_users(123456789)

# Foydalanuvchini o'chirgandan keyin mavjudligini tekshirish
exists = database.user_exists(123456789)
print(f"O'chirgandan keyin foydalanuvchi mavjud: {exists}")

```
# Litsenziya
Ushbu loyiha MIT Litsenziyasi ostida litsenziyalangan - batafsil ma'lumot uchun LICENSE faylini ko'ring.
