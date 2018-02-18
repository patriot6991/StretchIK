import maya.cmds as mc


class StretchIK(object):
    def __init__(self, s=''):
        self.num = 5
        self.name = s
        self.tn = ''
        self.sn = ''

    def create(self, *args):
        # field get
        temp_joint.num = int(
            mc.intField('jntNum', q=True, value=True))
        temp_joint.name = str(
            mc.textField('tempJntName', q=True, text=True))
        stretch_joint.name = str(
            mc.textField('stretchJntName', q=True, text=True))

        # curve rebuild
        name_list = mc.ls(sl=True)
        curve.name = name_list[0]

        # shape node name edit
        mc.rename(curve.name, 'tempCurveName')
        mc.rename('tempCurveName', curve.name)
        mc.rebuildCurve(kr=0)
        mc.select(d=True)

        # short name
        s.tn = '%s_%s' % (curve.name, temp_joint.name)
        s.sn = '%s_%s' % (curve.name, stretch_joint.name)

        # crate temp temp_joint
        for i in range(temp_joint.num):
            mc.joint(p=(0, 0, 0), n='%s%s' % (s.tn, str(i + 1)))
            mc.select(d=True)
            p = 'pointOnCurveInfo'
            mc.createNode('%s' % p, n='%s_%s%s' % (p, s.tn, str(i + 1)))
            node_name = '%s_%s%s' % (p, s.tn, str(i + 1))
            mc.connectAttr(
                '%sShape.local' % curve.name,
                '%s.inputCurve' % node_name)
            mc.setAttr(
                '%s.parameter' % node_name,
                (float(1) / (temp_joint.num - 1)) * i)
            mc.connectAttr(
                '%s.position' % node_name,
                '%s%s.translate' % (s.tn, str(i + 1)))
        for i in range(temp_joint.num):
            mc.select('%s%s' % (s.tn, str(i + 1)), add=True)
        mc.group(n='%s_grp' % s.tn)
        mc.setAttr('.visibility', 0)
        mc.select(d=True)

        # aim constraint
        for i in range(temp_joint.num - 1):
            first = '%s%s' % (s.tn, str(i + 1))
            second = '%s%s' % (s.tn, str(i + 2))
            mc.aimConstraint(second, first)

        # create stretch joint
        for i in range(temp_joint.num):
            mc.joint(p=(0, 0, 0), n='%s%s' % (s.sn, str(i + 1)))
        for i in range(temp_joint.num):
            first = '%s%s' % (s.tn, str(i + 1))
            second = '%s%s' % (s.sn, str(i + 1))
            mc.parentConstraint(first, second)
        mc.select(d=True)

    def ui(self):
        win = mc.window(title='stretch IK', widthHeight=(250, 145))
        form = mc.formLayout()

        jnt = mc.text(
            l='jointNum', w=110, h=20)
        jnf = mc.intField(
            'jntNum', w=115, h=20, value=temp_joint.num)
        tnt = mc.text(
            l='tempJointName', w=115, h=20)
        tnf = mc.textField(
            'tempJntName', w=115, h=20, text=temp_joint.name)
        snt = mc.text(
            l='stretchJointName', w=110, h=20)
        snf = mc.textField(
            'stretchJntName', w=115, h=20, text=stretch_joint.name)
        but = mc.button(
            l='create StretchIK', w=230, h=50, c=self.create)
        mc.formLayout(form, edit=True, attachForm=[
            (jnt, 'top', 10), (jnt, 'left', 10),
            (jnf, 'top', 10), (jnf, 'left', 125),
            (tnt, 'top', 35), (tnt, 'left', 10),
            (tnf, 'top', 35), (tnf, 'left', 125),
            (snt, 'top', 60), (snt, 'left', 10),
            (snf, 'top', 60), (snf, 'left', 125),
            (but, 'top', 85), (but, 'left', 10)
        ])

        mc.showWindow(win)


temp_joint = StretchIK(s='temp')
stretch_joint = StretchIK(s='stretch')
curve = StretchIK()
s = StretchIK()
s.ui()
