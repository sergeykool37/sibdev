from django.shortcuts import render
from .forms import CsvModelForm
from .models import Csv
import csv
from django.contrib.auth.models import User
from sales.models import  Deal, Richuser
from datetime import datetime
import pytz


class RichuserView(Richuser):
    model = Richuser
    template_name = 'csvs/response.html'
    context_object_name = 'response'


class User:
    def __init__(self, name, total, items):
        self.name = name
        self.total = total
        self.items = items

    def __str__(self):
        return f'name-{self.name}, total-{self.total}, items-{self.items}'


def upload_file_view(request):

    def line_to_obj(line):
        if line[4] == 'date': return
        customer = line[0]
        item = line[1]
        total = float(line[2])
        quantity = int(line[3])
        date = datetime.strptime(line[4], "%Y-%m-%d %H:%M:%S.%f")
        date = date.replace(tzinfo=pytz.UTC)
        Deal.objects.create(
            customer=customer,
            item=item,
            total=total,
            quantity=quantity,
            date=date
        )
        object_user = {"customer": customer,
                       "item": item,
                       "total": total,
                       "quantity": quantity,
                       "date": date}
        return object_user

    def create_obj_richuser(list_customer):
        for customer in list_customer:
            new_items = []
            for item in customer[1].items:
                count = 0
                for customer1 in list_customer:
                    if item in customer1[1].items:
                        count += 1
                if count >= 2:
                    new_items.append(item)
            customer[1].items = new_items
        Richuser.objects.all().delete()
        for customer in list_customer:
            Richuser.objects.create(
                username=customer[1].name,
                spent_money=customer[1].total,
                gems=', '.join(customer[1].items)
            )
        obj.activated = True
        obj.save()


    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        customers = {}
        with open(obj.file_name.path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                object = line_to_obj(line)
                if object is None: continue
                name = object.get("customer")
                if customers.get(name) is None:
                    total = object.get("total") * object.get("quantity")
                    user = User(name=name, total=total, items=[object.get("item")])
                    customers[name] = user
                else:
                    user = customers.get(name)
                    user.total += object.get("total") * object.get("quantity")
                    item = object.get("item")
                    if item in user.items:
                        pass
                    else:
                        user.items.append(item)
                    customers[name] = user
        list_customer = list(customers.items())
        list_customer.sort(key=lambda i: i[1].total, reverse=True)
        list_customer = list_customer[0:5]
        create_obj_richuser(list_customer)


    return render(request, 'csvs/upload.html', {'form': form})


def response(request):
    richusers = Richuser.objects.all()
    return render(request, "csvs/response.html", context={"richusers": richusers})
