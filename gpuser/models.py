from django.db import models


# Create your models here.
class GPUInfo(models.Model):
    id = models.AutoField(primary_key=True)
    device_id = models.IntegerField()
    pid = models.IntegerField(null=True)
    username = models.CharField(max_length=32, null=True)
    fetch_time_id = models.ForeignKey("FetchTime", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Server(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class FetchTime(models.Model):
    id = models.AutoField(primary_key=True)
    fetch_time = models.DateTimeField(auto_now_add=True)
    server_id = models.ForeignKey("Server", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
