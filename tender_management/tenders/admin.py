from django.contrib import admin
from django.utils.html import format_html  # Use for HTML rendering in admin
from .models import Department, Tender, Vendor, VendorDocument, ShortfallDocument

# Custom Admin for Tender
class TenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'tender_number', 'department', 'published_date')
    list_filter = ('department',)
    search_fields = ('name', 'tender_number')

# Inline Model for VendorDocument (Allows document uploads in admin)
class VendorDocumentInline(admin.TabularInline):
    model = VendorDocument
    extra = 1  # Allows adding one extra document field
    fields = ('file',)

# Inline Model for Shortfall Documents
class ShortfallDocumentInline(admin.TabularInline):
    model = ShortfallDocument
    extra = 1  # Allow adding multiple documents
    fields = ('shortfall_stage', 'file', 'reason')  # Ensure dropdown is visible
    ordering = ['shortfall_stage']
    autocomplete_fields = ['vendor']  # Allow easy vendor selection

# Custom Admin for Vendor
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tender', 'get_document_links', 'get_shortfall_document_links')
    list_filter = ('tender',)
    search_fields = ('name', 'tender__name')
    inlines = [VendorDocumentInline, ShortfallDocumentInline]  # ✅ Add Shortfall Inline here

    def get_document_links(self, obj):
        documents = obj.documents.all()
        if documents:
            return format_html(
                "<br>".join(
                    f'<a href="{doc.file.url}" target="_blank">📄 Document {idx+1}</a>'
                    for idx, doc in enumerate(documents)
                )
            )
        return "No documents"

    def get_shortfall_document_links(self, obj):
        shortfalls = obj.shortfall_documents.all()
        if shortfalls:
            return format_html(
                "<br>".join(
                    f'<a href="{doc.file.url}" target="_blank">📂 {doc.get_shortfall_stage_display()}</a>'
                    for doc in shortfalls
                )
            )
        return "No shortfall documents"

    get_document_links.short_description = "Submitted Documents"
    get_shortfall_document_links.short_description = "Shortfall Documents"  # ✅ Add short description

# Register Models
admin.site.register(Department)
admin.site.register(Tender, TenderAdmin)
admin.site.register(Vendor, VendorAdmin)
