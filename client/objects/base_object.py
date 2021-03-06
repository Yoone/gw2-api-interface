from client import GuildWars2Client


class BaseAPIObject:
    """
    Base Resource handler that provides common properties
     and methods to be used by child resources.

    Can only be used once one or more `GuildWars2Client`
     have been instantiated to make sure that the `requests.Session()`
     object has been correctly set.
    """

    def __init__(self, object_type):
        """
        Initializes a **base** API object. Primarily acts as an interface
         for all child object to use.

        >>> import requests
        >>>
        >>> session = requests.Session()
        >>> object_type = 'guild'
        >>>
        >>> base_api_object = BaseAPIObject(session, object_type)

        :param object_type: String indicating what type of object to
                             interface with (i.e. 'guild'). Primarily
                             acts as the relative path to the base URL
        :raises ValueError: In the event that either a `Session` object
                             or `object_type` are not set.
        """
        if not object_type:
            raise ValueError('API Object requires `object_type` to be passed for %s'
                             .format(self.__class__.__name__))

        assert GuildWars2Client.session

        self.session = GuildWars2Client.session
        self.object_type = object_type

        self.base_url = GuildWars2Client.BASE_URL
        self.version = GuildWars2Client.VERSION

    def get(self, url=None, **kwargs):
        """Get a resource for specific object type"""

        # Done to allow cases where we need to call a specific endpoint
        #  without re-implementing the same method. If we specify the
        #  endpoint, ignore everything else and just sent the request
        if not url:
            request_url = self._build_endpoint_base_url()

            id = kwargs.get('id')
            page = kwargs.get('page')
            page_size = kwargs.get('page_size')

            if id:
                request_url += '/' + str(id)  # {base_url}/{object}/{id}

            if page or page_size:
                request_url += '?'  # {base_url}/{object}?page={page}&page_size={page_size}

            if page:
                request_url += 'page={page}&'.format(page=page)

            if page_size:
                assert 0 < page_size <= 200
                request_url += 'page_size={page_size}'.format(page_size=page_size)

            request_url.strip('&')  # Remove any trailing ampersand
        else:
            request_url = url

        return self.session.get(request_url)

    def _build_endpoint_base_url(self):
        """Construct the base URL to access an API object"""
        return '{base_url}/{version}/{object}'.format(base_url=self.base_url,
                                                      version=self.version,
                                                      object=self.object_type)

    def __repr__(self):
        return '<BaseAPIObject %r\nType: %r>' % (self.session, self.object_type)
