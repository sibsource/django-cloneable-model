# Django Cloneable Model

```python
from django.db import models
  
from cloneable_model.models import CloneableModelMixin


class News(CloneableModelMixin, models.Model):
    CLONE_CONFIG = {
        'comment_set': {}
    }

    title = models.CharField(max_length=255)


class Comment(models.Model):
    news = models.ForeignKey(News)
    text = models.TextField()
```

```python
item = News.objects.get(pk=1)
item.comments.values_list('id', flat=True)  # [1, 2, 3]
```

```python
new_item = item.clone()
new_item.pk  # 2
new_item.comment_set.values_list('id', flat=True)  # [4, 5, 6]
```

```python
new_item = item.clone(config={})
new_item.pk  # 3
new_item.comment_set.values_list('id', flat=True)  # []
```
