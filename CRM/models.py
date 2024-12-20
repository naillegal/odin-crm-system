from django.db import models
from django.utils import timezone
from datetime import timedelta


class Feature(models.Model):
    title = models.CharField(max_length=255, verbose_name="Xüsusiyyətin adı")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Xüsusiyyət"
        verbose_name_plural = "Xüsusiyyətlər"

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Məhsulun adı")
    description = models.TextField(verbose_name="Məhsulun açıqlaması", blank=True, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"

# The through model for the ManyToMany relationship between Customer and Product

class CustomerProduct(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name="Müştəri")
    products = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Məhsul")
    features = models.ManyToManyField('Feature', blank=True, verbose_name="Xüsusiyyətlər")
    size = models.CharField(max_length=100, verbose_name="Məhsulun ölçüsü", blank=True, null=True)  # Ölçü sahəsi

    def __str__(self):
        return f"{self.customer.full_name} - {self.products.title}"

    class Meta:
        verbose_name = "Müştəri Məhsulu"
        verbose_name_plural = "Müştəri Məhsulları"

class Design3D(models.Model):
    title = models.CharField(max_length=255, verbose_name="3D Dizayn Başlıq")
    image = models.ImageField(upload_to='designs/', verbose_name="3D Dizayn şəkil", blank=True, null=True)
    url = models.URLField(max_length=500, verbose_name="3D Dizayn Link", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "3D Dizayn"
        verbose_name_plural = "3D Dizaynlar"
        

class PriceOfferProduct(models.Model):
    price_offer = models.ForeignKey('PriceOffer', on_delete=models.CASCADE, verbose_name="Qiymət Təklifi")
    products = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Məhsul")
    size = models.CharField(max_length=100, verbose_name="Məhsulun ölçüsü", blank=True, null=True)
    price = models.CharField(max_length=30, verbose_name="Məhsulun qiyməti", blank=True, null=True)
    quantity = models.IntegerField(verbose_name="Sayı", blank=True, null=True)
    description = models.TextField(verbose_name="Məhsulun açıqlaması", blank=True, null=True)
    design_3d = models.ForeignKey(
        Design3D, 
        on_delete=models.SET_NULL, 
        verbose_name="3D Dizayn", 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"{self.price_offer.customer.full_name} - {self.products.title}"

    class Meta:
        verbose_name = "Qiymət Təklifi Məhsulu"
        verbose_name_plural = "Qiymət Təklifi Məhsulları"



class Customer(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Adı, Soyadı")
    contact_number = models.CharField(max_length=20, verbose_name="Əlaqə nömrəsi")
    initial_price_offer = models.CharField(max_length=50, verbose_name="İlkin qiymət təklifi", blank=True, null=True)
    products = models.ManyToManyField('Product', through='CustomerProduct', verbose_name="Maraqlandığı məhsullar")
    inquiry_method = models.CharField(max_length=255, verbose_name="Müraciət vasitəsi", blank=True, null=True)
    address = models.TextField(verbose_name="Ünvan", blank=True, null=True)
    feedback_note = models.JSONField(default=list, verbose_name="Qeydlər və tarixlər", blank=True, null=True)
    feedback_date = models.DateField(verbose_name="Geri dönüş tarixi", blank=True, null=True)
    feedback_checked = models.BooleanField(default=False, verbose_name="Geri dönüş yoxlanılması")
    feedback_checked_time = models.DateTimeField(blank=True, null=True, verbose_name="Yoxlanma vaxtı")  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi")
    customer_code = models.CharField(max_length=10, verbose_name="Müştəri Kodu", unique=True, blank=True, null=True)

    def __str__(self):
        return self.full_name
    
    def add_feedback(self, note):
        now = timezone.now().strftime('%Y-%m-%d %H:%M')
        self.feedback_note.append({'note': note, 'date': now})
        self.save()

    class Meta:
        verbose_name = "Müştəri"
        verbose_name_plural = "Müştərilər"
        ordering = ['-created_at']

    def should_be_removed(self):
        """24 saat keçibsə, task.html-dən çıxarılmasını yoxlayır."""
        if self.feedback_checked_time:
            return timezone.now() > self.feedback_checked_time + timedelta(hours=24)
        return False

    def save(self, *args, **kwargs):
        if not self.customer_code:
            last_customer = Customer.objects.all().order_by('id').last()
            if last_customer:
                last_code = int(last_customer.customer_code.strip('#'))
                new_code = f"#{last_code + 1:06d}"
            else:
                new_code = "#000001"
            self.customer_code = new_code

        if self.feedback_note:
            self.note_date = timezone.now()

        super().save(*args, **kwargs)

    
        

class PriceOffer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Müştəri", related_name="price_offers")  # Müştəri ilə əlaqə
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi")  # Yaradılma tarixi (avtomatik doldurulur)
    views_count = models.IntegerField(default=0, verbose_name="Baxış sayı")

    @property
    def total_price(self):
        total = 0
        products = PriceOfferProduct.objects.filter(price_offer=self)
        for product in products:
            try:
                total += int(float(product.price))  
            except (ValueError, TypeError):
                continue
        return total

    def __str__(self):
        return f"Qiymət Təklifi: {self.customer.full_name}"

    class Meta:
        verbose_name = "Qiymət Təklifi"
        verbose_name_plural = "Qiymət Təklifləri"


class SalesContract(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Müştəri", related_name="sales_contracts")  # Müştəri ilə əlaqə
    system_name = models.CharField(max_length=255, verbose_name="Sistem adı", blank=True, null=True)  # Sistem adı
    glass_thickness = models.CharField(max_length=100, verbose_name="Şüşənin qalınlığı", blank=True, null=True)  # Şüşənin qalınlığı
    profile_color = models.CharField(max_length=100, verbose_name="Profil rəngi", blank=True, null=True)  # Profil rəngi
    sales_price = models.CharField(max_length=50, verbose_name="Satış qiyməti")  # Satış qiyməti
    payment_type = models.CharField(max_length=50, choices=[('Nağd', 'Nağd'), ('Taksit', 'Taksit')], verbose_name="Ödəniş növü")   # Ödəniş növü (Nağd və ya Taksit)
    total_size = models.CharField(max_length=100, verbose_name="Toplam m²")  # Toplam m²
    # Checkbox-lar üçün sahələr (seçilə bilən şüşə xüsusiyyətləri)
    is_single_glass = models.BooleanField(default=False, verbose_name="Şüşə 8mm tək qat şüşə olacaqdır.")  # Checkbox 1
    is_double_glass = models.BooleanField(default=False, verbose_name="Şüşə paket şüşə olacaqdır.")  # Checkbox 2
    is_stainless_colored_glass = models.BooleanField(default=False, verbose_name="Şüşə paslanmayan və rəngli olacaqdır.")  # Checkbox 3

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi")  # Yaradılma tarixi
    views_count = models.IntegerField(default=0, verbose_name="Baxış sayı")

    def __str__(self):
        return f"Satış Sözləşməsi: {self.customer.full_name}"

    class Meta:
        verbose_name = "Satış Sözləşməsi"
        verbose_name_plural = "Satış Sözləşmələri"