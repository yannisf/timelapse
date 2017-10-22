"""Simple module to try out snippets"""

def keep_num_part(filename):
    """Transforms filename"""
    underscrore_index = filename.index('_')
    dot_index = filename.index('.')
    return filename[underscrore_index+1:dot_index]

transformed = keep_num_part("D7K_2843.JPG")

print(transformed)
