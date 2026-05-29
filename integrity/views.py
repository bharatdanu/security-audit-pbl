from django.shortcuts import render
from django.contrib import messages
from .models import FileRecord
import hashlib


def generate_hash(uploaded_file):
    sha256 = hashlib.sha256()
    for chunk in uploaded_file.chunks():
        sha256.update(chunk)
    return sha256.hexdigest()


def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        hash_val = generate_hash(file)

        record = FileRecord.objects.create(
            file=file,
            hash_value=hash_val
        )

        messages.success(request, 'File uploaded and hash generated successfully.')
        return render(request, 'integrity/upload.html', {
            'record': record,
        })

    return render(request, 'integrity/upload.html')


def verify_file(request):
    context = {}
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        new_hash = generate_hash(file)

        last_record = FileRecord.objects.last()
        context['new_hash'] = new_hash
        context['last_record'] = last_record

        if last_record is None:
            messages.error(request, 'No original file found to compare. Please upload first.')
        else:
            if new_hash == last_record.hash_value:
                messages.success(request, 'File is NOT tampered ✅')
                context['result'] = 'not_tampered'
            else:
                messages.error(request, 'File is TAMPERED ❌')
                context['result'] = 'tampered'

    return render(request, 'integrity/verify.html', context)


def hash_history(request):
    records = FileRecord.objects.order_by('-uploaded_at')
    return render(request, 'integrity/history.html', {'records': records})
