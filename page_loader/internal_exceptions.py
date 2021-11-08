

class PageLoaderError(Exception):
    pass


class ResourceSavingError(PageLoaderError):
    pass


class PageRequestError(PageLoaderError):
    pass
