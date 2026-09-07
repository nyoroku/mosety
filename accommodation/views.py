from django.views.generic import ListView, DetailView
from .models import PartnerHotel

class HotelListView(ListView):
    model = PartnerHotel
    template_name = 'accommodation/hotel_list.html'
    context_object_name = 'hotels'
    
    def get_queryset(self):
        return PartnerHotel.objects.filter(is_active=True)

class HotelDetailView(DetailView):
    model = PartnerHotel
    template_name = 'accommodation/hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch related images for the gallery
        context['gallery'] = self.object.images.all()
        return context
