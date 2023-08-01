import work
work.file_action("Дополнить", "config.txt", line_number=4, content_to_append="New line")

a = work.read_file('config.txt', 2)
print(a)