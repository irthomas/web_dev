from django.shortcuts import render
from django.http import HttpResponse
# from django.http import request as http
from urllib.parse import urlparse


# Create your views here.
from downloader.models import CHANNELS, LEVELS
from downloader.models import search_db, make_hdf5_filepaths, make_zip_filepath, make_zip_file, delete_zip_file, check_email
from downloader.send_email import send_bira_email
from downloader.config import SECRET_KEYS, MAX_FILES


def get_end_url(request):
    """get last part of url e.g. lno from http://127.0.0.1:8000/lno or http://127.0.0.1:8000/lno/"""
    if type(request) == str:
        url = request
    else:
        url = request.get_full_path()
        
    #trim ending forward slash
    if url[-1] == "/":
        url = url[:-1]
    
    p = urlparse(url)
    end_url = p.path.rsplit("/", 1)[-1]
    return end_url, url.replace(end_url, "")


def channelList(request):
    
    context = {"channels":CHANNELS}
    
    return render(request, 'downloader/index.html', context)
    
    



def levelList(request):

    channel, _ = get_end_url(request)

    context = {"channel":channel, "levels":LEVELS}
    
    return render(request, 'downloader/levels.html', context)




def fileList(request):

    level, url = get_end_url(request)
    channel, _ = get_end_url(url)
    
    download = False
    prepare_zip = False
    delete_zip = False
    
    if request.method == 'POST':
        regex_str = request.POST.get('regex', '.*')

        if "download" in request.POST:
            download = True
        if "prepare_zip" in request.POST:
            prepare_zip = True
            email = request.POST.get('email', '')
        if "delete_zip" in request.POST:
            zip_filename = request.POST.get('zip', '')
            delete_zip = True

    else:
        regex_str = ".*"
    
    #sanitize inputs
    if channel in CHANNELS:
        if level in LEVELS:
            
            filenames = search_db(regex_str, channel, level)

            context = {"channel":channel, "level":level, "filenames":filenames, "regex_str":regex_str, "nfiles":len(filenames)}
            
            if delete_zip:
                delete_zip_file(zip_filename)

                return render(request, 'downloader/delete_zip.html', context)

            elif prepare_zip:
                
                if context["nfiles"] < MAX_FILES:
                    
                    if check_email(email):
                        zip_filename, zip_filepath = make_zip_filepath(email)
                        filepaths, filepaths_str = make_hdf5_filepaths(level, filenames)
                        
                        _ = make_zip_file(zip_filepath, filepaths_str)
                        link_path = "ftp://nomad:%s@ftp-ae.oma.be/tmp/%s" %(SECRET_KEYS["nomad_ftp"], zip_filename)
        
                        context["email"] = email
                        context["link_path"] = link_path
                        context["zip_filename"] = zip_filename
                        # context["terminal_output"] = terminal_output
                        context["terminal_output"] = ""
                        send_bira_email(email, "NOMAD data download is ready", \
"Your download is ready. Please click here to get your file:<a href='%s'>%s</a>\n\n\n \
Please note that direct links to ftps are restricted in modern browsers; \
if so then you need to use an ftp client to retrieve your file:\n \
server=ftp-ae.oma.be\n \
username=nomad\n \
password=%s\n\n \
Your file is the following: /tmp/%s\n\n \
Please remember to click Delete Zip in your web browser once the download is finished!" %(link_path, link_path, SECRET_KEYS["nomad_ftp"], zip_filename))
                        
                        return render(request, 'downloader/prepare_zip.html', context)
                    else:
                        h = "<html><head></head><body>Error: email address is not recognised - please contact Ian to be added to the list</body></html>"
                        return HttpResponse(h)
                else:
                    h = "<html><head></head><body>Error: more than %i files have been selected. Please refine your search</body></html>" %MAX_FILES
                    return HttpResponse(h)
                
            
            elif download:
                return render(request, 'downloader/enter_email.html', context)

            else:
                return render(request, 'downloader/filelist.html', context)


        else:
            h = "<html><head></head><body>Error: level %s not found</body></html>" %level
    else:
        h = "<html><head></head><body>Error: channel %s not found</body></html>" %channel
           
    return HttpResponse(h)


