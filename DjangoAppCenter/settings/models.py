import json
from datetime import datetime

# from Crypto.Cipher import AES
from django.core.management import utils
from django.db import models


def random_secret():
    return utils.get_random_string(16)


class NameSpace(models.Model):
    name = models.CharField(verbose_name='配置命名空间', unique=True, max_length=128, null=False, blank=False)
    description = models.CharField(verbose_name='描述', max_length=255, null=False, blank=False)
    secret = models.CharField(verbose_name='配置获取密码', help_text='采用AES算法, 16位密钥', max_length=16,
                              default=random_secret,
                              null=False, blank=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True, editable=False)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'name_space'
        verbose_name = '命名空间'
        verbose_name_plural = '命名空间'


class ConfigItem(models.Model):
    namespace = models.ForeignKey('NameSpace', verbose_name='归属命名空间', on_delete=models.CASCADE,
                                  db_constraint=False, related_name='config_items')
    key = models.CharField(verbose_name='配置KEY', max_length=128, null=False, blank=False)
    value = models.CharField(verbose_name='配置内容', max_length=4096, null=False, blank=False)
    description = models.CharField(verbose_name='描述', max_length=128, null=True, blank=True)
    enable = models.BooleanField(verbose_name='是否启用', default=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True, editable=False)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, editable=False)

    def __str__(self):
        return f'{self.namespace}.{self.key}'

    class Meta:
        db_table = 'config_item'
        verbose_name = '配置项'
        verbose_name_plural = '配置项'


class ConfigSnapShot(models.Model):
    version = models.UUIDField(verbose_name='版本号', null=True, blank=True, editable=False)
    latest = models.BooleanField(verbose_name='是否是最新版本', editable=False, default=False)
    publish_time = models.DateTimeField(verbose_name='创建时间', auto_created=True, auto_now_add=True, editable=False)
    config = models.JSONField(verbose_name='配置内容JSON', editable=False)

    class Meta:
        db_table = 'config_snapshot'
        verbose_name = '配置快照'
        verbose_name_plural = '配置快照'

    def save(self, *args, **kwargs):
        if not self.version:
            self.version = datetime.now().strftime("%Y%m%d%H%M%S")

        super().save(*args, **kwargs)

    @classmethod
    def publish(cls) -> 'ConfigSnapShot':
        # 查询出所有的namespace
        namespaces = NameSpace.objects.all().prefetch_related('config_items')
        config = {}
        # 遍历namespace
        for namespace in namespaces:
            config = {}
            # 查询出namespace下的所有配置项
            items = namespace.config_items.all().filter(enable=True)
            # 遍历配置项
            for item in items:
                # 将配置项添加到config字典中
                config[item.key] = item.value

        snapshot = ConfigSnapShot(latest=True, config=config)
        snapshot.save()
        return snapshot

    @classmethod
    def rollback(cls, version: str) -> 'ConfigSnapShot':
        snapshot = ConfigSnapShot.objects.filter(version=version).first()
        if not snapshot:
            raise ValueError(f'版本号[{version}]不存在')
        ConfigSnapShot.objects.filter(latest=True).update(latest=False)
        snapshot.latest = True
        snapshot.save()
        return snapshot

    # @classmethod
    # def aes_encrypt(cls, text, key):
    #     obj = AES.new(key, AES.MODE_CBC, key)
    #     padding = 16 - len(text) % 16
    #     text += padding * bytes([padding])
    #     ciphertext = obj.encrypt(text)
    #     return base64.b64encode(ciphertext).decode('utf-8')
    #
    # @classmethod
    # def aes_decrypt(cls, ciphertext, key):
    #     obj = AES.new(key, AES.MODE_CBC, key)
    #     plaintext = obj.decrypt(base64.b64decode(ciphertext))
    #     padding = plaintext[-1]
    #     return plaintext[:-padding].decode()

    @classmethod
    def fetch(cls, namespace: str) -> dict:
        namespace = NameSpace.objects.filter(namespace=namespace).first()
        if not namespace:
            raise ValueError(f'namespace[{namespace}]不存在')

        snapshot = ConfigSnapShot.objects.filter(namespace__namespace=namespace, latest=True).first()
        if not snapshot:
            raise ValueError(f'配置未发布')

        return json.loads(snapshot.config)

    # @classmethod
    # def safe_fetch(cls, namespace: str) -> str:
    #     namespace = NameSpace.objects.filter(namespace=namespace).first()
    #     if not namespace:
    #         raise ValueError(f'namespace[{namespace}]不存在')
    #
    #     snapshot = ConfigSnapShot.objects.filter(namespace__namespace=namespace, latest=True).first()
    #     if not snapshot:
    #         raise ValueError(f'配置未发布')
    #
    #     ciphertext = cls.aes_encrypt(snapshot.config.encode(), namespace.secret.encode())
    #     return ciphertext
