import copy
import logging

from collections import defaultdict

from django.db import models, transaction
from django.db.models import ManyToOneRel, ManyToManyField, OneToOneRel
from django.db.models.fields import related_descriptors

__all__ = ('CloneableModelMixin',)

logging.basicConfig(level=logging.DEBUG)


class CloneableModelMixin(object):
    """Adds a ``clone`` method to models.

    Now works only with many-to-one and many-to-many relations.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids = defaultdict(set)
        self.map = defaultdict(dict)
        self.heap = defaultdict(dict)

    @transaction.atomic
    def _one_to_one_clone(self, model, new_model, relation, config, ext):
        """Clone one-to-one relations.

        There is only specified for ``modules`` models with ``ptr` relation.

        """
        accessor_name = relation.get_accessor_name()
        attname = relation.field.attname

        try:
            obj = getattr(model, accessor_name)
        except models.ObjectDoesNotExist as e:
            return

        ObjModel = obj._meta.model

        new_obj = ObjModel.objects.create(
            module_ptr_id=new_model.id,
            conference_id=new_model.conference_id,
            title=new_model.title
        )

        logging.debug('Clone O2O {0}.{1} => {2}.{3} ({4})'.format(
            model._meta.label_lower, model.id,
            new_model._meta.label_lower, new_model.id, ext
        ))

        self._recursive_clone(obj, new_obj, config)

    @transaction.atomic
    def _many_to_one_clone(self, model, new_model, relation, config, ext):
        """Clone many-to-one relations.

        Gets ``accessor_name`` -- name of objects that has m2o relationship
        from the field, create a copy of objects these available by the
        accessor name and make copy for each object with new parent`s ID.

        Only ``ForeignKey`` relations. Also ``ForeignKey`` from
        m2m with intermediary ``through`` model.

        """
        accessor_name = relation.get_accessor_name()
        attname = relation.field.attname
        allowed = config.keys()
        config = config.get(accessor_name, {})

        if accessor_name:
            objects = getattr(model, accessor_name)

            for obj in objects.all():
                label_lower = obj._meta.label_lower

                if obj.id in self.ids[label_lower]:
                    att = getattr(obj, attname, None)
                    clone_map = self.map[label_lower]

                    if clone_map.get(obj.id):
                        old_obj = self.heap[label_lower].get(
                            clone_map.get(obj.id)
                        )
                        setattr(old_obj, attname, clone_map.get(att))
                        old_obj.save(update_fields=[attname])

                    logging.debug('Skip M2O {0}.{1}'.format(
                        label_lower, obj.id
                    ))

                    continue

                new_obj = copy.copy(obj)
                new_obj.pk = None
                new_kwargs = ext or {}
                new_kwargs[attname] = new_model.pk

                for key, value in new_kwargs.items():
                    setattr(new_obj, key, value)

                new_obj.save()

                self.ids[label_lower].add(obj.id)
                self.ids[label_lower].add(new_obj.id)
                self.map[label_lower].update({obj.id: new_obj.id})
                self.heap[label_lower].update({new_obj.id: new_obj})

                if obj._meta.model is not new_model._meta.model:
                    new_kwargs.update({attname: new_model.id})

                logging.debug('Clone M2O {0}.{1} => {2}.{3} ({4})'.format(
                    model._meta.label_lower, model.id,
                    new_model._meta.label_lower, new_model.id, ext
                ))

                self._recursive_clone(obj, new_obj, config, new_kwargs)

    @transaction.atomic
    def _many_to_many_clone(self, model, new_model, relation, config, ext):
        """Clone many-to-many relations.

        Get objects for m2m relationship excludes objects with ``through``
        (these objects do not have ``auto_created``) and save to new
        model uses ``add`` method. Objects, these have given for the relation,
        do not create, it are same object with relation through new auto
        created intermediary table.

        """
        attname = relation.get_attname()
        allowed = config.keys()

        if (attname
                and relation.rel.through._meta.auto_created):
            objects = list(getattr(model, attname).all())
            new_objects = []

            for obj in objects:
                label_lower = obj._meta.label_lower

                if obj.id in self.ids[label_lower]:
                    logging.debug('Skip M2M {0}.{1}'.format(
                        label_lower, obj.id
                    ))

                    continue

                new_obj = copy.copy(obj)
                new_obj.pk = None
                new_obj.save()
                new_objects.append(new_obj)

                logging.debug('Clone M2M {0}.{1} => {2}.{3} ({4})'.format(
                    obj._meta.label_lower, obj.id,
                    new_obj._meta.label_lower, new_obj.id, ext
                ))

                self._recursive_clone(obj, new_obj, config, ext)

            getattr(new_model, attname).add(*new_objects)

    def _recursive_clone(self, model, new_model, config=None, ext=None):
        """Recursive clone.

        Clone related object for each field of the model.

        Args:
            self (object): A ``self`` instance of the object.
            model (object): A Django`s model object that will be cloned.
            config (dict): Names of related models that will be included.

        """
        config = config or {}

        for rel in model._meta.get_fields():
            if isinstance(rel, OneToOneRel):
                self._one_to_one_clone(model, new_model, rel, config, ext)
            elif isinstance(rel, ManyToOneRel):
                self._many_to_one_clone(model, new_model, rel, config, ext)
            elif isinstance(rel, ManyToManyField):
                self._many_to_many_clone(model, new_model, rel, config, ext)

    def clone(self, config=None):
        """Method for clone model instance.

        Args:
            self (object): An instance of the model.
            config (dict): Names of related models that will be included.

        """
        model = self
        config = config or self.CLONE_SETTINGS
        config = config if isinstance(config, dict) else {}
        new_model = copy.copy(model)
        new_model.pk = None

        new_model.save()

        self.ids[model._meta.label_lower] = {model.id, new_model.id}
        self.map[model._meta.label_lower].update({model.id: new_model.id})
        self.heap[model._meta.label_lower].update({new_model.id: new_model})

        self._recursive_clone(model, new_model, config)

        logging.debug(self.ids)
        logging.debug(self.map)
        logging.debug(self.heap)

        return new_model
