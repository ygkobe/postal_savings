from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'jobs'

        indexes = [
            models.Index(fields=['title'], name='title1_idx'),
            models.Index(fields=['created_at'], name='created1_at_idx'),
        ]

        ordering = ['-created_at']  # 按 created_at 降序排序
