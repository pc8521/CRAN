開始工作前（同步最新程式碼）
```bash
git checkout main
git pull origin main
git checkout <your branch>
git merge main
```

開發與提交
```bash
git add products/models.py
git commit -m "update products/views.py"
git push origin <your branch>
```

module errors
```bash
pip install -r requirements.txt
```

db errors
```bash
python manage.py makemigrations
python manage.py migrate
```

DB Tool for import / export categorys & prodcuts
```bash
python manage.py db_tool
```