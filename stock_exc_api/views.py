from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from stock_exc_api.models import StockExchangeIndex, Country, Historical_Data,Company
from django.shortcuts import get_object_or_404
from rest_framework import generics
from stock_exc_api.serializers import CountrySerializer, HistDataSerializer,CompanySerializer, StockExchangeIndexSerializer, StockExchangeIndexDetailSerializer, CountryDetailSerializer, HistDataDetailSerializer
import django_filters
from rest_framework import filters

class ListMixingHistData(object):
    def get(self, request, pk=None):
        queryset = self.get_queryset()
        index = get_object_or_404(queryset, pk=pk)
        serializer = HistDataDetailSerializer(index)
        return Response(serializer.data)

class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object

class AllowPUTAsCreateMixin(object):
    """
    The following mixin class may be used in order to support PUT-as-create
    behavior for incoming requests.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup_value = self.kwargs[lookup_url_kwarg]
            extra_kwargs = {self.lookup_field: lookup_value}
            serializer.save(**extra_kwargs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise
'''
class IndexesList(generics.ListCreateAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = StockExchangeIndexSerializer
    filter_backends = (filters.DjangoFilterBackend,)    
    #filter_field = 'country'   
'''
class IndexesList(generics.ListCreateAPIView):
    queryset = StockExchangeIndex.objects.all()
    serializer_class = StockExchangeIndexSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('country__name',)    

class IndexesDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = StockExchangeIndexDetailSerializer
	#lookup_field = 'name'

class CountryDetail(generics.RetrieveAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = CountryDetailSerializer
	#lookup_field = 'pk'


class IndexesListPerCountry(generics.RetrieveAPIView):    
    #index = StockExchangeIndex.objects.filter(pk=lookup_field)
    #innerqs = index.name
    queryset = StockExchangeIndex.objects.all() #filter(name=innerqs)
    serializer_class = StockExchangeIndexDetailSerializer
    lookup_field = 'pk'
	
    #filter_backends = (filters.DjangoFilterBackend,)
	#filter_fields = ('country',)

class HistData(ListMixingHistData, generics.CreateAPIView):
	queryset = StockExchangeIndex.objects.all()
	serializer_class = HistDataDetailSerializer
	lookup_field = 'pk'
'''
class HistData(ListMixing, generics.ListAPIView):
    queryset = Historical_Data.objects.all()
    serializer_class = HistDataSerializer
    lookup_field = 'index_id'
'''

class ConstituentsList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'index_id'
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('country__name',)    

class ConstituentsDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_fields = ('index_id', 'pk')


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