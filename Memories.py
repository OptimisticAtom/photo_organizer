import os, shutil, time

cwd = os.getcwd()
new_mem_dir = "/New_Memories/"
old_mem_dir = "/Old_Memories/"
print(cwd)


def parse_date(date):
    split_date = date.split(',')
    # print(split_date)
    return split_date

def create_date_dict(path):
    dates = dict()
    for root, dirs, files in os.walk(path):
        # print(files)
        # day_count = 0
        for file in files:
            if os.path.exists(path + file):
                file_time = time.localtime(os.path.getmtime(path + file))
                date_key = "{},{},{}".format(file_time.tm_mon, file_time.tm_mday, file_time.tm_year)
                if dates.get(date_key) == None:
                    data = [file]
                    dates[date_key] = data

                else:
                    # number = dates[date_key].get("number")
                    dates[date_key].append(file)
                    # files.append(file)
                    # number += 1
                    # dates[date_key].update({"number": number})
    return dates

def new_date_dirs(dates, path):
    for date in dates:
        tm_mdy = parse_date(date)
        y_path = path + tm_mdy[2]
        if os.path.isdir(y_path):
            y_path += '/'
            dates2 = create_date_dict(y_path)
            if dates2.get(date) != None:
                if len(dates[date]) + len(dates2[date]) > 9:
                    print("creating date dir {} and merging new and old dates for it".format(date))
                    dates[date] += dates2[date]
                    make_dir = y_path + date
                    if os.path.isdir(make_dir):
                        print("date dir already exists. just appending")
                    else:
                        os.mkdir(make_dir)
                else:
                    print("not enough {} for new directory".format(date))

            else:
                print("no old file with {} exists".format(date))


def move_files(dates, src):
    for date in dates:
        files = dates[date]
        tm_mdy = parse_date(date)
        directory = cwd + old_mem_dir + tm_mdy[2]
        if os.path.isdir(directory):
            print("putting {} in {}".format(date, directory))
        else:
            print("create year: " + tm_mdy[2])
            os.mkdir(directory)
        directory += '/'
        date_dir = directory + date
        if os.path.isdir(date_dir):
            dest = date_dir + '/'
            print("dest: " + dest)
        elif len(files) > 9:
            # date_dir.append(date)
            print("create dir " + date)
            os.mkdir(date_dir)
            dest = date_dir + '/'
        else:
            dest = directory
            print("putting {} in {}".format(date, tm_mdy[2]))
        for file in files:
            if os.path.exists(src + file) and not os.path.exists(dest + file):
                shutil.move(src + file, dest)
            elif os.path.exists(directory + file) and not os.path.exists(dest + file):
                shutil.move(directory + file, dest)
            else:
                print(file + " is in an unexpected location or already exists")

src = cwd + new_mem_dir
dates = create_date_dict(src)
new_date_dirs(dates, cwd + old_mem_dir)
move_files(dates, src)
