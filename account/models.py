from django.db import models
from django.contrib.auth.models import User


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fllowers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    #### adding new field after migration ####
    # ! ERROR for previous data because the dont have new fields:
    # sulotion:
    # 1_ Delete Databse and create again
    # 2_ put default value =>     default='empty'
    # 3_ put null value => null = True, blank = True

    def __str__(self):
        return f'{self.from_user} TO {self.to_user}'