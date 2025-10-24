# your_project/management/commands/db_tool.py
import os
import csv
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.apps import apps
from django.contrib.auth.models import User
from django.conf import settings

# 取得所有自訂 App（排除 Django 內建）
CUSTOM_APPS = [
    'accounts',
    'products',
    'stores',
    'cart',
    'wishlist',
    'orders',
    'notifications',
]

def get_all_models():
    models = []
    for app_label in CUSTOM_APPS:
        app_config = apps.get_app_config(app_label)
        models.extend(app_config.get_models())
    return models

def clear_database():
    """清空所有自訂資料表（保留 auth_user 結構但清空資料）"""
    with transaction.atomic():
        # 先清空有外鍵依賴的表（反向排序）
        models = get_all_models()
        # 移除 User（保留結構，只清資料）
        for model in models:
            if model.__name__ != 'User':
                model.objects.all().delete()
        # 最後清空 User（保留 superuser 可選）
        User.objects.filter(is_superuser=False).delete()
    print("✅ 資料庫已清空（保留 superuser）")

def export_to_csv():
    """匯出所有模型資料為 CSV"""
    export_dir = "db_export"
    os.makedirs(export_dir, exist_ok=True)
    
    for model in get_all_models():
        filename = f"{export_dir}/{model._meta.label_lower.replace('.', '_')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 欄位名稱
            fields = [f.name for f in model._meta.fields]
            writer.writerow(fields)
            # 資料列
            for obj in model.objects.all():
                row = []
                for field in fields:
                    value = getattr(obj, field)
                    if value is None:
                        row.append('')
                    elif isinstance(value, datetime):
                        row.append(value.isoformat())
                    else:
                        row.append(str(value))
                writer.writerow(row)
        print(f"📤 匯出 {model._meta.label} → {filename}")

def import_from_csv():
    """從 CSV 匯入資料"""
    import_dir = "db_export"
    if not os.path.exists(import_dir):
        print("❌ 匯入目錄不存在，請先執行匯出")
        return

    with transaction.atomic():
        # 清空現有資料
        clear_database()
        
        for model in get_all_models():
            filename = f"{import_dir}/{model._meta.label_lower.replace('.', '_')}.csv"
            if not os.path.exists(filename):
                print(f"⚠️  跳過 {model._meta.label}（CSV 不存在）")
                continue

            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                objs = []
                for row in reader:
                    # 處理特殊欄位
                    for k, v in row.items():
                        if v == '':
                            row[k] = None
                        elif '_at' in k or k in ['date_joined', 'last_login']:
                            if v:
                                row[k] = datetime.fromisoformat(v)
                    try:
                        objs.append(model(**row))
                    except Exception as e:
                        print(f"❌ 匯入錯誤 {model._meta.label} 行 {len(objs)+1}: {e}")
                        continue
                if objs:
                    model.objects.bulk_create(objs)
            print(f"📥 匯入 {model._meta.label} ← {filename}")

def generate_fake_data():
    """生成隨機測試資料"""
    from products.models import Category, Product
    from stores.models import Store
    from accounts.models import UserProfile
    from django.utils import timezone

    # 1. 建立測試用戶
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        UserProfile.objects.get_or_create(user=user)

    # 2. 建立分類
    categories = []
    for name in ['清潔用品', '廚房用品', '居家收納', '個人護理']:
        cat, _ = Category.objects.get_or_create(name=name)
        categories.append(cat)

    # 3. 建立商品
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

    # 4. 建立門市
    Store.objects.get_or_create(
        name='測試門市',
        defaults={
            'address': '台北市測試路123號',
            'phone': '02-12345678',
            'opening_hours': '10:00-22:00',
            'is_active': True
        }
    )

    print("✅ 已生成測試資料（用戶: testuser / 密碼: testpass123）")

def show_menu():
    print("\n" + "="*50)
    print("🛠️  CRAN 專案資料庫工具")
    print("="*50)
    print("1. 清空資料庫所有資料")
    print("2. 匯出資料庫到 CSV")
    print("3. 從 CSV 匯入資料庫")
    print("4. 生成隨機測試資料")
    print("0. 離開")
    print("-"*50)

class Command(BaseCommand):
    help = 'CRAN 專案資料庫管理工具'

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.WARNING("⚠️  警告：非 DEBUG 模式，請確認是否為測試環境！")
            )
            confirm = input("輸入 'YES' 繼續: ")
            if confirm != 'YES':
                return

        while True:
            show_menu()
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