import sys
import re
import glob
import os


def simplify_path(paths):
    simplified = [re.sub(r'/+', '/', s) for s in paths]
    simplified = [re.sub(r'/[^/]+/../', '/', s) for s in simplified]
    return simplified

def remove_duplicates_keep_last(strings):
    seen = set()
    unique_list = []
    for item in reversed(strings):
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return list(reversed(unique_list))


def parse_file(filename):
    tokens_l = []
    tokens_L = []
    tokens_quotes_a = []
    tokens_quotes_dll = []

    with open(filename, 'r') as file:
        content = file.read()
        tokens = content.split()

        for token in tokens:
            if token.startswith('-l'):
                tokens_l.append(token)
            elif token.startswith('-L'):
                tokens_L.append(token)
            elif re.match(r'^".*\dll.a"$', token):
                tokens_quotes_dll.append(token)
            elif re.match(r'^".*\.a"$', token):
                tokens_quotes_a.append(token)

    # Remove duplicate /
    tokens_L          = simplify_path(tokens_L)
    tokens_quotes_dll = simplify_path(tokens_quotes_dll)
    tokens_quotes_a   = simplify_path(tokens_quotes_a)

    # Remove duplicates
    tokens_l          = remove_duplicates_keep_last(tokens_l)
    tokens_L          = remove_duplicates_keep_last(tokens_L)
    tokens_quotes_a   = remove_duplicates_keep_last(tokens_quotes_a)
    tokens_quotes_dll = remove_duplicates_keep_last(tokens_quotes_dll)

    return tokens_l, tokens_L, tokens_quotes_a, tokens_quotes_dll

def search_lib_dir(lib_list, prefix_sigrok):
    sigrok_libs = []
    other_libs  = []
    for lib in lib_list:
        lib_name = lib[2:]
        lig_sigrok = f"{prefix_sigrok}/lib/lib{lib_name}.a"
        if glob.glob(lig_sigrok):
            sigrok_libs.append(lib)
        else:
            other_libs.append(lib)
            
    return sigrok_libs, other_libs

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <prefix>")
        sys.exit(1)

    filename = sys.argv[1]
    prefix   = sys.argv[2]

    tokens_l, tokens_L, explicit_libs, explicit_dll = parse_file(filename)
    sigrok_libs, other_libs = search_lib_dir(tokens_l, prefix)

    # Try to optimize library order
    # This heuristics may not work at all times (in case of cross-dependencies)
    # Can be solved by duplicating the set of cross-dependant libs
    # At this time none has been detected so duplicates are commented
    with open(filename, 'w') as file:
        file.write("\n".join(tokens_L)+"\n")
        file.write("\n".join(sigrok_libs)+"\n")
        # file.write("\n".join(sigrok_libs)+"\n")
        file.write("\n".join(explicit_libs)+"\n")
        # file.write("\n".join(explicit_libs)+"\n")
        file.write("\n".join(explicit_dll)+"\n")
        file.write("\n".join(other_libs)+"\n")


    print("Rewriten library list (workaround CMake link issue):", filename)
