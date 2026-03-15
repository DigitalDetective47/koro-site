from typing import Final, Optional

from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from koro import BinSlot, XmlSlot

from .forms import SubmissionForm
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


@login_required
def new(request: HttpRequest) -> HttpResponse:
    form: SubmissionForm
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file: Final[Optional[UploadedFile]] = form.files.get("stage_data")
            if file is not None:
                untyped_content: Final[str | bytes] = file.read()
                content: Final[bytes] = (
                    untyped_content.encode("shift_jis", "xmlcharrefreplace")
                    if isinstance(untyped_content, str)
                    else bytes(untyped_content)
                )
                Submission(
                    name=form.cleaned_data["name"],
                    stage_data=(XmlSlot if content[0] else BinSlot).deserialize(
                        content
                    ),
                    creator=request.user,
                    embed=form.cleaned_data["embed"],
                    description=form.cleaned_data["description"],
                    music=form.cleaned_data["music"],
                ).save()
                return HttpResponseRedirect("/stage/1")
    else:
        form = SubmissionForm()
    return render(request, "stages/new.html", {"form": form})
