#!/usr/bin/env python
# coding=utf-8

import inkex
from inkex.elements import Circle, PathElement, Pattern
from math import sin, cos, radians


def draw_circle(cx, cy, r, style, name, parent):

    circ_style = {'stroke': style.c_col,
                  'stroke-width': str(style.c_th), 'fill': style.c_fill}

    # cx, cy = get_cartesian_pt(centre, params)
    circ_attribs = {'cx': str(cx), 'cy': str(cy), 'r': str(r)}
    elem = parent.add(Circle(**circ_attribs))
    elem.style = circ_style
    elem.label = name


def draw_close_path(point_list, parent_g, style_dict):
    inkex.utils.debug(f"there are {len(point_list)} points")
    if len(point_list) < 3:
        inkex.errormsg(
            'less than 3 points have been passed to draw a close path')
    else:
        p_element = parent_g.add(PathElement())
        temp_path = 'M ' + \
            str(point_list[0][0]) + ',' + str(point_list[0][1])
        for i in range(1, len(point_list)):
            temp_path = temp_path + ' L ' + \
                str(point_list[i][0]) + ',' + str(point_list[i][1])
        temp_path = temp_path + ' z'
        p_element.path = temp_path
        p_element.style = style_dict
        # p_element.label = name


class StripePattern(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--angle", type=float, default=0.0, help="angle")
        pars.add_argument("--thickness", type=float,
                          default=0.0, help="thickness")
        pars.add_argument("--space", type=float, default=10.0, help="space")
        pars.add_argument("--name", type=str,
                          default="new stripe pattern", help="pattern name")
        pars.add_argument("--color", type=str,
                          default="#00FF00FF", help="color")

    def effect(self):
        so = self.options
        st = Style(self.svg)
        # create a group and hold it relative to origin
        g = self.svg.get_current_layer().add(inkex.Group.new(so.name))
        g.transform = 'translate(0,0)'
        # theta = so.angle
        # space = so.space
        # thickness =
        angle_rad = radians(so.angle)
        dx_thickness = so.thickness/sin(angle_rad)
        dy_thickness = so.thickness/cos(angle_rad)
        dx_space = so.space/sin(angle_rad)
        dy_space = so.space/cos(angle_rad)
        p1 = (0, 0)
        p2 = (dx_thickness, 0)
        p3 = (dx_thickness + dx_space, 0)
        p4 = (0, dy_space)
        p5 = (dx_thickness + dx_space, dy_space)
        p6 = (0, dy_thickness + dy_space)
        p7 = (dx_thickness, dy_thickness + dy_space)
        p8 = (dx_thickness + dx_space, dy_thickness + dy_space)

        style_dict = {'stroke': '#000000ff',
                      'stroke-width': '0', 'fill': str(so.color)}
        point_list = [p1, p2, p5, p8]
        draw_close_path(point_list, g, style_dict)
        point_list = [p4, p7, p6]
        draw_close_path(point_list, g, style_dict)
        # draw_circle(cx, cy, r, st, 'mycircle', layer)

        # obj = self.svg.selection.first()
        # obj = self.svg.selection.first()
        # inkex.utils.debug(f"selected objects: {obj}")
        bbox = g.bounding_box()
        inkex.utils.debug(f"bbox of the selected objects: {bbox}")
        inkex.utils.debug(f"bbox.left of the selected objects: {bbox.left}")
        inkex.utils.debug(
            f"bbox.bottom of the selected objects: {bbox.bottom}")

        mat = g.composed_transform().matrix
        inkex.utils.debug(f"composed_transform: {g.composed_transform()}")
        inkex.utils.debug(f"matrix: {mat}")
        pattern = self.svg.defs.add(Pattern())
        pattern.set_random_id(so.name)
        # pattern.set('id', 'pattern_name_13')
        pattern.set('width', str(bbox.width))
        pattern.set('height', str(bbox.height))
        pattern.set('patternUnits', 'userSpaceOnUse')
        pattern.patternTransform.add_translate(
            bbox.left - mat[0][2], bbox.top - mat[1][2])
        pattern.append(g)


class Style(object):  # container for style information
    def __init__(self, svg):

        # circles
        self.c_th = svg.unittouu('2px')
        self.c_fill = 'none'
        self.c_col = '#000000'

        # stripe
        self.stroke_width = '0'
        self.stroke_color = '#000000'
        self.fill = '#000000ff'


if __name__ == '__main__':
    StripePattern().run()
