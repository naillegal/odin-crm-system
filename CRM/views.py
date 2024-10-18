from .models import Customer, SalesContract
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, CustomerProduct, Product, Feature, PriceOffer, PriceOfferProduct, SalesContract
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
# İndex view, loginsiz giriş üçün açıqdır


def index(request):
    return render(request, 'index.html')

# Custom login view, burada remember me funksionallığı əlavə edilib


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        # Səhv olarsa mesaj göstər
        messages.error(
            self.request, "İstifadəçi adı və ya şifrə səhvdir. Zəhmət olmasa yenidən cəhd edin.")
        return super().form_invalid(form)

    def form_valid(self, form):
        # "remember me" checkbox yoxlaması
        remember_me = self.request.POST.get('remember_me', None)

        # Əgər "remember me" işarələnibsə, sessiyanın vaxtını 30 gün et
        if remember_me:
            self.request.session.set_expiry(2592000)  # 30 gün
        else:
            # Brauzer bağlananda sessiya silinsin
            self.request.session.set_expiry(0)

        return super().form_valid(form)

# Task view, yalnız login olan istifadəçilər üçün


@login_required
def task(request):
    today = timezone.now().date()

    # feedback_note-u olan və bugünkü/gələcək tarixdə feedback_date-i olan müştəriləri seçirik
    customers_list = Customer.objects.filter(
        feedback_note__isnull=False,  # feedback_note boş olmayanlar
        feedback_note__gt='',  # Silinmiş qeydləri də istisna edir
    ).filter(
        Q(feedback_date__isnull=True) | Q(feedback_date__gte=today)  # Geri dönüş tarixi uyğun olanlar
    )

    # Sayfalandırma - hər səhifədə 10 müştəri
    paginator = Paginator(customers_list, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # İlk səhifə
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Son səhifə

    # POST istəklərinin idarəsi
    if request.method == 'POST':
        checked_customers = request.POST.getlist('checked_customers')
        Customer.objects.filter(id__in=checked_customers).update(feedback_checked=True)
        return redirect('task')

    return render(request, 'task.html', {'page_obj': page_obj, 'today': today})

@login_required
def addcustomer(request):

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact_number')
        initial_price_offer = request.POST.get('initial_price_offer')
        inquiry_method = request.POST.get('inquiry_method')
        address = request.POST.get('address')
        feedback_date = request.POST.get('feedback_date')

        try:
            # Müştəri yaradırıq
            customer = Customer.objects.create(
                full_name=full_name,
                contact_number=contact_number,
                initial_price_offer=initial_price_offer,
                inquiry_method=inquiry_method,
                address=address,
                feedback_date=feedback_date
            )

            products = request.POST.getlist('products[]')
            sizes = request.POST.getlist('size[]')

            if not products:
                raise ValidationError("Məhsul daxil edilməlidir!")

            for i in range(len(products)):
                product = Product.objects.get(id=products[i])
                size = sizes[i]

                # Müştəri məhsulu yaradırıq
                customer_product = CustomerProduct.objects.create(
                    customer=customer,
                    products=product,
                    size=size
                )

                # Seçilmiş xüsusiyyətləri əlavə edirik
                selected_features = request.POST.getlist(f'features_{i}[]')
                for feature_id in selected_features:
                    feature = Feature.objects.get(id=feature_id)
                    customer_product.features.add(feature)

           
            return redirect('customer')

        except ValidationError as e:
            messages.error(request, f"Formda səhv var: {e}")

    products = Product.objects.all()
    features = Feature.objects.all()

    return render(request, 'addcustomer.html', {
        'products': products,
        'features': features
    })


@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        try:
            # Müştərinin əsas məlumatlarını yeniləyirik
            customer.full_name = request.POST.get('full_name')
            customer.contact_number = request.POST.get('contact_number')
            customer.initial_price_offer = request.POST.get('initial_price_offer')
            customer.inquiry_method = request.POST.get('inquiry_method')
            customer.address = request.POST.get('address')
            customer.feedback_date = request.POST.get('feedback_date')
            customer.save()

            # Mövcud məhsul məlumatlarını silirik və yenidən əlavə edirik
            customer.customerproduct_set.all().delete()

            products = request.POST.getlist('products[]')
            sizes = request.POST.getlist('size[]')

            if not products:
                raise ValidationError("Ən azı bir məhsul daxil edilməlidir.")

            for i in range(len(products)):
                product = Product.objects.get(id=products[i])
                size = sizes[i]

                # Müştəri üçün məhsul əlavə edirik
                customer_product = CustomerProduct.objects.create(
                    customer=customer,
                    products=product,
                    size=size
                )

                # Seçilmiş xüsusiyyətləri əlavə edirik
                selected_features = request.POST.getlist(f'features_{i}[]')
                for feature_id in selected_features:
                    feature = Feature.objects.get(id=feature_id)
                    customer_product.features.add(feature)

            return redirect(reverse('customerinfo', kwargs={'id': customer.id}))

        except Exception as e:
            messages.error(request, f"Xəta baş verdi: {e}")

    products = Product.objects.all()
    features = Feature.objects.all()
    customer_products = customer.customerproduct_set.all()

    return render(request, 'editcustomer.html', {
        'customer': customer,
        'products': products,
        'features': features,
        'customer_products': customer_products,
    })

@login_required
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    try:
        # Müştəriyə aid bütün məlumatları silirik
        customer.delete()
    except Exception as e:
        messages.error(request, f"Xəta baş verdi: {e}")

    # Silindikdən sonra müştəri siyahısına yönləndiririk
    return redirect('customer')

@login_required
def customer(request):
    query = request.GET.get('q', '').strip()  # Axtarış sorğusunu əldə edirik

    # Müştəriləri sorğulamaq
    customers = Customer.objects.all()

    # Əgər axtarış sorğusu varsa, filtr tətbiq edirik
    if query:
        customers = customers.filter(
            Q(full_name__icontains=query) | Q(customer_code__icontains=query)
        )

    customer_data = []
    for customer in customers:
        # Qiymət təklifi və satış sözləşmələrinin olub olmadığını yoxlayırıq
        price_offers = PriceOffer.objects.filter(customer=customer)
        sales_contracts = SalesContract.objects.filter(customer=customer)

        # Müştəri rəngini müəyyən edirik
        if sales_contracts.exists():
            color = "#941c1b"  # Satış sözləşməsi varsa
        elif price_offers.exists():
            color = "#197e16"  # Yalnız qiymət təklifi varsa
        else:
            color = "#1473c7"  # Heç biri yoxdursa

        # Müştəriyə aid məlumatları bir yerə yığırıq
        customer_data.append({
            'customer': customer,
            'price_offers': price_offers,
            'sales_contracts': sales_contracts,
            'color': color,
        })

    return render(request, 'customer.html', {
        'customer_data': customer_data,
    })


@login_required
def adminassistprice(request, customer_id):
    # Müştərini gətiririk
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        try:
            # Form məlumatlarını əldə edirik
            products = request.POST.getlist('product[]')
            prices = request.POST.getlist('price[]')
            quantities = request.POST.getlist('quantity[]')
            sizes = request.POST.getlist('size[]')
            descriptions = request.POST.getlist('description[]')
            design_urls = request.POST.getlist('design_3d_url[]')

            if not products:
                raise ValidationError("Ən azı bir məhsul seçilməlidir!")

            # Müştəri üçün qiymət təklifi yaradırıq
            price_offer = PriceOffer.objects.create(customer=customer)

            # Qiymət təklifi məhsullarını yaradıb saxlamaq
            for i in range(len(products)):
                product = Product.objects.get(id=products[i])
                PriceOfferProduct.objects.create(
                    price_offer=price_offer,
                    products=product,
                    price=prices[i] if prices[i] else None,
                    quantity=quantities[i] if quantities[i] else None,
                    size=sizes[i] if sizes[i] else None,
                    description=descriptions[i] if descriptions[i] else None,
                    design_3d_url=design_urls[i] if design_urls[i] else None,
                )

            return redirect('customerinfo', id=customer.id)

        except ValidationError as e:
            messages.error(request, f"Formda səhv var: {e}")

    # Müştərinin məlumatları ilə formu göstəririk
    products = Product.objects.all()
    return render(request, 'adminassistprice.html', {
        'customer': customer,
        'products': products
    })


@login_required
def adminsalescontract(request, customer_id):
    # Müştəri məlumatlarını gətiririk
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        try:
            # POST request-dən məlumatları alırıq
            system_name = request.POST.get('system')
            glass_thickness = request.POST.get('glass_thickness')
            profile_color = request.POST.get('profile_color')
            sales_price = request.POST.get('sales_price')
            payment_type = request.POST.get('payment_type')
            total_size = request.POST.get('total_size')
            is_single_glass = request.POST.get('is_single_glass') == 'on'
            is_double_glass = request.POST.get('is_double_glass') == 'on'
            is_stainless_colored_glass = request.POST.get(
                'is_stainless_colored_glass') == 'on'

            # Tələb olunan sahələrin yoxlanması
            if not sales_price or not payment_type or not total_size:
                raise ValidationError(
                    "Satış qiyməti, ödəniş növü və toplam m² daxil edilməlidir!")

            # Satış sözləşməsi yaradılır
            SalesContract.objects.create(
                customer=customer,
                system_name=system_name,
                glass_thickness=glass_thickness,
                profile_color=profile_color,
                sales_price=sales_price,
                payment_type=payment_type,
                total_size=total_size,
                is_single_glass=is_single_glass,
                is_double_glass=is_double_glass,
                is_stainless_colored_glass=is_stainless_colored_glass
            )

            return redirect('customerinfo', id=customer.id)

        except ValidationError as e:
            messages.error(request, f"Formda səhv var: {e}")

    # Müştəri məlumatları ilə formu göstəririk
    return render(request, 'adminsalescontract.html', {
        'customer': customer
    })


@login_required
def assistpricedetail(request, offer_id):
    price_offer = get_object_or_404(PriceOffer, id=offer_id)

    price_offer.views_count += 1
    price_offer.save()

    offer_products = PriceOfferProduct.objects.filter(price_offer=price_offer)

    return render(request, 'assistpricedetail.html', {
        'price_offer': price_offer,
        'offer_products': offer_products,
    })


@login_required
def salescontractdetail(request, id):
    try:
        sales_contract = SalesContract.objects.get(id=id)

        sales_contract.views_count += 1
        sales_contract.save()

    except SalesContract.DoesNotExist:
        messages.error(request, "Satış sözləşməsi tapılmadı!")
        return redirect('adminsalescontract')

    return render(request, 'salescontractdetail.html', {
        'sales_contract': sales_contract,
    })


@login_required
def delete_sales_contract(request, id):
    sales_contract = get_object_or_404(SalesContract, id=id)

    if request.method == 'POST':
        # Satış sözləşməsini silirik
        sales_contract.delete()
    else:
        messages.error(request, "Satış sözləşməsi silinə bilmədi.")

    return redirect('salescontract')


@login_required
def edit_sales_contract(request, id):
    sales_contract = get_object_or_404(SalesContract, id=id)

    if request.method == 'POST':
        try:
            # Məlumatları toplamaq
            sales_contract.system_name = request.POST.get('system', '').strip()
            sales_contract.glass_thickness = request.POST.get('glass_thickness', '').strip()
            sales_contract.profile_color = request.POST.get('profile_color', '').strip()
            sales_contract.sales_price = request.POST.get('sales_price', '').strip()
            sales_contract.payment_type = request.POST.get('payment_type')
            sales_contract.total_size = request.POST.get('total_size', '').strip()

            # Checkboxları düzgün idarə etmək
            sales_contract.is_single_glass = bool(request.POST.get('is_single_glass'))
            sales_contract.is_double_glass = bool(request.POST.get('is_double_glass'))
            sales_contract.is_stainless_colored_glass = bool(request.POST.get('is_stainless_colored_glass'))

            # Vacib sahələrin yoxlanması
            if not all([sales_contract.sales_price, sales_contract.payment_type, sales_contract.total_size]):
                raise ValidationError("Satış qiyməti, ödəniş növü və toplam m² daxil edilməlidir!")

            # Dəyişiklikləri yadda saxlamaq
            sales_contract.save()

            return redirect('salescontract')

        except ValidationError as e:
            messages.error(request, f"Formda səhv var: {e}")

        except Exception as e:
            messages.error(request, f"Xəta baş verdi: {str(e)}")

    return render(request, 'editsales.html', {
        'sales_contract': sales_contract,
    })


@login_required
def assistprice(request):
    query = request.GET.get('q', '').strip()  # Axtarış sorğusunu əldə edirik

    # Müştəriləri sorğulamaq
    customers = Customer.objects.prefetch_related('price_offers').all()

    # Axtarış sorğusuna əsasən filtr tətbiq edirik
    if query:
        customers = customers.filter(
            Q(full_name__icontains=query) | Q(customer_code__icontains=query)
        )

    # Hər müştərinin ümumi baxış sayını hesablamaq
    for customer in customers:
        customer.total_views_count = sum(
            [offer.views_count for offer in customer.price_offers.all()]
        )

    return render(request, 'assistprice.html', {
        'customers': customers,
    })


@login_required
def delete_assist_price(request, id):
    price_offer = get_object_or_404(PriceOffer, id=id)

    if request.method == 'POST':
        # Qiymət təklifini silirik
        price_offer.delete()
    else:
        messages.error(request, "Qiymət təklifi silinə bilmədi.")

    return redirect('assistprice')


@login_required
def edit_assist_price(request, id):
    price_offer = get_object_or_404(PriceOffer, id=id)

    if request.method == 'POST':
        try:
            customer_id = request.POST.get('customer')
            customer = Customer.objects.get(id=customer_id)
            price_offer.customer = customer
            price_offer.save()

            # Mövcud məhsulları silirik
            PriceOfferProduct.objects.filter(price_offer=price_offer).delete()

            product_ids = request.POST.getlist('product[]')
            prices = request.POST.getlist('price[]')
            quantities = request.POST.getlist('quantity[]')
            sizes = request.POST.getlist('size[]')
            descriptions = request.POST.getlist('description[]')
            design_urls = request.POST.getlist('design_3d_url[]')

            # Hər məhsulu yenidən əlavə edirik
            for index in range(len(product_ids)):
                product = Product.objects.get(id=product_ids[index])
                PriceOfferProduct.objects.create(
                    price_offer=price_offer,
                    products=product,
                    price=prices[index] if prices[index] else None,
                    quantity=quantities[index] if quantities[index] else None,
                    size=sizes[index] if sizes[index] else None,
                    description=descriptions[index] if descriptions[index] else None,
                    design_3d_url=design_urls[index] if design_urls[index] else None,
                )

            # Müvafiq yönləndirməni düzəldirik
            return redirect('assistprice')

        except Exception as e:
            messages.error(request, f"Xəta baş verdi: {str(e)}")

    price_offer_products = PriceOfferProduct.objects.filter(price_offer=price_offer)

    return render(request, 'editprice.html', {
        'price_offer': price_offer,
        'products': Product.objects.all(),
        'customers': Customer.objects.all(),
        'price_offer_products': price_offer_products,
    })



@login_required
def salescontract(request):
    query = request.GET.get('q', '').strip()  # Axtarış sorğusunu əldə edirik

    # Müştəriləri sorğulamaq
    customers = Customer.objects.prefetch_related('sales_contracts').all()

    # Axtarış sorğusuna əsasən filtr tətbiq edirik
    if query:
        customers = customers.filter(
            Q(full_name__icontains=query) | Q(customer_code__icontains=query)
        )

    # Hər müştərinin ümumi baxış sayını hesablamaq
    for customer in customers:
        customer.total_views_count = sum(
            [contract.views_count for contract in customer.sales_contracts.all()]
        )

    return render(request, 'salescontract.html', {
        'customers': customers,
    })


@login_required
def customerinfo(request, id):
    customer = get_object_or_404(Customer, id=id)
    return render(request, 'customerinfo.html', {'customer': customer})



@login_required
def feedback(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        feedback_note = request.POST.get('note')
        feedback_date = request.POST.get('date')

        try:
            # Qeyd və geri dönüş tarixi yenilənir
            customer.feedback_note = feedback_note
            customer.feedback_date = feedback_date
            customer.save()  # Burada `note_date` avtomatik yenilənir

            return redirect('customerinfo', id=customer.id)

        except Exception as e:
            messages.error(request, f"Xəta baş verdi: {e}")

    return render(request, 'feedback.html', {'customer': customer})