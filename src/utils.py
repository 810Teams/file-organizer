"""
    Path formatting utility functions
"""


def path(*path_segment_list: str) -> str:
    """ Returns a formatted path. """
    if len(path_segment_list) == 0:
        return str()

    has_leading_double_slash: bool = (
        path_segment_list[0] is not None
        and (
            path_segment_list[0].startswith('//')
            or path_segment_list[0].startswith('\\\\')
        )
    )

    path_segment_list: list[str] = [
        segment.strip().replace('\\', '/').strip('/')
        for segment in path_segment_list
        if isinstance(segment, str) and segment.strip() != ''
    ]

    joined_path: str = '/'.join(path_segment_list)

    while '//' in joined_path:
        joined_path = joined_path.replace('//', '/')

    return has_leading_double_slash * '//' + joined_path
