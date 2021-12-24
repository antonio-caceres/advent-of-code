"""(2021) Day 13: Transparent Origami"""

import re

from utils import read, plot


def folding_instruction(line):
    """Puzzle line parser for two different instructions -- points and folding lines."""
    if match := re.fullmatch(r"(?P<x>[\d]+),(?P<y>[\d]+)", line):
        return plot.DiscretePoint(*(int(num) for num in match.groups()))
    elif match := re.fullmatch(r"fold along (?P<dim>[xy])=(?P<num>[\d]+)", line):
        match match.group(1), match.group(2):
            case "x", x:
                return plot.DiscreteLine.vertical_line(int(x))
            case "y", y:
                return plot.DiscreteLine.horizontal_line(int(y))
    else:
        return None


def fold_point(pt, fold_dim, fold_val, minimize_fold):
    """Fold a `DiscretePoint` in one dimension while keeping the other dimension constant.

    Folding a point essentially reflects the points across the line at the given value.
    Folding can minimize, maximize, or neither.
    If folding does neither, the fold is always a reflection.
    If folding minimizes or maximizes, the fold will result in either the original point
    or its reflection across the line, whichever is lower or higher, respectively.

    For example, folding the point (1, 3) in the x-dimension with value 2
    would return the point (1, 3) if minimizing, or (3, 3) if maximizing or neither.

    Args:
        pt: Point to fold.
        fold_dim: Character "x" or "y" representing the dimension to fold in.
            The dimension that is not the folding dimension is held constant.
        fold_val: Value to fold with respect to.
        minimize_fold(bool | None): If the folding should prioritize lower values.
             If ``True``, minimizes. If ``False``, maximizes. If ``None``, always reflects.

    Returns:
        `plot.DiscretePoint`: Folded point.
    """
    if (fold_dim := fold_dim.lower()) not in {"x", "y"}:
        raise ValueError(f'Fold dimension must be one of "x" or "y": {fold_dim}')
    const_dim = "y" if fold_dim == "x" else "x"
    folding_coord, const_coord = getattr(pt, fold_dim), getattr(pt, const_dim)

    if minimize_fold is None:
        # reflection: the inequality folding_coord vs. fold_val is always reverse
        # of the inequality folded_coord vs. fold_val, with the same difference
        folded_coord = fold_val - (folding_coord - fold_val)
    else:
        # if minimizing, ensure folded_coord <= fold_val; opposite if maximizing
        sign = -1 if minimize_fold else +1
        folded_coord = fold_val + sign * abs(folding_coord - fold_val)

    return plot.DiscretePoint(**{fold_dim: folded_coord, const_dim: const_coord})


def fold_points(pts, line, minimize_fold):
    """Fold a set of points along a line.

    Perform a reflection of the points across the given line, subject to the constraints
    of `minimize_fold`.
    The exact mechanics of folding are described in `fold_point`.

    Only one of each unique point after the flip is kept.

    Args:
        pts: Points to fold.
        line: Horizontal or vertical `plot.DiscreteLine` to fold with respect to.
        minimize_fold(bool | None): If the folding should prioritize lower values.
             If ``True``, minimizes. If ``False``, maximizes. If ``None``, always reflects.

    Returns:
        Set of points present after the flip has been performed.
    """
    if line.is_vertical():
        fold_attr, fold_val = "x", line.pt.x
    elif line.is_horizontal():
        fold_attr, fold_val = "y", line.pt.y
    else:
        raise ValueError(f"Fold line must be horizontal or vertical: {line}")

    return {fold_point(pt, fold_attr, fold_val, minimize_fold) for pt in pts}


def disp_points(pts):
    """Return a string displaying the points in a rectangular grid using '#' if present and '.' if not present."""
    min_x, max_x = min(pt.x for pt in pts), max(pt.x for pt in pts)
    min_y, max_y = min(pt.y for pt in pts), max(pt.y for pt in pts)

    plot_lines = []
    sorted_pts = plot.sort_points(pts, by_y_coord=True)
    cur_pt_idx = 0

    for y in range(min_y, max_y+1):
        line_chars = []
        for x in range(min_x, max_x+1):
            if cur_pt_idx < len(sorted_pts) and sorted_pts[cur_pt_idx] == (x, y):
                line_chars.append("#")
                cur_pt_idx += 1
            else:
                line_chars.append(".")
        plot_lines.append("".join(line_chars))

    return "\n".join(plot_lines)


if __name__ == "__main__":
    parsed_lines = read.dayta(day=13, line_parser=folding_instruction)
    new_line_idx = parsed_lines.index(None)
    point_set, folds = set(parsed_lines[:new_line_idx]), parsed_lines[new_line_idx+1:]
    for fold_num, fold in enumerate(folds):
        point_set = fold_points(point_set, fold, minimize_fold=True)
        if fold_num == 0:
            print(f"Part One: {len(point_set)}")
    print(f"Part Two:\n{disp_points(point_set)}")
