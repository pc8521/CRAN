首次git push到github CRAN:
@project folder (branch: main)
(假設已commit, 箭咀綠色)

```bash
git branch <your branch>
git switch <your branch>
git remote remove origin
git remote add origin git@github.com:pc8521/CRAN.git
git push origin <your branch>
```

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