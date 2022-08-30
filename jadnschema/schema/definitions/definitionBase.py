from typing import Any, ClassVar, Tuple
from pydantic.main import ModelMetaclass
from .options import Options
from .field import getFieldSchema
from ..consts import SELECTOR_TYPES, STRUCTURED_TYPES
from ..baseModel import BaseModel
from ...utils import classproperty, ellipsis_str


class DefinitionMeta(ModelMetaclass):
    def __new__(mcs, name, bases, attrs, **kwargs):
        opts = Options(
            attrs.pop("__options__", None), attrs.pop("Options", None),
            kwargs.pop("__options__", None), kwargs.pop("Options", None),
            getattr(mcs, "__options__", None), getattr(mcs, "Options", None),
        )
        base_opts = [b.__options__ for b in reversed(bases) if issubclass(b, BaseModel) and b != BaseModel]
        opts = Options(*base_opts, opts)
        new_namespace = {
            **attrs,
            **kwargs,
            "__options__": opts,
        }
        cls = super().__new__(mcs, name, bases, new_namespace)
        base_names = [b.__name__ for b in bases]
        for idx, (field, opts) in enumerate(cls.__fields__.items()):
            if field != "__root__":
                opts.field_info.extra["parent"] = cls
                field_opts = opts.field_info.extra.get("options", Options())
                field_opts = opts.field_info.extra["options"] = Options(field_opts)
                opts.field_info.extra.setdefault("id", idx)
                if not opts.required and field_opts.minc != 0 and "Choice" not in base_names:
                    field_opts.minc = 0
        return cls


class DefinitionBase(BaseModel, metaclass=DefinitionMeta):
    __options__: ClassVar[Options]

    @classproperty
    def name(cls):
        return cls.__options__.name or cls.__name__

    def __str__(self):
        cls = self.__class__
        mro = [c for c in cls.__mro__ if not c.__name__ == cls.__name__][0]
        data = self.json(exclude_none=True)
        return f"{self.name}({mro.__name__}: {ellipsis_str(data)})"

    # Pydantic overrides
    @classmethod
    def schema(cls) -> list:
        mro = [c for c in cls.__mro__ if not c.__name__ == cls.__name__][0]
        schema = [cls.name, mro.__name__, cls.__options__.schema(), (cls.__doc__ or "").strip()]
        if cls.__fields__ and "__root__" not in cls.__fields__:
            fields = []
            for field, opt in cls.__fields__.items():
                fields.append(getFieldSchema(opt))
            schema.append(fields)
        return schema

    # Custom Methods
    @classmethod
    def is_enum(cls) -> bool:
        for base in cls.__mro__:
            if base.__name__ == "Enumerated":
                return True
        return False

    @classmethod
    def is_structure(cls) -> bool:
        for base in cls.__mro__:
            if base.__name__ in STRUCTURED_TYPES:
                return True
        return False

    @classmethod
    def is_selector(cls) -> bool:
        for base in cls.__mro__:
            if base.__name__ in SELECTOR_TYPES:
                return True
        return False

    @classmethod
    def has_fields(cls) -> bool:
        return cls.is_selector() or cls.is_structure()

    # Dict-like functions
    def items(self) -> Tuple[Tuple[str, Any], ...]:
        items = []
        if self.has_fields():
            for field in self.__fields__:
                if val := getattr(self, field, None):
                    items.append((field, val))
        return tuple(items)

    class Config:
        arbitrary_types_allowed = True
