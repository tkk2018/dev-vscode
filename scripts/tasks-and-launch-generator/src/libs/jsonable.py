import datetime
import decimal

class Jsonable(object):
    """
    https://stackoverflow.com/a/28253689/16027098
    There are some changes to make it compatible with Python 3.
    """

    def __iter__(self):
        if sys.version_info[0] >= 3:
            for attr, value in self.__dict__.items():
                if isinstance(value, datetime.datetime):
                    iso = value.isoformat()
                    yield attr, iso
                elif isinstance(value, decimal.Decimal):
                    yield attr, str(value)
                elif hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
                    if hasattr(value, "pop"):
                        a = []
                        for subval in value:
                            if hasattr(subval, "__iter__") and not isinstance(subval, (str, bytes)):
                                try:
                                    a.append(dict(subval))
                                except (TypeError, ValueError):
                                    a.append(subval)
                            else:
                                a.append(subval)
                        yield attr, a
                    else:
                        try:
                            yield attr, dict(value)
                        except (TypeError, ValueError):
                            yield attr, list(value)
                else:
                    yield attr, value

        else:
            for attr, value in self.__dict__.iteritems():
                if isinstance(value, datetime.datetime):
                    iso = value.isoformat()
                    yield attr, iso
                elif isinstance(value, decimal.Decimal):
                    yield attr, str(value)
                elif(hasattr(value, '__iter__')):
                    if(hasattr(value, 'pop')):
                        a = []
                        for subval in value:
                            if(hasattr(subval, '__iter__')):
                                a.append(dict(subval))
                            else:
                                a.append(subval)
                        yield attr, a
                    else:
                        yield attr, dict(value)
                else:
                    yield attr, value
