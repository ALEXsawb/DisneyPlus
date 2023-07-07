def invalid_update(function):
    async def wrapper(*args, **kwargs):
        result = await function(*args, **kwargs)
        if not result.raw_result['nModified']:
            raise ValueError('The update was not completed')
        return result
    return wrapper
