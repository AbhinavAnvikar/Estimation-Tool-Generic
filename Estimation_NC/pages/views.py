from django.shortcuts import render
from EstimationEngine.EstimateMatrix import Estimate_Engine
from EstimationEngine.CrudeOperation import Users as usr

rows = []
i=0
# Create your views here.

def Home_Page(request):
    return render(request, "home.html", {})

def Logout_Page(request):
    request.session.flush()
    return render(request,"logout.html",{})

def Login_Page(request):
    username = 'none'
    password = ''
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            context = {'username': username}
            return render(request, "Home.html", context)
        else:
            username = request.POST.get('u_name')
            password = request.POST.get('password')
            print(password)
            print(username)
            err_text = usr.checkLogin(username,password)
            #Condition to check if username and password is matching
            if err_text == 'success':
                request.session['username'] = username
                context = {'username': username}
                return render(request, "Home.html", context)
            else:
                context = {'username':'none','err_text':err_text}
                return render(request, "login.html", context)
    else:
        if request.session.has_key('username'):
            username = request.session['username']
            context= {'username':username}
            return render(request, "Home.html", context)
        else:
            context = {'username': 'none', 'err_text': 'none' }
            return render(request, "login.html", context)

def Register_Page(request):
    context={'success':'0','username':'none','u_email':'none'}
    if request.method == 'POST':
        u_name = request.POST.get("u_name")
        password = request.POST.get("password")
        re_pass = request.POST.get("re_pass")
        u_email = request.POST.get("u_email")
        password_mismatch = "Password doesn't match"
        user_already_exists = "Username already exists"
        print(u_name,password,u_email)
        #condition to verify the password and re_pass field
        res,success = usr.passwordValidation(password)
        print(res)
        if success:
            result = usr.registerUser(u_name,password,re_pass,u_email)
            if result =='success':
                print('coming here 1')
                # call method to store the data in table.
                context= {'success':'1', 'username':u_name, 'err_msg':'0'}
                print(context)
            else:
                if str(result).__contains__('Already'):
                    context = {'success': '3', 'username': u_name, 'err_msg': user_already_exists, 'u_email': u_email}
                else:
                    if str(result).__contains__('Re-enter'):
                        context = {'success': '2', 'username': u_name, 'err_msg': password_mismatch, 'u_email': u_email}
                    else:
                        context = {'success':'0','username':'none','err_msg':'-1'}
        else:
            print("Coming here point 4")
            context ={'success':'4','username':u_name,'u_email': u_email,'result':res }
            print(context)
    return render(request, "register.html", context)

def Index_tl_page(request):
    if request.method == 'POST':
        global rows
        global i
        num_tab = request.POST.get('num_tab')
        num_trans = request.POST.get('num_trans')
        num_val = request.POST.get('num_val')
        comp = request.POST.get('complex1')
        is_rec = request.POST.get('is_recon')
        comments =  request.POST.get('comments')
        print(num_tab, num_trans, num_val,comp,is_rec,comments)
        if comp:
            if rows:
                rows.pop(len(rows)-1)
            sum_loe, total_loe = Estimate_Engine.get_loe_ll(comp, num_tab, num_trans, num_val)
            print(sum_loe, total_loe)
            if is_rec is not None:
                sum_loe += (float(num_tab) * 2)
                total_loe += (float(num_tab) * 2)
            rows.append([num_tab,comp, num_trans, num_val, sum_loe, total_loe, comments])
            data = '1'
            tot1, tot2 = Estimate_Engine.total_estimate_ll(rows)
            rows.append(['', '', '', 'Total', tot1, tot2, ''])
        elif not comp:
            if not rows:
                data = '-1'
            else:
                rows.pop(len(rows) - 1)
                data = '1'
                tot1, tot2 = Estimate_Engine.total_estimate_ll(rows)
                rows.append(['', '', '', 'Total', tot1, tot2, ''])
        # print(comments)
        context = {'data': data, 'rows': rows}
    elif request.method=='GET':
        context = {'data': '-1'}
        rows = []
    else:
        context = {'data': '-1'}
    Estimate_Engine.download_to_excel_LL(rows)
    return render(request, "index.html",context)

def Index_d_page(request):
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
            tot1, tot2 = Estimate_Engine.total_estimate(rows)
            rows.append(['', '', 'Total', tot1, tot2, ''])
        elif (not complex1 or not complex2):
            if not rows :
                data = '-1'
            else:
                rows.pop(len(rows) - 1)
                data = 1
                tot1, tot2 = Estimate_Engine.total_estimate(rows)
                rows.append(['', '', 'Total', tot1, tot2, ''])
        # Last row for the Total LOE's
        #print(comments)

        context={'data':data, 'rows':rows}

    elif request.method =='GET':
        context = {'data': '-1'}
        rows=[]
        i=0
    else:
        context = {'data':'-1'}

    Estimate_Engine.download_to_excel(rows)
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