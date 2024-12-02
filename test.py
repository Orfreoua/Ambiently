from epub2txt import epub2txt

epub_file_path = 'back/uploads/' + 'hugo_contemplations.epub'
ch_list = epub2txt(epub_file_path, outputlist=True)
print(ch_list[10])
