import json

from django.contrib import admin
from django.core.cache import cache
from django.http import JsonResponse
from simpleui.admin import AjaxAdmin

from DjangoAppCenter.settings.models import ConfigItem, NameSpace, ConfigSnapShot


class ConfigItemInline(admin.TabularInline):
    model = ConfigItem
    extra = 0


class NameSpaceAdmin(AjaxAdmin):
    list_display = ['name', 'description', 'create_time', 'update_time']
    inlines = [ConfigItemInline]
    actions = ['publish', 'copy']

    def publish(self, request, queryset):
        """
        发布当前版本的配置
        :param request:
        :param queryset:
        :return:
        """
        name_spaces = list(queryset)
        count = len(name_spaces)

        if count == 0:
            return JsonResponse(data={
                'status': 'error',
                'msg': '请至少选中一个NameSpace！'
            })

        if count > 1:
            return JsonResponse(data={
                'status': 'error',
                'msg': '一次只能选择一个NameSpace！'
            })

        config_dict = {}
        for item in ConfigItem.objects.filter(namespace=name_spaces[0], enable=True).values('key', 'value'):
            try:
                value = json.loads(item.get('value'))
            except:
                try:
                    value = eval(item.get('value'))
                except:
                    value = item.get('value')

            config_dict[item.get('key')] = value

        ConfigSnapShot.objects.filter(namespace=name_spaces[0]).update(latest=False)
        ConfigSnapShot(namespace=name_spaces[0], latest=True, config=json.dumps(config_dict, indent=2)).save()
        cache.clear()
        return JsonResponse(data={
            'status': 'success',
            'msg': '发布成功!'
        })

    publish.short_description = '发布'
    publish.type = 'success'
    publish.icon = 'el-icon-s-promotion'
    publish.layer = {
        'title': '确定要发布当前命名空间下的所有配置？',
        'tips': f'请选中一个命名空间进行发布!',
        # 确认按钮显示文本
        'confirm_button': '发布',
        # 取消按钮显示文本
        'cancel_button': '取消',
        # 弹出层对话框的宽度，默认50%
        'width': '32%',
    }

    def copy(self, request, queryset):
        """
        从一个已有的命名空间复制
        """
        _namespace = request.POST.get('namespace')
        _new_namespace = request.POST.get('new_namespace')
        if not _namespace:
            return JsonResponse(data={
                'status': 'error',
                'msg': '源命名空间不允许为空！'
            })
        if not _new_namespace:
            return JsonResponse(data={
                'status': 'error',
                'msg': '新命名空间不允许为空！'
            })
        namespace = NameSpace.objects.filter(namespace=_namespace).first()
        if not namespace:
            return JsonResponse(data={
                'status': 'error',
                'msg': f'命名空间[{_namespace}]不存在！'
            })

        new_namespace = NameSpace(namespace=_new_namespace, description=namespace.description)
        new_namespace.save()
        # 复制所有的配置项
        config_items = ConfigItem.objects.filter(namespace__namespace=_namespace)
        for item in config_items:
            ConfigItem(namespace=new_namespace, key=item.key, value=item.value, description=item.description).save()

        return JsonResponse(data={
            'status': 'success',
            'msg': f'复制成功！新的命名空间名为{_new_namespace}'
        })

    copy.layer = {
        'title': '从一个已有命名空间复制',
        # 确认按钮显示文本
        'confirm_button': '复制',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '32%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "120px",
        'params': [
            {
                'type': 'input',
                'key': 'namespace',
                'label': '源命名空间',
            },
            {
                'type': 'input',
                'key': 'new_namespace',
                'label': '新命名空间',
            }
        ]
    }

    copy.short_description = '复制'
    copy.type = 'success'
    copy.icon = 'el-icon-s-promotion'


class ConfigSnapShotAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'latest', 'publish_time')
    readonly_fields = ('id', 'version', 'latest', 'publish_time', 'config')


admin.site.register(NameSpace, NameSpaceAdmin)
admin.site.register(ConfigSnapShot, ConfigSnapShotAdmin)
