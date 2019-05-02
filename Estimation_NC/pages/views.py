from django.shortcuts import render
from EstimationEngine.EstimateMatrix import Estimate_Engine

rows = []
i=0
# Create your views here.

def Home_Page(request):
    return render(request, "home.html", {})

def Index_tl_page(request):
    if request.method == 'POST':
        num_tab = request.POST.get('num_tab')
        num_trans = request.POST.get('num_trans')
        num_val = request.POST.get('num_val')
        comp = request.POST.get('complex1')
        is_rec = request.POST.get('is_recon')
        comments =  request.POST.get('comments')
        print(num_tab, num_trans, num_val,comp,is_rec,comments)
    context = {'data':'-1'}
    return render(request, "index.html",context)

def Index_d_page(request):
    context = {'data':'-1'}
    return render(request, "index_d.html",context)

def Index_dev_Page(request):
    if request.method =='POST':
        #print(complex1, complex2)
        global rows
        global i

        #get the input complexities
        req = request.POST.get('req_name')
        complex1 = request.POST.get('complex1')
        complex2 = request.POST.get('complex2')
        comments = request.POST.get('comments_txt')
        #print(complex1, complex2)
        print(req)
        # Confition if no selection
        if (complex1 and complex2):
            i+=1

            # First Run. No need to delete the total
            if rows:
                rows.pop(len(rows)-1)
            tech_loe,final_tech_loe = Estimate_Engine.get_loe(complex1,complex2)
            if not req:
                rows.append([i,complex1, complex2, tech_loe, final_tech_loe,comments])
            else:
                rows.append([req, complex1, complex2, tech_loe, final_tech_loe, comments])
            data = 1
        elif (not complex1 or not complex2):
            if not rows :
                data = '-1'
            else:
                rows.pop(len(rows) - 1)
                data = 1
        # Last row for the Total LOE's
        tot1,tot2 = Estimate_Engine.total_estimate(rows)
        rows.append(['','','Total',tot1,tot2,''])
        #print(comments)

        context={'data':data, 'rows':rows}

    elif request.method =='GET':
        context = {'data': '-1'}
        rows=[]
        i=0
    else:
        context = {'data':'-1'}

    Estimate_Engine.download_to_excel(rows)

    return render(request,"index_dev.html",context)