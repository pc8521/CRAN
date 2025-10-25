# pages/management/commands/db_tool.py
import os
import csv
import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.apps import apps
from django.contrib.auth.models import User

# 根據 CRAN 專案的實際模型結構
CUSTOM_MODELS = [
    ('accounts', 'UserProfile'),
    ('products', 'Category'),
    ('products', 'Product'),
    ('stores', 'Shop'),  # 注意：是 Shop，不是 Store
    ('cart', 'CartItem'),
    ('wishlist', 'WishlistItem'),
    ('orders', 'Order'),
    ('orders', 'OrderItem'),
    ('notifications', 'Notification'),
]

def get_model(app_label, model_name):
    return apps.get_model(app_label, model_name)

def clear_database():
    """清空所有資料（保留 superuser）"""
    with transaction.atomic():
        # 先清空有外鍵的模型（反向順序）
        for app_label, model_name in reversed(CUSTOM_MODELS):
            model = get_model(app_label, model_name)
            if model_name != 'User':
                model.objects.all().delete()
        # 清空一般用戶（保留 superuser）
        User.objects.filter(is_superuser=False).delete()
    print("✅ 資料庫已清空（保留 superuser）")

def export_to_csv():
    """匯出所有模型為 CSV（使用外鍵 ID）"""
    export_dir = "db_export"
    os.makedirs(export_dir, exist_ok=True)

    for app_label, model_name in CUSTOM_MODELS:
        model = get_model(app_label, model_name)
        filename = f"{export_dir}/{app_label}_{model_name.lower()}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 欄位：外鍵用 _id 結尾
            fields = []
            for field in model._meta.fields:
                if field.is_relation:
                    fields.append(f"{field.name}_id")
                else:
                    fields.append(field.name)
            writer.writerow(fields)

            for obj in model.objects.all():
                row = []
                for field_name in fields:
                    if field_name.endswith('_id'):
                        rel_field = field_name[:-3]
                        rel_obj = getattr(obj, rel_field)
                        row.append(rel_obj.id if rel_obj else '')
                    else:
                        value = getattr(obj, field_name)
                        if value is None:
                            row.append('')
                        elif isinstance(value, datetime):
                            row.append(value.isoformat())
                        else:
                            row.append(str(value))
                writer.writerow(row)
        print(f"📤 匯出 {app_label}.{model_name} → {filename}")

def import_from_csv():
    """從 CSV 匯入（按依賴順序）"""
    clear_database()
    import_dir = "db_export"
    if not os.path.exists(import_dir):
        raise FileNotFoundError("匯入目錄不存在，請先執行匯出")

    with transaction.atomic():
        # 第一階段：無外鍵或外鍵簡單的模型
        simple_models = [
            ('products', 'Category'),
            ('stores', 'Shop'),
            ('accounts', 'UserProfile'),
        ]
        for app_label, model_name in simple_models:
            model = get_model(app_label, model_name)
            filename = f"{import_dir}/{app_label}_{model_name.lower()}.csv"
            if not os.path.exists(filename):
                continue
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                objs = []
                for row in reader:
                    clean_row = {}
                    for k, v in row.items():
                        if v == '':
                            clean_row[k] = None
                        elif '_at' in k or k in ['date_joined', 'last_login']:
                            clean_row[k] = datetime.fromisoformat(v) if v else None
                        elif k.endswith('_id'):
                            clean_row[k] = int(v) if v else None
                        else:
                            clean_row[k] = v
                    try:
                        objs.append(model(**clean_row))
                    except Exception as e:
                        print(f"❌ 匯入錯誤 {app_label}.{model_name}: {e}")
                        continue
                if objs:
                    model.objects.bulk_create(objs)
            print(f"📥 匯入 {app_label}.{model_name} ← {filename}")

        # 建立快取（用於外鍵）
        from products.models import Category
        from stores.models import Shop
        category_cache = {cat.id: cat for cat in Category.objects.all()}
        shop_cache = {shop.id: shop for shop in Shop.objects.all()}

        # 第二階段：有外鍵的模型
        # Product
        product_file = f"{import_dir}/products_product.csv"
        if os.path.exists(product_file):
            with open(product_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                objs = []
                for row in reader:
                    clean_row = {}
                    for k, v in row.items():
                        if k == 'category_id':
                            clean_row['category'] = category_cache.get(int(v)) if v else None
                        elif v == '':
                            clean_row[k.replace('_id', '')] = None
                        elif '_at' in k:
                            clean_row[k.replace('_id', '')] = datetime.fromisoformat(v) if v else None
                        elif k.endswith('_id'):
                            # 其他外鍵（如 user_id）
                            clean_row[k.replace('_id', '')] = int(v) if v else None
                        else:
                            clean_row[k] = v
                    try:
                        from products.models import Product
                        objs.append(Product(**clean_row))
                    except Exception as e:
                        print(f"❌ Product 匯入錯誤: {e}")
                        continue
                if objs:
                    Product.objects.bulk_create(objs)
            print("📥 匯入 products.Product ← products_product.csv")

        # 其他模型（CartItem, Order 等）可依此模式擴充
        print("✅ 匯入完成")

def generate_fake_data():
    """生成測試資料（使用正確模型名稱）"""
    from products.models import Category, Product
    from stores.models import Shop  # 關鍵修正：Shop 而非 Store
    from accounts.models import UserProfile
    from django.contrib.auth.models import User
    import random

    user, _ = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
    )
    if not user.password:
        user.set_password('12345678')
        user.save()
    UserProfile.objects.get_or_create(user=user)

    categories = []
    for name in ['清潔用品', '廚房用品', '居家收納', '個人護理']:
        cat, _ = Category.objects.get_or_create(name=name)
        categories.append(cat)

    for i in range(20):
        Product.objects.get_or_create(
            sku=f"SKU{i:04d}",
            defaults={
                'name': f'測試商品 {i+1}',
                'description': f'這是第 {i+1} 個測試商品',
                'price': round(random.uniform(10, 500), 2),
                'stock': random.randint(0, 100),
                'category': random.choice(categories),
                'is_active': True
            }
        )

    Shop.objects.get_or_create(  # 關鍵修正：Shop
        shop_name='測試門市',
        defaults={
            'address': '台北市測試路123號',
            'phone': '02-12345678',
            'opening_hours': '10:00-22:00',
            'is_active': True
        }
    )
    print("✅ 已生成測試資料（用戶: testuser / 密碼: testpass123）")

class Command(BaseCommand):
    help = 'CRAN 專案資料庫工具'

    def handle(self, *args, **options):
        while True:
            print("\n" + "="*50)
            print("🛠️  CRAN 專案資料庫工具")
            print("="*50)
            print("1. 清空資料庫所有資料")
            print("2. 匯出資料庫到 CSV")
            print("3. 從 CSV 匯入資料庫")
            print("4. 生成隨機測試資料")
            print("0. 離開")
            print("-"*50)

            choice = input("請選擇功能 (0-4): ").strip()
            if choice == '1':
                confirm = input("⚠️  確定要清空所有資料？(y/N): ")
                if confirm.lower() == 'y':
                    clear_database()
            elif choice == '2':
                export_to_csv()
            elif choice == '3':
                confirm = input("⚠️  匯入會先清空資料庫，確定？(y/N): ")
                if confirm.lower() == 'y':
                    import_from_csv()
            elif choice == '4':
                generate_fake_data()
            elif choice == '0':
                print("👋 再見！")
                break
            else:
                print("❌ 無效選項，請重試")