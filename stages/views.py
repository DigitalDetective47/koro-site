from typing import Final

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from koro import BinSlot

from .models import Submission


def item(request: HttpRequest, pk: int) -> HttpResponse:
    return render(
        request,
        "stages/index.html",
        {"submission": get_object_or_404(Submission, id=pk)},
    )


def download(request: HttpRequest, pk: int) -> HttpResponse:
    target: Final[Submission] = get_object_or_404(Submission, id=pk)
    return HttpResponse(
        BinSlot.serialize(target.stage_data),
        content_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{slugify(target.name)}.bin"'
        },
    )
