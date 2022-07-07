from django.urls import path

from sales.views import CorporateSaleListView, CorporateSaleOrganizationListView, CustomersDetailView, FinanceAndCorporateSaleDetailView, FinanceSaleListView, FinanceSaleOrganizationListView, OrganizationsDetailView, RetailCustomersListView, RetailDetailView, RetailListView, RetailPurchaseView, WholesaleCustomersListView, WholesaleDetailView, WholesaleListView, WholesaleView


urlpatterns = [
    path('sales/retail/customers/', RetailCustomersListView.as_view(), name="retail customers"),
    path('sales/wholesale/customers/', WholesaleCustomersListView.as_view(), name="wholesale customers"),
    path('sales/finance-sale/organizations/', FinanceSaleOrganizationListView.as_view(), name="finance sale organizations"),
    path('sales/corporate-sale/organizations/', CorporateSaleOrganizationListView.as_view(), name="corporate sale organizations"),
    
    path('sales/customers/<id>/', CustomersDetailView.as_view(), name="customers"),
    path('sales/organizations/<id>/', OrganizationsDetailView.as_view(), name="organizations"),
    
    path('sales/retail/purchases/', RetailListView.as_view(), name="retail purchases"),
    path('sales/wholesale/purchases/', WholesaleListView.as_view(), name="wholesale purchases"),
    path('sales/finance-sale/purchases/', FinanceSaleListView.as_view(), name="finance sale purchases"),
    path('sales/corporate-sale/purchases/', CorporateSaleListView.as_view(), name="corporate sale purchases"),
    
    path('sales/retail/purchases/<slug>', RetailDetailView.as_view(), name="retail purchases details"),
    path('sales/wholesale/purchases/<slug>', WholesaleDetailView.as_view(), name="wholesale purchases details"),
    path('sales/finance-and-corporate-sale/purchases/<slug>', FinanceAndCorporateSaleDetailView.as_view(), name="finance and corporate sale purchases details"),
    
    path('sales/retail/make-sale/', RetailPurchaseView.as_view(), name="retail"),
    path('sales/wholesale/make-sale/', WholesaleView.as_view(), name="wholesale"),
]
