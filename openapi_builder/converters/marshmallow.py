from typing import Union

import marshmallow

from openapi_builder.converters import Converter, register_converter
from openapi_builder.specification import Reference, Schema


class EmailConverter(Converter):
    converts_class = marshmallow.fields.Email

    def convert(self, value) -> Schema:
        return Schema(type="string", format="email")


class StringConverter(Converter):
    converts_class = marshmallow.fields.String

    def convert(self, value) -> Schema:
        return Schema(type="string", format="string")


class BooleanConverter(Converter):
    converts_class = marshmallow.fields.Boolean

    def convert(self, value) -> Schema:
        return Schema(type="boolean", format="boolean")


class NumberConverter(Converter):
    converts_class = marshmallow.fields.Number

    def convert(self, value) -> Schema:
        return Schema(type="number", format=None)


class IntegerConverter(Converter):
    converts_class = marshmallow.fields.Integer

    def convert(self, value) -> Schema:
        return Schema(type="integer", format="int32")


class FloatConverter(Converter):
    converts_class = marshmallow.fields.Float

    def convert(self, value) -> Schema:
        return Schema(type="number", format=None)


class UUIDConverter(Converter):
    converts_class = marshmallow.fields.Float

    def convert(self, value) -> Schema:
        return Schema(type="string", format="uuid")


class DecimalConverter(Converter):
    converts_class = marshmallow.fields.Decimal

    def convert(self, value) -> Schema:
        return Schema(type="number", format=None)


class DateConverter(Converter):
    converts_class = marshmallow.fields.Date

    def convert(self, value) -> Schema:
        return Schema(type="string", format="date")


class DateTimeConverter(Converter):
    converts_class = marshmallow.fields.DateTime

    def convert(self, value) -> Schema:
        return Schema(type="string", format="date-time")


class TimeConverter(Converter):
    converts_class = marshmallow.fields.Time

    def convert(self, value) -> Schema:
        return Schema(type="string", format="time")


class URLConverter(Converter):
    converts_class = marshmallow.fields.URL

    def convert(self, value) -> Schema:
        return Schema(type="string", format="URL")


class NestedConverter(Converter):
    converts_class = marshmallow.fields.Nested

    def convert(self, value) -> Union[Schema, Reference]:
        schema = self.builder.process(value.nested)
        if value.many:
            schema = Schema(type="array", items=schema)
        return schema


class ListConverter(Converter):
    converts_class = marshmallow.fields.List

    def convert(self, value) -> Schema:
        return Schema(type="array", items=None)


class SchemaMetaConverter(Converter):
    converts_class = marshmallow.schema.SchemaMeta

    def convert(self, value) -> Schema:
        # instantiating a SchemaMeta creates a Schema
        return self.builder.process(value=value())


class SchemaConverter(Converter):
    converts_class = marshmallow.schema.Schema

    def convert(self, value) -> Schema:
        schema_name = value.__class__.__name__  # class name
        properties = {
            key: self.builder.process(value=prop, name=f"{schema_name}.{key}")
            for key, prop in value._declared_fields.items()
        }

        self.builder.schemas[schema_name] = Schema(type="object", properties=properties)
        reference = Reference.from_schema(schema_name=schema_name)
        if value.many:
            return Schema(type="array", items=reference)
        return reference


class DictConverter(Converter):
    converts_class = marshmallow.fields.Dict

    def convert(self, value) -> Schema:
        return Schema(type="object")


def register_marshmallow_converters(builder):
    register_converter(EmailConverter(builder=builder))
    register_converter(StringConverter(builder=builder))
    register_converter(BooleanConverter(builder=builder))
    register_converter(NumberConverter(builder=builder))
    register_converter(IntegerConverter(builder=builder))
    register_converter(FloatConverter(builder=builder))
    register_converter(UUIDConverter(builder=builder))
    register_converter(DecimalConverter(builder=builder))
    register_converter(DateConverter(builder=builder))
    register_converter(DateTimeConverter(builder=builder))
    register_converter(TimeConverter(builder=builder))
    register_converter(URLConverter(builder=builder))
    register_converter(NestedConverter(builder=builder))
    register_converter(ListConverter(builder=builder))
    register_converter(SchemaConverter(builder=builder))
    register_converter(SchemaMetaConverter(builder=builder))
    register_converter(DictConverter(builder=builder))
