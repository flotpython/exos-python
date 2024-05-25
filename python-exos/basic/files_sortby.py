from pathlib import Path

def init():
    """
    a utility function only for populating the 'pathlib-foo' subfolder
    """
    scale = 10
    logs = Path("pathlib-foo") / "logs"
    logs.mkdir(parents=True, exist_ok = True)
    for i, log, key in ( (1, 0, 'b'), (10, 1, 'a'), (100, 2, 'c')):
        f = logs / f"file{i}"
        with f.open('w') as output:
            content = (10-log) * '*'
            output.write(content + "\n")
        size = f.stat().st_size
        print(f"Wrote file {f} - size {size}")
        d = logs / f"dir{i}"
        d.mkdir(exist_ok = True)
        for j in range(1, 4):
            pad = (6-2*log) * 'x'
            f = d / f"file{j*key}{pad}"
            with f.open('w') as output:
                content = (i*scale+j) * '*'
                output.write(content + "\n")
            size = f.stat().st_size
            print(f"Wrote file {f} - size {size}")

# prune-end-init

def scan_dir(root, *, relative=None, recursive=False):
    # we need a Path instance to start with
    if not isinstance(root, Path):
        root = Path(root)
    # if relative is not provided, we use the current folder
    if relative is None:
        relative = '.'
    # the pattern to use is '**/*' if recursive is True
    glob_pattern = '**/*' if recursive else '*'
    # the most accessible version uses a comprehension
    # however, as we will see, in this case we can use a genexpr instead
    return (f for f in (root/relative).glob(glob_pattern) if f.is_file())


def sort_dir(root: Path, *, relative: str = '.', recursive=False, by='name'):
    """
    sort files under the folder 'root'
    only the subfolder under 'relative' is considered,

    Parameters:
      root: a Path to the main folder
      relative: a str, the relative path to subfolder
      recursive: a boolean that says if a recursive search is needed
      criteria: a str among 'name', 'namelen', or 'size'

    """
    files = scan_dir(root, relative=relative, recursive=recursive)

    match by:
        case 'name':
            sort_function = lambda p: p.name
        case 'namelen':
            sort_function = lambda p: len(p.name)
        case 'size':
            sort_function = lambda p: p.stat().st_size
        case 'mtime':
            sort_function = lambda p: p.stat().st_mtime
        # not too interesting - not advertized
        case 'path':
            sort_function = lambda p: len(str(p.relative_to(root)))
    return sorted(files, key = sort_function)
