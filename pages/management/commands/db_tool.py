# pages/management/commands/db_tool.py
import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Category, Product

# 預設值（避免 NOT NULL 錯誤）
DEFAULT_DESCRIPTION = ""
DEFAULT_TAG = "Classic"      # 必須是 tag_choices 中存在的 key
DEFAULT_BRAND = "Other"      # 必須是 brand_choices 中存在的 key

def clear_database():
    """僅清空 Category 和 Product"""
    with transaction.atomic():
        Product.objects.all().delete()
        Category.objects.all().delete()
    print("✅ 已清空 Category 與 Product 資料")

def export_to_csv():
    """匯出所有欄位（空值轉為預設值）"""
    export_dir = "db_export"
    os.makedirs(export_dir, exist_ok=True)

    # 匯出 Category
    with open(f"{export_dir}/products_category.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'description', 'category_img'])
        for cat in Category.objects.all():
            writer.writerow([
                cat.id,
                cat.name,
                cat.description or DEFAULT_DESCRIPTION,
                cat.category_img.name if cat.category_img else 'products/default.jpg'
            ])
    print("📤 匯出 products_category.csv")

    # 匯出 Product
    with open(f"{export_dir}/products_product.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'id', 'sku', 'name', 'description', 'price', 'stock', 'category_id',
            'is_active', 'tag', 'brand',
            'product_img', 'product_img1', 'product_img2'
        ])
        for prod in Product.objects.all():
            writer.writerow([
                prod.id,
                prod.sku or '',
                prod.name,
                prod.description or DEFAULT_DESCRIPTION,
                str(prod.price),
                prod.stock,
                prod.category.id if prod.category else '',
                prod.is_active,
                prod.tag or DEFAULT_TAG,      # 空值轉預設
                prod.brand or DEFAULT_BRAND,  # 空值轉預設
                prod.product_img.name if prod.product_img else 'products/default.jpg',
                prod.product_img1.name if prod.product_img1 else 'products/default.jpg',
                prod.product_img2.name if prod.product_img2 else 'products/default.jpg',
            ])
    print("📤 匯出 products_product.csv（含預設值處理）")

def import_from_csv():
    """匯入所有欄位（空值使用預設值）"""
    clear_database()
    import_dir = "db_export"
    if not os.path.exists(import_dir):
        raise FileNotFoundError("目錄 'db_export' 不存在，請先執行匯出")

    with transaction.atomic():
        # 匯入 Category
        category_map = {}
        with open(f"{import_dir}/products_category.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = Category.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    description=row['description'] or DEFAULT_DESCRIPTION,  # 關鍵修正
                    category_img=row['category_img'] or 'products/default.jpg'
                )
                category_map[cat.id] = cat
        print("📥 匯入 products_category.csv")

        # 匯入 Product
        with open(f"{import_dir}/products_product.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Product.objects.create(
                    id=int(row['id']),
                    sku=row['sku'] or None,
                    name=row['name'],
                    description=row['description'] or DEFAULT_DESCRIPTION,  # 關鍵修正
                    price=row['price'],
                    stock=int(row['stock']) if row['stock'] else 0,
                    category=category_map.get(int(row['category_id'])) if row['category_id'] else None,
                    is_active=row['is_active'].lower() in ('true', '1', 'yes', 't'),
                    tag=row['tag'] or DEFAULT_TAG,      # 關鍵修正：空值轉預設
                    brand=row['brand'] or DEFAULT_BRAND,  # 關鍵修正：空值轉預設
                    product_img=row['product_img'] or 'products/default.jpg',
                    product_img1=row['product_img1'] or 'products/default.jpg',
                    product_img2=row['product_img2'] or 'products/default.jpg',
                )
        print("📥 匯入 products_product.csv（使用預設值避免 NULL）")
    print("✅ 商品資料已成功匯入")

def generate_fake_data():
    """生成測試資料（確保 brand/tag 有值）"""
    from django.utils import timezone
    import random

    Product.objects.all().delete()
    Category.objects.all().delete()

    # 建立分類（description 設為空字串）
    cat1 = Category.objects.create(
        name="清潔用品",
        description=DEFAULT_DESCRIPTION,
        category_img="products/default.jpg"
    )
    cat2 = Category.objects.create(
        name="廚房用品",
        description=DEFAULT_DESCRIPTION,
        category_img="products/default.jpg"
    )

    # 從 choices 取值（確保存在）
    from products.choices import brand_choices, tag_choices
    brands = list(brand_choices.keys())
    tags = list(tag_choices.keys())

    for i in range(5):
        Product.objects.create(
            sku=f"SKU{i:04d}",
            name=f"測試商品 {i+1}",
            description=DEFAULT_DESCRIPTION,
            price=round(random.uniform(50, 500), 2),
            stock=random.randint(0, 100),
            category=random.choice([cat1, cat2]),
            is_active=True,
            tag=random.choice(tags),
            brand=random.choice(brands),
            product_img="products/default.jpg",
            product_img1="products/default.jpg",
            product_img2="products/default.jpg"
        )
    print("✅ 已生成測試商品（brand/tag 使用有效值）")

class Command(BaseCommand):
    help = 'CRAN 商品資料工具（方案 B：不改模型，用預設值）'

    def handle(self, *args, **options):
        while True:
            print("\n" + "="*50)
            print("📦 商品資料工具（預設值模式）")
            print("="*50)
            print("1. 清空 Category 與 Product")
            print("2. 匯出完整商品資料")
            print("3. 匯入完整商品資料")
            print("4. 生成測試商品")
            print("0. 離開")
            print("-"*50)

            choice = input("請選擇功能 (0-4): ").strip()
            if choice == '1':
                confirm = input("⚠️  確定清空？(y/N): ")
                if confirm.lower() == 'y':
                    clear_database()
            elif choice == '2':
                export_to_csv()
            elif choice == '3':
                confirm = input("⚠️  匯入會覆蓋現有商品，確定？(y/N): ")
                if confirm.lower() == 'y':
                    import_from_csv()
            elif choice == '4':
                generate_fake_data()
            elif choice == '0':
                break
            else:
                print("❌ 無效選項")