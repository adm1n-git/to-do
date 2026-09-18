from datetime import datetime

def dt2str(dt):
    return dt.strftime(r"%Y-%m-%d %H:%M:%S")

def str2dt(str):
    return datetime.strptime(str, r"%Y-%m-%d %H:%M:%S")
