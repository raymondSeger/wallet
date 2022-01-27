import datetime
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from test_wallet_app.models import User, Wallet, Transaction_Data

def index(request):
    return HttpResponse("Please go to http://127.0.0.1:8000/start-test-data to setup the initialization data")

def start_test_data(request):

    if User.objects.all().filter(the_id="ea0212d3-abd6-406f-8c67-868e814a2436").first() == None:
        # create Main User
        user = User(the_id="ea0212d3-abd6-406f-8c67-868e814a2436", auth_token="cb04f9f26632ad602f14acef21c58f58f6fe5fb55a", name="test name", email="raymondseger@live.com", hashed_password="123123")
        user.save()

        # create main wallet
        wallet = Wallet(the_id="6ef31ed3-f396-4b6c-8049-674ddede1b16", wallet_name="", enabled_status=False)
        wallet.save()
        user.user_wallet.add(wallet)

    return HttpResponse("Please use the links on the documentation to test the app, use the same token. https://documenter.getpostman.com/view/8411283/SVfMSqA3")

@require_http_methods(["POST"])
@csrf_exempt
def api_v1_init(request):
    customer_xid = request.POST.get('customer_xid', '')

    if customer_xid == "":
        return JsonResponse({
            "status": "fail"
        })

    the_user = User.objects.all().filter(the_id=customer_xid).first()

    if the_user == None:
        return JsonResponse({
            "status": "fail"
        })

    return JsonResponse({
        "data": {
            "token": the_user.auth_token
        },
        "status": "success"
    })

@require_http_methods(["POST"])
@csrf_exempt
def api_v1_wallet_deposits(request):
    authorization_data  = request.META.get('HTTP_AUTHORIZATION')
    the_token           = authorization_data[len("Token "):]
    amount              = request.POST.get('amount', '')
    reference_id        = request.POST.get('reference_id', '')

    if amount == "" or reference_id == "":
        return JsonResponse({
            "status": "fail"
        })

    the_user = User.objects.all().filter(auth_token=the_token).first()
    if the_user == None:
        return JsonResponse({
            "status": "fail"
        })

    # no Transaction with this reference ID
    if Transaction_Data.objects.all().filter(reference_id=reference_id).count() > 0:
        return JsonResponse({
            "status": "fail",
            "why"   : "reference id with this number already exist"
        })

    the_wallet      = the_user.user_wallet.all().first()
    current_time    = datetime.datetime.now()

    # must be able to handle decimal number
    new_transaction_data = Transaction_Data(reference_id=reference_id, transaction_data=the_wallet, amount=amount, deposited_by=the_user.the_id, deposited_at=current_time)
    new_transaction_data.save()

    total_amount        = Transaction_Data.objects.all().filter(transaction_data=the_wallet).aggregate(Sum('amount'))
    total_amount_number = total_amount["amount__sum"]

    return JsonResponse({
      "status"  : "success",
      "data"    : {
        "deposit"   : {
            "id"                : new_transaction_data.id,
            "reference_id"      : new_transaction_data.reference_id,
            "deposited_by"      : new_transaction_data.deposited_by,
            "status"            : "success",
            "deposited_at"      : new_transaction_data.deposited_at,
            "amount"            : total_amount_number
        }
      }
    })

@require_http_methods(["POST"])
@csrf_exempt
def api_v1_wallet_withdrawals(request):
    authorization_data  = request.META.get('HTTP_AUTHORIZATION')
    the_token           = authorization_data[len("Token "):]
    amount              = request.POST.get('amount', '')
    reference_id        = request.POST.get('reference_id', '')

    if amount == "" or reference_id == "":
        return JsonResponse({
            "status": "fail"
        })

    the_user = User.objects.all().filter(auth_token=the_token).first()
    if the_user == None:
        return JsonResponse({
            "status": "fail"
        })

    # no Transaction with this reference ID
    if Transaction_Data.objects.all().filter(reference_id=reference_id).count() > 0:
        return JsonResponse({
            "status": "fail",
            "why"   : "reference id with this number already exist"
        })

    the_wallet      = the_user.user_wallet.all().first()
    current_time    = datetime.datetime.now()

    amount = -float(amount)

    # must be able to handle decimal number
    new_transaction_data = Transaction_Data(reference_id=reference_id, transaction_data=the_wallet, amount=amount, withdrawn_by=the_user.the_id, withdrawn_at=current_time)
    new_transaction_data.save()

    total_amount        = Transaction_Data.objects.all().filter(transaction_data=the_wallet).aggregate(Sum('amount'))
    total_amount_number = total_amount["amount__sum"]

    return JsonResponse({
        "status": "success",
        "data": {
            "withdrawal": {
                "id"            : new_transaction_data.id,
                "reference_id"  : new_transaction_data.reference_id,
                "withdrawn_by"  : new_transaction_data.withdrawn_by,
                "status"        : "success",
                "withdrawn_at"  : new_transaction_data.withdrawn_at,
                "amount"        : total_amount_number
            }
        }
    })

@require_http_methods(["PATCH", "GET", "POST"])
@csrf_exempt
def api_v1_wallet(request):
    if request.method == 'POST':
        authorization_data  = request.META.get('HTTP_AUTHORIZATION')
        the_token           = authorization_data[len("Token "):]

        the_user            = User.objects.all().filter(auth_token=the_token).first()
        if the_user == None:
            return JsonResponse({
                "status": "fail"
            })

        the_wallet                  = the_user.user_wallet.all().first()
        the_wallet.enabled_status   = True
        the_wallet.enabled_at       = datetime.datetime.now()
        the_wallet.save()

        total_amount        = Transaction_Data.objects.all().filter(transaction_data=the_wallet).aggregate(Sum('amount'))
        total_amount_number = total_amount["amount__sum"]

        if total_amount_number == None:
            total_amount_number = 0

        return JsonResponse({
            "status"    : "success",
            "data"      : {
                "wallet"    : {
                  "id"          : the_wallet.the_id,
                  "owned_by"    : the_user.the_id,
                  "status"      : "enabled" if the_wallet.enabled_status else "disabled",
                  "enabled_at"  : the_wallet.enabled_at,
                  "balance"     : total_amount_number
                }
            }
        })

    elif request.method == 'GET':
        # GET
        authorization_data  = request.META.get('HTTP_AUTHORIZATION')
        the_token           = authorization_data[len("Token "):]

        the_user            = User.objects.all().filter(auth_token=the_token).first()
        if the_user == None:
            return JsonResponse({
                "status": "fail"
            })

        the_wallet          = the_user.user_wallet.all().first()
        total_amount        = Transaction_Data.objects.all().filter(transaction_data=the_wallet).aggregate(Sum('amount'))
        total_amount_number = total_amount["amount__sum"]

        if total_amount_number == None:
            total_amount_number = 0

        return JsonResponse({
            "status"    : "success",
            "data"      : {
                "wallet"    : {
                    "id"        : the_wallet.the_id,
                    "owned_by"  : the_user.the_id,
                    "status"    : "enabled" if the_wallet.enabled_status else "disabled",
                    "enabled_at": the_wallet.enabled_at,
                    "balance"   : total_amount_number
                }
            }
        })
    elif request.method == "PATCH":
        # PATCH
        authorization_data  = request.META.get('HTTP_AUTHORIZATION')
        the_token           = authorization_data[len("Token "):]
        is_disabled         = request.body.decode('utf-8')

        if is_disabled == "is_disabled=true":
            the_user = User.objects.all().filter(auth_token=the_token).first()

            if the_user == None:
                return JsonResponse({
                    "status": "fail"
                })

            the_wallet                  = the_user.user_wallet.all().first()
            the_wallet.enabled_status   = False
            the_wallet.disabled_at      = datetime.datetime.now()
            the_wallet.save()

            total_amount        = Transaction_Data.objects.all().filter(transaction_data=the_wallet).aggregate(Sum('amount'))
            total_amount_number = total_amount["amount__sum"]

            if total_amount_number == None:
                total_amount_number = 0

            return JsonResponse({
                "status": "success",
                "data": {
                    "wallet": {
                        "id"            : the_wallet.the_id,
                        "owned_by"      : the_user.the_id,
                        "status"        : "enabled" if the_wallet.enabled_status else "disabled",
                        "enabled_at"    : the_wallet.enabled_at,
                        "balance"       : total_amount_number
                    }
                }
            })
        else:
            return JsonResponse({
                "status": "fail"
            })