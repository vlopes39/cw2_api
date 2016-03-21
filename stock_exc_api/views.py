from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from stock_exc_api.models import StockExchangeIndex, Country, Historical_Data
from stock_exc_api.serializers import StockExchangeIndexSerializer,StockExchangeIndexDetailSerializer,CountrySerializer,HistDataSerializer, IndexCountry
from rest_framework import generics
from rest_framework import filters

class IndexesList(generics.ListCreateAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = StockExchangeIndexSerializer

class IndexesDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = StockExchangeIndexDetailSerializer
	lookup_field = 'name'

class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = IndexCountry
	lookup_field = 'name'

class IndexesListPerCountry(generics.ListCreateAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = StockExchangeIndexSerializer
	lookup_field = 'name'
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('country',)

class HistData(generics.RetrieveUpdateDestroyAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = HistDataSerializer
	lookup_field = 'name'
'''

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json' # define media type as JSON
        super(JSONResponse, self).__init__(content, **kwargs)

'''
'''

# Put simply, decorators wrap a function, modifying its behavior.
# CSRF token compare the key of original data and posted data. POST is safe(???), but the origin of data is not. 
#@csrf_exempt 

@api_view(['GET', 'POST'])
def indexes_list(request, format=None):
    """
    List all indexes, or create a new index.
    """
    if request.method == 'GET':
        indexes = StockExchangeIndex.objects.all()
        serializer = StockExchangeIndexSerializer(indexes, many=True) # many=True to serialize querysets instead of model instances
        return Response(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request) # parse the data coming in JSON
        serializer = StockExchangeIndexSerializer(data=request.data) # deserialize
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def indexes_detail(request, country, format=None):
    """
    Retrieve, update or delete an index.
    """
    try:
        index = StockExchangeIndex.objects.get(country=country)
    except StockExchangeIndex.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StockExchangeIndexSerializer(index)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = StockExchangeIndexSerializer(index, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        index.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''