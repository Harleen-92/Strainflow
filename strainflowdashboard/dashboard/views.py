from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView

# Create your views here.
from . import LinePlot
import logging

#logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "dashboard/index.html"


class PlotView(TemplateView):
    template_name = "dashboard/index2.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotView, self).get_context_data(**kwargs)
        context['plot'] = LinePlot.line_plot_1()
        return context