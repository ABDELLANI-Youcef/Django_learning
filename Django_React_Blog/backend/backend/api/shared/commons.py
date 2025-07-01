from rest_framework import mixins, generics

class ListAPIView(mixins.ListModelMixin, generics.GenericAPIView):
  """
  Concrete view for listing a queryset.
  """
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)