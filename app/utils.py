from django.core.serializers.python import Serializer
import json
from decimal import Decimal

class ExpensesSerializer(Serializer):
    def get_dump_object(self, obj):
        dump_object={}
        dump_object.update({'title':obj.title})
        dump_object.update({'category':obj.category})
        dump_object.update({'amount':"{}".format(obj.amount)})
        dump_object.update({'description':obj.description})
        dump_object.update({'dateUsage':"{}".format(obj.dateUsage)})
        dump_object.update({'expenses_id':obj.id})

        return dump_object 
    
