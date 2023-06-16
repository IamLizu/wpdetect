import validators

def isUrl(string):
    return validators.url(string)

def splitArray(array, n):
    final = [array[i * n:(i + 1) * n] for i in range((len(array) + n - 1) // n )]
    return final
