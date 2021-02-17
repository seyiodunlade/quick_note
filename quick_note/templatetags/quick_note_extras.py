from django import template

register = template.Library()

'''

    def custom(value, arg):
    
        return something

'''


def getValueAtIndex(dList, dIndex):

    return dList[dIndex]


register.filter('getValueAtIndex', getValueAtIndex)
