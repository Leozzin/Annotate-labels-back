from firebase import firebase
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def cleanData(data):
    doc = data['document']
    i = 0
    ann = []
    while True:
        try:
            dd = {}
            dd['start'] = data[f'annotations[{i}][start]']
            dd['end'] = data[f'annotations[{i}][end]']
            dd['label'] = data[f'annotations[{i}][label]']
            dd['text'] = data[f'annotations[{i}][text]']
            ann.append(dd)
            i += 1
        except:
            break
    
    return {
        'document': doc,
        'annotations': ann
    }


@csrf_exempt
def addAnnotation(request):
    firebase_rtdb = firebase.FirebaseApplication("https://annotation-labels-default-rtdb.firebaseio.com/", None)
    # print(request.POST)
    data = dict(request.POST).copy()
    id = datetime.now().strftime("%d%m%Y_%H%M%S")
    data = cleanData(data)
    print(data)
    result = firebase_rtdb.put('data/', name=id, data=data)
    return JsonResponse(list(request.POST), safe=False)
