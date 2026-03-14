from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from koro import BinSlot
from .models import Submission


# Create your views here.
def item(request: HttpRequest, pk: int) -> HttpResponse:
    return render(
        request,
        "stages/index.html",
        {"submission": get_object_or_404(Submission, id=pk)},
    )


def download(request: HttpRequest, pk: int) -> HttpResponse:
    return HttpResponse(
        BinSlot.serialize(get_object_or_404(Submission, id=pk).stage_data),
        content_type="application/octet-stream",
        headers={"Content-Disposition": "attachment"},
    )
