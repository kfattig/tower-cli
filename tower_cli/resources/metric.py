from tower_cli import models, resources, exceptions


class Resource(models.BaseResource):
    """A resource for a metric calcualted by Ansible Tower

    This resource is read-only.
    """
    cli_help = 'Metric data calculated by Ansible Tower'
    endpoint = '/metrics/'

    value = models.Field()
    labels = models.Field()

    def __getattribute__(self, attr):
        if attr in ['create', 'delete', 'modify']:
            raise AttributeError
        return super(Resource, self).__getattribute__(attr)

    @resources.command(use_fields_as_options=False)
    def list(self, **kwargs):
        """Return a list of objects.

        =====API DOCS=====
        Retrieve a list of Tower metrics.

        :param `**kwargs`: Keyword arguments used for searching resource objects.
        :returns: A JSON object containing details of all metric objects returned by Tower backend.
        :rtype: dict

        =====API DOCS=====
        """
        kwargs['format'] = 'json'
        result = super(Resource, self).list(**kwargs)
        return {
            'results': [{'id': k, 'value': v['value'], 'labels': v['labels']} for k, v in result.items()]
        }

    @resources.command(use_fields_as_options=False)
    def get(self, pk):
        """Return one and exactly one object

        =====API DOCS=====
        Return one and exactly one Tower metric.
        :type pk: string
        :returns: loaded JSON of the retrieved Tower metric.
        :rtype: dict
        :raises tower_cli.exceptions.NotFound: When no specified Tower setting exists.

        =====API DOCS=====
        """
        # The Tower API doesn't provide a mechanism for retrieving a single
        # setting value at a time, so fetch them all and filter
        try:
            return next(s for s in self.list()['results'] if s['id'] == pk)
        except StopIteration:
            raise exceptions.NotFound('The requested metric could not be found.')
