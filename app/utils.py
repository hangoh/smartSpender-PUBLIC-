from django.core.serializers.python import Serializer

class ExpensesSerializer(Serializer):
    def get_dump_object(self, obj):
        dump_object={}
        dump_object.update({'category',obj.category})
        dump_object.update({'amount',obj.amount})
        dump_object.update({'description',obj.description})
        dump_object.update({'dateUsage',obj.dateUsage})
        dump_object.update({'expenses_id',obj.id})
        return dump_object 