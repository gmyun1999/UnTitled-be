from typing import Type

from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DynamicNestedFieldSerializer(DynamicFieldsModelSerializer):
    class Meta:
        nested_serializers: dict[str, Type[serializers.Serializer]] = {}

    def __init__(self, *args, exclude_fields=None, **kwargs):
        self.exclude_fields = exclude_fields or {}
        super().__init__(*args, **kwargs)

        # 일반 필드 및 외래키 필드 제외 처리
        for field_name in self.exclude_fields.keys():
            if field_name in self.fields and not self._is_nested_field(field_name):
                self.fields.pop(field_name, None)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # 자동으로 외래키 필드를 탐색하여 exclude 처리를 동적으로 적용
        for field_name, serializer_class in self._get_meta_nested_serializers().items():
            if field_name in self.fields and getattr(instance, field_name, None):
                nested_data = serializer_class(getattr(instance, field_name)).data

                # exclude 처리된 필드 제거
                exclude_nested_fields = self.exclude_fields.get(field_name, [])
                for field in exclude_nested_fields:
                    nested_data.pop(field, None)
                representation[field_name] = nested_data

        return representation

    def _get_meta_nested_serializers(self):
        """
        메타 클래스에 정의된 nested_serializers를 자동으로 반환
        """
        return getattr(self.Meta, "nested_serializers", {})

    def _is_nested_field(self, field_name):
        """
        필드 이름이 외래키(Nested)인지
        """
        return field_name in self._get_meta_nested_serializers()
