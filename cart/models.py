from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class CartItem(models.Model):
    """
    購物車項目模型，支援登入用戶（user）與匿名用戶（session_key）
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="登入用戶；若為匿名用戶則為 null"
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text="匿名用戶的 session key；若為登入用戶則為 null"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="關聯的商品"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="商品數量"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="加入時間"
    )

    class Meta:
        # 確保每個用戶或 session 只能有一筆同商品的記錄
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product',
                condition=models.Q(user__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['session_key', 'product'],
                name='unique_session_product',
                condition=models.Q(session_key__isnull=False)
            ),
            # 業務邏輯：user 和 session_key 必須有且僅有一個非空
            models.CheckConstraint(
                check=(
                    models.Q(user__isnull=False, session_key__isnull=True) |
                    models.Q(user__isnull=True, session_key__isnull=False)
                ),
                name='user_or_session_key'
            )
        ]
        ordering = ['-added_at']

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.product.name} (x{self.quantity})"
        else:
            return f"Session {self.session_key[:8]}... - {self.product.name} (x{self.quantity})"