from django.db import models

import uuid
# Create your models here.


class OrganSystem(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=128, verbose_name="身体系统")

    class Meta:
        verbose_name = "身体系统"
        verbose_name_plural = "身体系统"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class BodyPart(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, auto_created=True, editable=False)

    name = models.CharField(max_length=128, verbose_name="部位名称")

    parent = models.ForeignKey(verbose_name="父级部位", to="self", on_delete=models.CASCADE,
                               related_name="pid", to_field="id", db_constraint=False)

    incidence = models.IntegerField(
        verbose_name="发病率", choices=((0, "低"), (1, "中"), (2, "高")))

    class Meta:
        verbose_name = "身体部位"
        verbose_name_plural = "身体部位"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Symptom(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, auto_created=True, editable=False)

    name = models.CharField(max_length=128, verbose_name="症状名称")

    accuracy = models.IntegerField(
        verbose_name="明显程度", choices=((0, "无法理解"), (1, "部分理解"), (2, "十分显著")))

    body_part = models.ForeignKey(verbose_name="身体部位", to="BodyPart",
                                  on_delete=models.DO_NOTHING, related_name="symptoms", db_constraint=False)

    organ_system = models.ForeignKey(verbose_name="身体系统", to="OrganSystem",
                                     on_delete=models.DO_NOTHING, related_name="symptoms", db_constraint=False)

    class Meta:
        verbose_name = "症状"
        verbose_name_plural = "症状"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Disease(models.Model):

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, auto_created=True, editable=False)

    name = models.CharField(max_length=128, verbose_name="疾病名称")

    incidence = models.IntegerField(
        verbose_name="发病率", choices=((0, "低"), (1, "中"), (2, "高")))

    class Meta:
        verbose_name = "疾病"
        verbose_name_plural = "疾病"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class SymptomToDisease(models.Model):
    """疾病-症状关系表
    """

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, auto_created=True, editable=False)

    symptom = models.ForeignKey(verbose_name="症状", to="Symptom",
                                on_delete=models.DO_NOTHING, to_field="id", db_constraint=False, related_name="symptoms")

    disease = models.ForeignKey(verbose_name="疾病", to="Disease",
                                on_delete=models.DO_NOTHING, to_field="id", db_constraint=False, related_name="dieases")

    relevence = models.IntegerField(
        verbose_name="关联程度", choices=((0, "次要"), (1, "重要"), (2, "必要")))

    class Meta:
        verbose_name = "疾病-症状 标注"
        verbose_name_plural = "疾病-症状 标注"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
