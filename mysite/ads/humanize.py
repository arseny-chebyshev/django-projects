def naturalsize(count):
    fcount = float(count)
    kb = 1024
    mb = kb * kb
    gb = mb * kb
    if fcount < kb:
        return str(count) + 'B'
    if fcount >= kb and fcount < mb:
        return str(int(fcount / (kb/10.0)) / 10.0) + 'KB'
    if fcount >= mb and fcount < gb:
        return str(int(fcount / (mb/10.0)) / 10.0) + 'MB'
    return str(int(fcount / (gb/10.0)) / 10.0) + 'GB'
