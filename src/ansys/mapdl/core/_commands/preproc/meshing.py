# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Optional, Union

from ansys.mapdl.core.mapdl_types import MapdlFloat, MapdlInt


class Meshing:
    def accat(self, na1="", na2="", **kwargs):
        """Concatenates multiple areas in preparation for mapped meshing.

        APDL Command: ACCAT

        Parameters
        ----------
        na1, na2
            Areas to be concatenated.  If NA1 = ALL, NA2 will be ignored and
            all selected areas [ASEL] will be concatenated.  If NA1 = P,
            graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NA1 (NA2 is ignored).

        Notes
        -----
        Concatenates multiple, adjacent areas (the input areas) into one area
        (the output area) in preparation for mapped meshing.  A volume that
        contains too many areas for mapped meshing can still be mapped meshed
        if some of the areas in that volume are first concatenated (see Meshing
        Your Solid Model in the Modeling and Meshing Guide for details on
        mapped meshing restrictions).

        Because of modeling restrictions that result from its use, ACCAT is
        meant to be used solely for meshing.  Specifically, (a) the output area
        and any volumes that have the output area on their area list [VLIST]
        cannot be used as input to any other solid modeling operation (not even
        another ACCAT command); and (b) the output area cannot accept solid
        model boundary conditions [DA, SFA].

        The output area (or volumes which contain it) will be meshed [AMESH,
        VMESH] by meshing the input areas, which themselves must be meshable.
        The output area from the ACCAT operation will be coincident with the
        input areas and the input areas will be retained.  Consider the AADD
        command instead of ACCAT if you wish to delete the input areas.  When
        an ACCAT command is issued, volume area lists [VLIST] that contain all
        of the input areas will be updated so that the volume area lists refer
        to the output area instead of the input area.  Deletion of the output
        area [ADELE] effectively reverses the ACCAT operation and restores
        volume area lists to their original condition.  ACCAT operations on
        pairs of adjacent four-sided areas automatically concatenate
        appropriate lines [LCCAT]; in all other situations, line concatenations
        must be addressed by the user.

        You can use the ASEL command to select areas that were created by
        concatenation, and then follow it with an ADELE,ALL command to delete
        them.  See Meshing Your Solid Model in the Modeling and Meshing Guide
        for a discussion on how to easily select and delete concatenated areas
        in one step.
        """
        command = f"ACCAT,{na1},{na2}"
        return self.run(command, **kwargs)

    def aclear(self, na1="", na2="", ninc="", **kwargs):
        """Deletes nodes and area elements associated with selected areas.

        APDL Command: ACLEAR

        Parameters
        ----------
        na1, na2, ninc
            Delete mesh for areas NA1 to NA2 (defaults to NA1) in steps of NINC
            (defaults to 1).  If NA1 = ALL, NA2 and NINC are ignored and the
            mesh for all selected areas [ASEL] is deleted.  If NA1 = P,
            graphical picking is enabled and all remaining arguments are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NA1 (NA2 and NINC are ignored).

        Notes
        -----
        Deletes all nodes and area elements associated with selected areas
        (regardless of whether the nodes or elements are selected).  Nodes
        shared by adjacent meshed areas and nodes associated with non-area
        elements will not be deleted.  Attributes assigned as a result of AATT
        are maintained.  In the program's response to the command, if an area,
        line, or keypoint is tallied as "cleared," it means either its node or
        element reference was deleted.

        This command is also valid for rezoning. When issued during rezoning
        (after the REMESH,START command and before the REMESH,FINISH command),
        ACLEAR clears only the area generated by the AREMESH command.
        """
        command = f"ACLEAR,{na1},{na2},{ninc}"
        return self.run(command, **kwargs)

    def aesize(self, anum="", size="", **kwargs):
        """Specifies the element size to be meshed onto areas.

        APDL Command: AESIZE

        Parameters
        ----------
        anum
            Area number of the area to which this element size specification
            applies. If ANUM = ALL, size applies to all selected areas. If ANUM
            = P, graphical picking is enabled. A component name may also be
            substituted for ANUM.

        size
             Desired element size.

        Notes
        -----
        AESIZE allows control over the element sizing inside any area or on the
        face(s) of a volume.

        SIZE controls element size on the interior of the area. For any line on
        the area not having its own size assignment and not controlled by
        keypoint size assignments, it specifies the element size along the line
        as well, so long as no adjacent area has a smaller size, which would
        take precedence. If the AESIZE governs the boundary and SmartSizing is
        on, the boundary size can be refined for curvature or proximity.

        This command is also valid for rezoning.
        """
        command = f"AESIZE,{anum},{size}"
        return self.run(command, **kwargs)

    def amap(self, area="", kp1="", kp2="", kp3="", kp4="", **kwargs):
        """Generates a 2-D mapped mesh based on specified area corners.

        APDL Command: AMAP

        Parameters
        ----------
        area
            Area number of area to be meshed.  If AREA = P, graphical picking
            is enabled and all remaining arguments are ignored (valid only in
            the GUI).

        kp1, kp2, kp3, kp4
            Keypoints defining corners of the mapped mesh.  Three or four
            corners may be specified, and may be input in any order.

        Notes
        -----
        Only one area at a time can be meshed with this command.  The program
        internally concatenates all lines between the specified keypoints, then
        meshes the area with all quadrilateral elements.  If line divisions are
        set, the mesh will follow the rules for mapped meshing (see Meshing
        Your Solid Model in the Modeling and Meshing Guide).

        If the area being meshed has concatenated lines, the program will ask
        if those concatenations should be removed (in batch, the concatenations
        will automatically be removed).  Nodes required for the generated
        elements are created and assigned the lowest available node numbers.
        If a mapped mesh is not possible due to mismatched line divisions or
        poor element shapes, the meshing operation is aborted.
        """
        command = f"AMAP,{area},{kp1},{kp2},{kp3},{kp4}"
        return self.run(command, **kwargs)

    def amesh(self, na1="", na2="", ninc="", **kwargs):
        """Generates nodes and area elements within areas.

        APDL Command: AMESH

        Parameters
        ----------
        na1, na2, ninc
            Mesh areas from NA1 to NA2 (defaults to NA1) in steps of NINC
            (defaults to 1).  If NA1 = ALL, NA2 and NINC are ignored and all
            selected areas [ASEL] are meshed.  If NA1 = P, graphical picking is
            enabled and all remaining arguments are ignored (valid only in the
            GUI).  A component name may also be substituted for NA1 (NA2 and
            NINC are ignored).

        Notes
        -----
        Any undefined nodes required for the generated elements are created and
        assigned the lowest available numbers.

        This command is also valid for rezoning.
        """
        command = f"AMESH,{na1},{na2},{ninc}"
        return self.run(command, **kwargs)

    def arefine(
        self,
        na1="",
        na2="",
        ninc="",
        level="",
        depth="",
        post="",
        retain="",
        **kwargs,
    ):
        """Refines the mesh around specified areas.

        APDL Command: AREFINE

        Parameters
        ----------
        na1, na2, ninc
            Areas (NA1 to NA2 in increments of NINC) around which the mesh is
            to be refined.  NA2 defaults to NA1, and NINC defaults to 1.  If
            NA1 = ALL, NA2 and NINC are ignored and all selected areas are used
            for refinement.  If NA1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NA1 (NA2 and NINC are
            ignored).

        level
            Amount of refinement to be done.  Specify the value of LEVEL as an
            integer from 1 to 5, where a value of 1 provides minimal
            refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth
            Depth of mesh refinement in terms of the number of elements outward
            from the indicated areas (defaults to 1).

        post
            Type of postprocessing to be done after element splitting, in order
            to improve element quality:

            OFF - No postprocessing will be done.

            SMOOTH - Smoothing will be done.  Node locations may change.

            CLEAN - Smoothing and cleanup will be done.  Existing elements may be deleted, and node
                    locations may change (default).

        retain
            Flag indicating whether quadrilateral elements must be retained in
            the refinement of an all-quadrilateral mesh.  (The ANSYS program
            ignores the RETAIN argument when you are refining anything other
            than a quadrilateral mesh.)

            ON - The final mesh will be composed entirely of quadrilateral elements, regardless
                 of the element quality (default).

            OFF - The final mesh may include some triangular elements in order to maintain
                  element quality and provide transitioning.

        Notes
        -----
        AREFINE performs local mesh refinement around the specified areas.  By
        default, the indicated elements are split to create new elements with
        1/2 the edge length of the original elements (LEVEL = 1).

        AREFINE refines all area elements and tetrahedral volume elements that
        are adjacent to the specified areas.  Any volume elements that are
        adjacent to the specified areas, but are not tetrahedra (for example,
        hexahedra, wedges, and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains initial
        conditions at nodes [IC], coupled nodes [CP family of commands],
        constraint equations [CE family of commands], or boundary conditions or
        loads applied directly to any of its nodes or elements.  This applies
        to nodes and elements anywhere in the model, not just in the region
        where you want to request mesh refinement.  See Revising Your Model in
        the Modeling and Meshing Guide for additional restrictions on mesh
        refinement.

        This command is also valid for rezoning.
        """
        command = f"AREFINE,{na1},{na2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)

    def chkmsh(self, comp="", **kwargs):
        """Checks area and volume entities for previous meshes.

        APDL Command: CHKMSH

        Parameters
        ----------
        comp
            Name of component containing areas or volumes.

        Notes
        -----
        CHKMSH invokes a predefined ANSYS macro that checks areas and volumes
        to find out if they were previously meshed.  This macro name will
        appear in the log file (Jobname.LOG) prior to area and volume meshing
        operations initiated through the GUI.  This command is not intended to
        be typed in directly in an ANSYS session (although it can be included
        in an input file for use with the /INPUT command).
        """
        command = f"CHKMSH,{comp}"
        return self.run(command, **kwargs)

    def clrmshln(self, **kwargs):
        """Clears meshed entities.

        APDL Command: CLRMSHLN

        Notes
        -----
        When you use the GUI method to set the number of elements on specified
        lines, and any of those lines is connected to one or more meshed lines,
        areas, or volumes, ANSYS gives you the option to clear the meshed
        entities.  (This occurs only when you perform this operation via the
        GUI; ANSYS does not provide such an option when you use the command
        method [LESIZE].)

        If you activate the mesh clearing option, the program invokes an ANSYS
        macro, CLRMSHLN, that clears the meshed entities.  This macro name will
        appear in the log file (Jobname.LOG).  This macro is for the ANSYS
        program's internal use only.  This command is not intended to be typed
        in directly in an ANSYS session, although it can be included in an
        input file for batch input or for use with the /INPUT command.
        """
        command = f"CLRMSHLN,"
        return self.run(command, **kwargs)

    def cpcyc(
        self,
        lab="",
        toler="",
        kcn="",
        dx="",
        dy="",
        dz="",
        knonrot="",
        **kwargs,
    ):
        """Couples the two side faces of a cyclically symmetric model
        for loading that are the same on every segment.

        APDL Command: CPCYC

        Parameters
        ----------
        lab
            Degree of freedom label for coupled nodes (in the nodal coordinate
            system). If ALL, use all appropriate labels.  Valid labels are:
            Structural labels:  UX, UY, or UZ (displacements); ROTX, ROTY, or
            ROTZ (rotations, in radians).

        toler
            Tolerance for coincidence (based on maximum coordinate difference
            in each global Cartesian direction for node locations and on angle
            differences for node orientations).  Defaults to 0.0001. Only nodes
            within the tolerance are considered to be coincident for coupling.

        kcn
            In coordinate system KCN, node 1 of CP + dx dy dz = node 2 of CP.

        dx, dy, dz
            Node location increments in the active coordinate system (DR, Dθ,
            DZ for cylindrical, DR, D θ, DΦ for spherical or toroidal).

        knonrot
            When KNONROT = 0, the nodes on coupled sets are rotated into
            coordinate system KCN (see NROTAT command description). When
            KNONROT = 1, the nodes are not rotated, and you should make sure
            that coupled nodal DOF directions are correct.

        Notes
        -----
        Cyclic coupling requires identical node and element patterns on the
        low and high sector boundaries. The MSHCOPY operation allows convenient
        generation of identical node and element patterns. See Using CPCYC and
        MSHCOPY Commands in the Modeling and Meshing Guide for more
        information.

        Although developed primarily for use with cyclically symmetric models,
        your use of the CPCYC command is not limited to cyclic symmetry
        analyses.
        """
        command = f"CPCYC,{lab},{toler},{kcn},{dx},{dy},{dz},{knonrot}"
        return self.run(command, **kwargs)

    def czdel(self, grp1="", grp2="", grp3="", **kwargs):
        """Edits or clears cohesive zone sections.

        APDL Command: CZDEL

        Parameters
        ----------
        grp1
            Initial group of cohesive zone elements to be deleted.

        grp2
            Final group of cohesive zone elements to be deleted.

        grp3
            Increment for selected groups.

        Notes
        -----
        The CZDEL command edits or deletes the interface elements and nodes,
        along with the associated changes made to the underlying plane or solid
        elements created during a previous CZMESH operation.

        Each CZMESH operation will create groups of elements and nodes with
        component names in the format CZME_EL01 (elements) and CZME_ND01
        (nodes). The final number of this format will be the number used for
        grp1 and grp2. If grp1 = ALL, all nodes and elements created by the
        CZMESH command will be deleted. After using CZDEL, all the user-defined
        components will be unselected.

        The CZDEL command is valid for structural analyses only.
        """
        command = f"CZDEL,{grp1},{grp2},{grp3}"
        return self.run(command, **kwargs)

    def czmesh(
        self,
        ecomps1="",
        ecomps2="",
        kcn="",
        kdir="",
        value="",
        cztol="",
        **kwargs,
    ):
        """Create and mesh an interface area composed of cohesive zone elements.

        APDL Command: CZMESH

        Parameters
        ----------
        ecomps1
            Component name or number for the group of plane or solid structural
            elements adjacent to the interface being meshed.

        ecomps2
            Component name or number for the opposing (from ecomps1) group of
            plane or solid structural elements adjacent to the interface being
            meshed.

        kcn
            Coordinate system number for the separation surface and normal
            direction. (if ecomps1 and ecomps2 not specified)

        kdir
            Direction (x, y, or z) normal to separation surface in the KCN
            coordinate system (if ecomps1 and ecomps2 not specified).

        value
            Coordinate value along the KDIR axis at which to locate the
            interface (if ecomps1 and ecomps2 not specified).

        cztol
            Optional absolute tolerance about VALUE (if ecomps1 and ecomps2 not
            specified). Allows nodes occurring slightly above or below the
            separation to be grouped properly. The following expression
            represents the default value:

        Notes
        -----
        CZMESH is used on a mesh with shared nodes at the interface.

        If ecomps1 and ecomps2 are specified, the CZMESH command creates/meshes
        interface elements (INTER202, INTER203, INTER204, INTER205) along the
        boundary between the two components or groups of elements.

        The elements in each of the components or groups of elements will share
        nodes with each other and also with the interface elements. This one-
        element thick boundary of interface elements will split the body
        between the two components or groups of elements.

        Subsequent separation (delamination and failure) of the interface zone
        will result in an increasing displacement between the nodes (within the
        interface element) along the cohesive zone elements. Unless otherwise
        specified, the CZMESH command analyzes the configuration and geometry
        of the adjacent structural elements and provides the appropriate
        interface element.

        The CZMESH operation copies any nodal temperatures you have defined on
        the split surface of the original mesh from the original nodes to the
        newly created coincident duplicate nodes. However, displacements,
        forces, and other boundary conditions are not copied.

        The CZMESH command is valid for structural analyses only.
        """
        command = f"CZMESH,{ecomps1},{ecomps2},{kcn},{kdir},{value},{cztol}"
        return self.run(command, **kwargs)

    def desize(
        self,
        minl="",
        minh="",
        mxel="",
        angl="",
        angh="",
        edgmn="",
        edgmx="",
        adjf="",
        adjm="",
        **kwargs,
    ):
        """Controls default element sizes.

        APDL Command: DESIZE

        Parameters
        ----------
        minl
            Minimum number of elements that will be attached to a line when
            using lower-order elements (defaults to 3 elements per line).  If
            MINL = DEFA, all arguments will be set back to default values.  If
            MINL = STAT, list status of command (Including on/off status).  If
            MINL = OFF, deactivate default element sizing.  If MINL = ON,
            reactivate default element sizing.

        minh
            Minimum number of elements that will be attached to a line when
            using higher-order elements. Defaults to 2 elements per line.

        mxel
            Maximum number of elements that will be attached to a single line
            (lower or higher-order elements). Defaults to 15 elements per line
            for h-elements. To deactivate this limit, specify a large number
            (such as 9999).

        angl
            Maximum spanned angle per lower-order element for curved lines.
            Defaults to 15 degrees per element.

        angh
            Maximum spanned angle per higher-order element for curved lines.
            Defaults to 28 degrees per element.

        edgmn
            Minimum element edge length. Defaults to no minimum edge length.
            The MINL or MINH argument can override this value.

        edgmx
            Maximum element edge length. Defaults to no maximum edge length.
            The MXEL argument can override this value.

        adjf
            Target aspect ratio for adjacent line.  Used only when free
            meshing. Defaults to 1.0, which attempts to create equal-sided
            h-elements.

        adjm
            Target aspect ratio for adjacent line.  Used only when map meshing.
            Defaults to 4.0, which attempts to create rectangular h-elements.

        Notes
        -----
        DESIZE settings are usually used for mapped meshing.  They are also
        used for free meshing if SmartSizing is turned off [SMRTSIZE,OFF],
        which is the default.  Even when SmartSizing is on, some DESIZE
        settings (such as maximum and minimum element edge length) can affect
        free mesh density. The default settings of the DESIZE command  are used
        only when no other element size specifications [KESIZE, LESIZE, ESIZE]
        exist for a certain line.

        This command is also valid for rezoning.
        """
        command = (
            f"DESIZE,{minl},{minh},{mxel},{angl},{angh},{edgmn},{edgmx},{adjf},{adjm}"
        )
        return self.run(command, **kwargs)

    def eorient(
        self,
        etype: str = "",
        dir_: Union[str, int] = "",
        toler: MapdlFloat = "",
        **kwargs,
    ) -> Optional[str]:
        """Reorients solid element normals.

        APDL Command: EORIENT

        Parameters
        ----------
        etype
            Specifies which elements to orient.

            LYSL - Specifies that certain solid elements (such as
                   SOLID185 with KEYOPT(3) = 1,
                   SOLID186 with KEYOPT(3) = 1, and SOLSH190) will be
                   oriented. This value is the default.

        dir_
            The axis and direction for orientation, or an element
            number. If Dir is set to a positive number (n),
            then all eligible elements are oriented as similarly as
            possible to element n.

            NEGX - The element face with the outward normal most
                   nearly parallel to the element coordinate system’s
                   negative x-axis is designated (reoriented) as face 1.

            POSX - The element face with the outward normal most
                   nearly parallel to the element coordinate system’s
                   positive x-axis is designated (reoriented) as face 1.

            NEGY - The element face with the outward normal most
                   nearly parallel to the element coordinate system’s
                   negative y-axis is designated (reoriented) as face
                   1. .

            POSY - The element face with the outward normal most
                   nearly parallel to the element coordinate system’s
                   positive y-axis is designated (reoriented) as face 1.

            NEGZ - (Default) The element face with the outward normal
                   most nearly parallel to the element coordinate
                   system’s negative z-axis is designated (reoriented)
                   as face 1.

            POSZ - The element face with the outward normal most
                   nearly parallel to the element coordinate system’s
                   positive z-axis is designated (reoriented) as face 1.

        toler
            The maximum angle (in degrees) between the outward normal
            face and the target axis. Default is 90.0.
            Lower toler values will reduce the number of faces that
            are considered as the basis of element reorientation.

        Notes
        -----
        EORIENT renumbers the element faces, designating the face  most
        parallel to the XY plane of the element coordinate system (set
        with ESYS) as face 1 (nodes I-J-K-L, parallel to the layers
        in layered elements). It calculates the outward normal of
        each face and changes the node designation  of the elements
        so the face with a normal most nearly parallel with and in
        the same general direction as the target axis becomes face 1.

        The target axis, defined by Dir, is either the negative or
        positive indicated axis or the outward normal of face 1 of
        that element.

        All SOLID185 Layered Structural Solid, SOLID186 Layered
        Structural Solid, and SOLSH190 solid shell elements in the
        selected set are considered for reorientation.

        After reorienting elements, you should always display and
        graphically review results using the /ESHAPE command. When
        plotting models with many or symmetric layers, it may be
        useful to temporarily reduce the number of layers to two,
        with one layer being much thicker than the other.

        You cannot use EORIENT to change the normal direction of any
        element that has a body or surface load.  We recommend that
        you apply all of your loads only after ensuring that the
        element normal directions are acceptable.

        Prisms and tetrahedrals are also supported, within the current
        limitations of the SOLID185, SOLID186, and SOLSH190 elements.
        (Layers parallel to the four-node face of the prism are not
        supported.)
        """
        command = f"EORIENT,{etype},{dir_},{toler}"
        return self.run(command, **kwargs)

    def erefine(
        self,
        ne1: Union[str, int] = "",
        ne2: MapdlInt = "",
        ninc: MapdlInt = "",
        level: MapdlInt = "",
        depth: MapdlInt = "",
        post: str = "",
        retain: str = "",
        **kwargs,
    ) -> Optional[str]:
        """Refines the mesh around specified elements.

        APDL Command: EREFINE

        Parameters
        ----------
        ne1, ne2, ninc
            Elements (NE1 to NE2 in increments of NINC) around which
            the mesh is to be refined. NE2 defaults to NE1, and NINC
            defaults to 1. If NE1 = ALL, NE2 and NINC are ignored and
            all selected elements are used for refinement. A component
            name may also be substituted for NE1 (NE2 and NINC are
            ignored).

        level
            Amount of refinement to be done. Specify the value of
            LEVEL as an integer from 1 to 5, where a value of 1
            provides minimal refinement, and a value of 5 provides
            maximum refinement (defaults to 1).

        depth
            Depth of mesh refinement in terms of number of elements
            outward from the indicated elements, NE1 to NE2
            (defaults to 0).

        post
            Type of postprocessing to be done after element
            splitting, in order to improve element quality:

            OFF - No postprocessing will be done.

            SMOOTH - Smoothing will be done. Node locations may change.

            CLEAN - Smoothing and cleanup will be done. Existing
                    elements may be deleted, and node
                    locations may change (default).

        retain
            Flag indicating whether quadrilateral elements must be
            retained in the refinement of an all-quadrilateral mesh.
            (The ANSYS program ignores the RETAIN argument when you
            are refining anything other than a quadrilateral mesh.)

            ON - The final mesh will be composed entirely of
                 quadrilateral elements, regardless
                 of the element quality (default).

            OFF - The final mesh may include some triangular elements
                  in order to maintain
                  element quality and provide transitioning.

        Notes
        -----
        EREFINE performs local mesh refinement around the specified
        elements. By default, the surrounding elements are split to
        create new elements with 1/2 the edge length of the original
        elements (LEVEL = 1).

        EREFINE refines all area elements and tetrahedral volume
        elements that are adjacent to the specified elements. Any
        volume elements that are adjacent to the specified elements,
        but are not tetrahedra (for example, hexahedra, wedges,
        and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains
        initial conditions at nodes [IC], coupled nodes
        [CP family of commands], constraint equations [CE family of
        commands], or boundary conditions or loads applied directly
        to any of its nodes or elements. This applies to nodes and
        elements anywhere in the model, not just in the
        region where you want to request mesh refinement. If you have
        detached the mesh from the solid model, you must disable
        postprocessing cleanup or smoothing (POST = OFF) after the
        refinement to preserve the element attributes.

        For additional restrictions on mesh refinement, see Revising
        Your Model in the Modeling and Meshing Guide.

        This command is also valid for rezoning.
        """
        command = f"EREFINE,{ne1},{ne2},{ninc}," f"{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)

    def esize(self, size="", ndiv="", **kwargs):
        """Specifies the default number of line divisions.

        APDL Command: ESIZE

        Parameters
        ----------
        size
            Default element edge length on surface boundaries (i.e., lines).
            Divisions are automatically calculated (rounded upward to next
            integer) from line lengths.  If SIZE is zero (or blank), use NDIV.

        ndiv
            Default number of element divisions along region boundary lines.
            Not used if SIZE is input.

        Notes
        -----
        Specifies the default number of line divisions (elements) to be
        generated along the region boundary lines. The number of divisions may
        be defined directly or automatically calculated. Divisions defined
        directly for any line [LESIZE, KESIZE, etc.] are retained. For adjacent
        regions, the divisions assigned to the common line for one region are
        also used for the adjacent region. See the MOPT command for additional
        meshing options.

        For free meshing operations, if smart element sizing is being used
        [SMRTSIZE] and ESIZE,SIZE has been specified, SIZE will be used as a
        starting element size, but will be overridden (i.e., a smaller size may
        be used) to accommodate curvature and small features.

        This command is also valid for rezoning.
        """
        command = f"ESIZE,{size},{ndiv}"
        return self.run(command, **kwargs)

    def esys(self, kcn: MapdlInt = "", **kwargs) -> Optional[str]:
        """Sets the element coordinate system attribute pointer.

        APDL Command: ESYS

        Parameters
        ----------
        kcn
            Coordinate system number:

            0 - Use element coordinate system orientation as defined
                (either by default or by KEYOPT setting) for the
                element (default).

            N - Use element coordinate system orientation based on
                local coordinate system N (where N must be greater
                than 10). For global system 0, 1, or 2, define a
                local system N parallel to appropriate system with
                the LOCAL or CS command (for example: LOCAL,11,1).

        Notes
        -----
        Identifies the local coordinate system to be used to define
        the element coordinate system of subsequently defined
        elements. Used only with area and volume elements. For
        non-layered volume elements, the local coordinate system N is
        simply assigned to be the element coordinate system. For
        shell and layered volume elements, the x and y axes of the
        local coordinate system N are projected onto the shell or
        layer plane to determine the element coordinate system. See
        Understanding the Element Coordinate System for more details.
        N refers to the coordinate system reference number (KCN)
        defined using the LOCAL (or similar) command. Element
        coordinate system numbers may be displayed [/PNUM].
        """
        command = f"ESYS,{kcn}"
        return self.run(command, **kwargs)

    def fvmesh(self, keep="", **kwargs):
        """Generates nodes and tetrahedral volume elements from detached exterior

        APDL Command: FVMESH
        area elements (facets).

        Parameters
        ----------
        keep
            Specifies whether to keep the area elements after the tetrahedral
            meshing operation is complete.

            0 - Delete area elements (default).

            1 - Keep area elements.

        Notes
        -----
        The FVMESH command generates a tetrahedral volume mesh from a selected
        set of detached exterior area elements (facets).  (Detached elements
        have no solid model associativity.)  The area elements can be
        triangular-shaped, quadrilateral-shaped, or a mixture of the two.

        The FVMESH command is in contrast to the VMESH command, which requires
        a volume to be input.

        The main tetrahedra mesher [MOPT,VMESH,MAIN] is the only tetrahedra
        mesher that supports the FVMESH command.  The alternate tetrahedra
        mesher [MOPT,VMESH,ALTERNATE] does not support FVMESH. MESH200 elements
        do not support FVMESH.

        Tetrahedral mesh expansion [MOPT,TETEXPND,Value] is supported for both
        the FVMESH and VMESH commands.  Tet-mesh expansion is the only mesh
        control supported by FVMESH.

        Triangle- or quadrilateral-shaped elements may be used as input to the
        FVMESH command. Where quadrilaterals are used, the default behavior is
        for the pyramid-shaped elements to be formed at the boundary when the
        appropriate element type is specified. See the MOPT,PYRA command for
        details.

        The FVMESH command does not support multiple "volumes."  If you have
        multiple volumes in your model, select the surface elements for one
        "volume," while making sure that the surface elements for the other
        volumes are deselected.  Then use FVMESH to generate a mesh for the
        first volume.  Continue this procedure by selecting one volume at a
        time and meshing it, until all of the volumes in the model have been
        meshed.

        If an error occurs during the meshing operation, the area elements are
        kept even if KEEP = 0.
        """
        command = f"FVMESH,{keep}"
        return self.run(command, **kwargs)

    def gsgdata(self, lfiber="", xref="", yref="", rotx0="", roty0="", **kwargs):
        """Specifies the reference point and defines the geometry in the fiber

        APDL Command: GSGDATA
        direction for the generalized plane strain element option.

        Parameters
        ----------
        lfiber
            Fiber length from the reference point. Defaults to 1.

        xref
            X coordinate of the reference point. Defaults to zero.

        yref
            Y coordinate of the reference point. Defaults to zero.

        rotx0
            Rotation of the ending plane about X in radians Defaults to zero.

        roty0
            Rotation of the ending plane about Y in radians Defaults to zero.

        Notes
        -----
        The ending point is automatically determined from the starting
        (reference) point and the geometry inputs. All inputs are in the global
        Cartesian coordinate system. For more information about the generalized
        plane strain feature, see Generalized Plane Strain Option of Current-
        Technology Solid Elements in the  Element Reference.
        """
        command = f"GSGDATA,{lfiber},{xref},{yref},{rotx0},{roty0}"
        return self.run(command, **kwargs)

    def imesh(
        self,
        laky="",
        nsla="",
        ntla="",
        kcn="",
        dx="",
        dy="",
        dz="",
        tol="",
        **kwargs,
    ):
        """Generates nodes and interface elements along lines or areas.

        APDL Command: IMESH

        Parameters
        ----------
        laky
            Copies mesh according to the following:

            LINE or 1 - Copies line mesh (default).

            AREA or 2 - Copies area mesh.

        nsla
            Number that identifies the source line or area. This is the line or
            area whose mesh will provide the pattern for the interface
            elements. ANSYS copies the pattern of the line or area elements
            through the area or volume to create the mesh of area or volume
            interface elements.

        ntla
            Number that identifies the target line or area. This is the line or
            area that is opposite the source line or area specified by NSLA.
            Add NTLA to obtain the copied mesh from the source line or area.

        kcn
            Number that identifies the particular ANSYS coordinate system.

        dx, dy, dz
            Incremental translation of node coordinates in the active
            coordinate system (DR, Dθ, DZ for cylindrical, and DR, Dθ, DΦ for
            spherical or toroidal). The source line or area coordinates + DX,
            DY, DZ = the target line or area coordinates. If left blank, ANSYS
            automatically estimates the incremental translation.

        tol
            Tolerance for verifying topology and geometry. By default, ANSYS
            automatically calculates the tolerance based on associated
            geometries.

        Notes
        -----
        Generates nodes and interface elements along lines or areas. The IMESH
        command requires that the target line or area exactly match the source
        line or area. Also, both target and source lines or areas must be in
        the same area or volume. The area or volume containing the source line
        or area must be meshed before executing IMESH, while the area or volume
        containing the target line or area must be meshed after executing
        IMESH.

        For three dimensional problems where LAKY = AREA, ANSYS fills the
        interface layer according to the following table:
        """
        command = f"IMESH,{laky},{nsla},{ntla},{kcn},{dx},{dy},{dz},{tol}"
        return self.run(command, **kwargs)

    def katt(self, mat="", real="", type_="", esys="", **kwargs):
        """Associates attributes with the selected, unmeshed keypoints.

        APDL Command: KATT

        Parameters
        ----------
        mat, real, type\\_, esys
            Material number, real constant set number, type number, and
            coordinate system number to be associated with selected, unmeshed
            keypoints.

        Notes
        -----
        Keypoints subsequently generated from the keypoints will also have
        these attributes.  These element attributes will be used when the
        keypoints are meshed.  If a keypoint does not have attributes
        associated with it (by this command) at the time it is meshed, the
        attributes are obtained from the then current MAT, REAL,TYPE, and ESYS
        command settings.  Reissue the KATT command (before keypoints are
        meshed) to change the attributes.  A zero (or blank) argument removes
        the corresponding association.

        If any of the arguments MAT, REAL, TYPE, or ESYS are defined as -1,
        then that value will be left unchanged in the selected set.

        In some cases, ANSYS can proceed with a keypoint meshing operation even
        when no logical element type has been assigned via KATT,,,TYPE or TYPE.
        For more information, see the discussion on setting element attributes
        in Meshing Your Solid Model in the Modeling and Meshing Guide.
        """
        command = f"KATT,{mat},{real},{type_},{esys}"
        return self.run(command, **kwargs)

    def kclear(self, np1="", np2="", ninc="", **kwargs):
        """Deletes nodes and point elements associated with selected keypoints.

        APDL Command: KCLEAR

        Parameters
        ----------
        np1, np2, ninc
            Delete mesh for keypoints NP1 to NP2 (defaults to NP1) in steps of
            NINC (defaults to 1).  If NP1 = ALL, NP2 and NINC are ignored and
            the mesh for all selected keypoints [KSEL] is deleted.  If NP1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NP1.

        Notes
        -----
        Deletes all nodes and point elements associated with selected keypoints
        (regardless of whether the nodes or elements are selected).  Nodes
        associated with non-point elements will not be deleted.  Attributes
        assigned as a result of KATT are maintained.  In the program's response
        to the command, if a keypoint is tallied as "cleared," it means either
        its node or element reference was deleted.
        """
        command = f"KCLEAR,{np1},{np2},{ninc}"
        return self.run(command, **kwargs)

    def kesize(self, npt="", size="", fact1="", fact2="", **kwargs):
        """Specifies the edge lengths of the elements nearest a keypoint.

        APDL Command: KESIZE

        Parameters
        ----------
        npt
            Number of the keypoint whose lines will be adjusted.  If ALL, use
            all selected keypoints [KSEL].  If NPT = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).

        size
            Size of elements along lines nearest keypoint NPT (overrides any
            other specified size).  If SIZE is zero (or blank), use FACT1 or
            FACT2.

        fact1
            Scale factor applied to a previously defined SIZE.  Not used if
            SIZE is input.

        fact2
            Scale factor applied to the minimum element division at keypoint
            NPT for any attached line.  This feature is useful with adaptive
            mesh refinement.  Not used if SIZE or FACT1 is input.

        Notes
        -----
        Affects only the line divisions adjacent to the keypoint on lines not
        previously assigned divisions by other line commands [LESIZE, etc.].
        The remaining line divisions are determined from the division nearest
        the keypoint at the other end of the line (specified by another KESIZE
        command or the ESIZE command).  Divisions are transferred to the lines
        during the mesh operation.  If smart element sizing is being used
        [SMRTSIZE], KESIZE specifications may be overridden (i.e., a smaller
        element size may be used) to accommodate curvature and small features.

        This command is valid in any processor. The command is also valid for
        rezoning.
        """
        command = f"KESIZE,{npt},{size},{fact1},{fact2}"
        return self.run(command, **kwargs)

    def kmesh(self, np1="", np2="", ninc="", **kwargs):
        """Generates nodes and point elements at keypoints.

        APDL Command: KMESH

        Parameters
        ----------
        np1, np2, ninc
            Mesh keypoints from NP1 to NP2 (defaults to NP1) in steps of NINC
            (defaults to 1).  If NP1 = ALL, NP2 and NINC are ignored and all
            selected keypoints [KSEL] are meshed.  If NP1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NP1.

        Notes
        -----
        Missing nodes required for the generated elements are created and
        assigned the lowest available numbers.
        """
        command = f"KMESH,{np1},{np2},{ninc}"
        return self.run(command, **kwargs)

    def krefine(
        self,
        np1="",
        np2="",
        ninc="",
        level="",
        depth="",
        post="",
        retain="",
        **kwargs,
    ):
        """Refines the mesh around specified keypoints.

        APDL Command: KREFINE

        Parameters
        ----------
        np1, np2, ninc
            Keypoints (NP1 to NP2 in increments of NINC) around which the mesh
            is to be refined.  NP2 defaults to NP1, and NINC defaults to 1.  If
            NP1 = ALL, NP2 and NINC are ignored and all selected keypoints are
            used for refinement.  If NP1 = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI).
            A component name may also be substituted for NP1 (NP2 and NINC are
            ignored).

        level
            Amount of refinement to be done.  Specify the value of LEVEL as an
            integer from 1 to 5, where a value of 1 provides minimal
            refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth
            Depth of mesh refinement in terms of the number of elements outward
            from the indicated keypoints (defaults to 1).

        post
            Type of postprocessing to be done after element splitting, in order
            to improve element quality:

            OFF - No postprocessing will be done.

            SMOOTH - Smoothing will be done.  Node locations may change.

            CLEAN - Smoothing and cleanup will be done.  Existing elements may be deleted, and node
                    locations may change (default).

        retain
            Flag indicating whether quadrilateral elements must be retained in
            the refinement of an all-quadrilateral mesh.  (The ANSYS program
            ignores the RETAIN argument when you are refining anything other
            than a quadrilateral mesh.)

            ON - The final mesh will be composed entirely of quadrilateral elements, regardless
                 of the element quality (default).

            OFF - The final mesh may include some triangular elements in order to maintain
                  element quality and provide transitioning.

        Notes
        -----
        KREFINE performs local mesh refinement around the specified keypoints.
        By default, the indicated elements are split to create new elements
        with 1/2 the edge length of the original elements (LEVEL = 1).

        KREFINE refines all area elements and tetrahedral volume elements that
        are adjacent to the specified keypoints.  Any volume elements that are
        adjacent to the specified keypoints, but are not tetrahedra (for
        example, hexahedra, wedges, and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains initial
        conditions at nodes [IC], coupled nodes [CP family of commands],
        constraint equations [CE family of commands], or boundary conditions or
        loads applied directly to any of its nodes or elements.  This applies
        to nodes and elements anywhere in the model, not just in the region
        where you want to request mesh refinement.  See Revising Your Model in
        the Modeling and Meshing Guide for additional restrictions on mesh
        refinement.

        This command is also valid for rezoning.
        """
        command = f"KREFINE,{np1},{np2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)

    def kscon(self, npt="", delr="", kctip="", nthet="", rrat="", **kwargs):
        """Specifies a keypoint about which an area mesh will be skewed.

        APDL Command: KSCON

        Parameters
        ----------
        npt
            Keypoint number at concentration.  If NPT = ALL, use all
            selected keypoints.  If remaining fields are blank, remove
            concentration from this keypoint (if unmeshed).  If NPT =
            P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI).  A component
            name may also be substituted for NPT.

        delr
            Radius of first row of elements about keypoint.

        kctip
            Crack tip singularity key:

            0 - Do not skew midside nodes, if any, within the element.

            1 - Skew midside nodes of the first row of elements to the
                1/4 point for crack tip singularity.

        nthet
            Number of elements in circumferential direction (defaults
            to approximately one per 45° (or one per 30°, if KCTIP =
            1)).

        rrat
            Ratio of 2nd row element size to DELR (defaults to 0.75, or 0.5 if
            KCTIP = 1).

        Notes
        -----
        Defines a concentration keypoint about which an area mesh will
        be skewed. Useful for modeling stress concentrations and crack
        tips.  During meshing, elements are initially generated
        circumferentially about, and radially away, from the
        keypoint. Lines attached to the keypoint are given appropriate
        divisions and spacing ratios. Only one concentration keypoint
        per unmeshed area is allowed.  Use KSCON,STAT to list current
        status of concentration keypoints. The KSCON command does not
        support 3-D modeling.

        This command is also valid for rezoning.
        """
        command = f"KSCON,{npt},{delr},{kctip},{nthet},{rrat}"
        return self.run(command, **kwargs)

    def latt(self, mat="", real="", type_="", kb="", ke="", secnum="", **kwargs):
        """Associates element attributes with the selected, unmeshed lines.

        APDL Command: LATT

        Parameters
        ----------
        mat, real, type\\_
            Material number, real constant set number, and type number
            to be associated with selected, unmeshed lines.

        kb, ke
            Beginning and ending orientation keypoints to be
            associated with selected, unmeshed lines.  ANSYS uses the
            location of these keypoints to determine how to orient
            beam cross sections during beam meshing.  Beam elements
            may be created along a line with a constant orientation by
            specifying only one orientation keypoint (KB), or a
            pre-twisted beam may be created by selecting different
            orientation keypoints at each end of the line (KB and KE).
            (For a line bounded by two keypoints (KP1 and KP2), the
            orientation vector at the beginning of the line extends
            from KP1 to KB, and the orientation vector at the end of
            the line extends from KP2 to KE.  The orientation vectors
            are used to compute the orientation nodes of the
            elements.)

        secnum
            Section identifier to be associated with selected,
            unmeshed lines.  For details, see the description of the
            SECTYPE and SECNUM commands.

        Notes
        -----
        The element attributes specified by the LATT command will be
        used when the lines are meshed.

        Lines subsequently generated from the lines will also have the
        attributes specified by MAT, REAL, TYPE, and SECNUM.  If a
        line does not have these attributes associated with it (by
        this command) at the time it is meshed, the attributes are
        obtained from the then current MAT, REAL, TYPE, and SECNUM
        command settings.

        In contrast, the values specified by KB and KE apply only to
        the selected lines; that is, lines subsequently generated from
        these lines will not share these attributes.  Similarly, if a
        line does not have KB and KE attributes associated with it via
        the LATT command at the time it is meshed, ANSYS cannot obtain
        the attributes from elsewhere.  See the discussion on beam
        meshing in Meshing Your Solid Model in the Modeling and
        Meshing Guide for more information.

        Reissue the LATT command (before lines are meshed) to change
        the attributes.  A zero (or blank) argument removes the
        corresponding association. If any of the arguments are defined
        as -1, then that value will be left unchanged in the selected
        set.

        In some cases, ANSYS can proceed with a line meshing operation
        even when no logical element type has been assigned via
        LATT,,,TYPE or TYPE.  See Meshing Your Solid Model in the
        Modeling and Meshing Guide for more information about setting
        element attributes.
        """
        command = f"LATT,{mat},{real},{type_},,{kb},{ke},{secnum}"
        return self.run(command, **kwargs)

    def lccat(self, nl1="", nl2="", **kwargs):
        """Concatenates multiple lines into one line for mapped meshing.

        APDL Command: LCCAT

        Parameters
        ----------
        nl1, nl2
            Lines to be concatenated.  If NL1 = ALL, NL2 is ignored and all
            selected lines [LSEL] are concatenated.  If NL1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).  A component name may also be substituted
            for NL1 (NL2 is ignored).

        Notes
        -----
        Concatenates multiple, adjacent lines (the input lines) into one line
        (the output line) in preparation for mapped meshing.  An area that
        contains too many lines for mapped meshing can still be mapped meshed
        if some of the lines in that area are first concatenated (see Meshing
        Your Solid Model in the Modeling and Meshing Guide for details on
        mapped meshing restrictions).

        LCCAT is meant to be used solely for meshing and cannot be used for any
        other purposes.  Specifically, (a) the output line and any areas that
        have the output line on their line list [ALIST] cannot be used as input
        to any other solid modeling operation (not even another LCCAT command);
        and (b) the output line cannot accept solid model boundary conditions
        [DL, SFL].

        The output line will take on the element divisions of the input lines
        and will not accept element divisions that are directly assigned
        [LESIZE].  The output line from the LCCAT operation will be coincident
        with the input lines and the input lines will be retained.  Consider
        the LCOMB command instead of LCCAT if you wish to delete the input
        lines and if the lines to be combined have similar slopes at the common
        keypoint(s).  When an LCCAT command is issued, area line lists [ALIST]
        that contain all of the input lines will be updated so that the area
        line lists refer to the output line instead of the input lines.
        Deletion of the output line [LDELE] effectively reverses the LCCAT
        operation and restores area line lists to their original condition.

        You can use the LSEL command to select lines that were created by
        concatenation, and then follow it with an LDELE,ALL command to delete
        them.  Also see Meshing Your Solid Model in the Modeling and Meshing
        Guide for a discussion on how to easily select and delete concatenated
        lines in one step.
        """
        command = f"LCCAT,{nl1},{nl2}"
        return self.run(command, **kwargs)

    def lclear(self, nl1="", nl2="", ninc="", **kwargs):
        """Deletes nodes and line elements associated with selected lines.

        APDL Command: LCLEAR

        Parameters
        ----------
        nl1, nl2, ninc
            Delete mesh for lines NL1 to NL2 (defaults to NL1) in steps of NINC
            (defaults to 1).  If NL1 = ALL, NL2 and NINC are ignored and the
            mesh for all selected lines [LSEL] is deleted.  If NL1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NL1 (NL2 and NINC are ignored).

        Notes
        -----
        Deletes all nodes and line elements associated with selected lines
        (regardless of whether the nodes or elements are selected).  Nodes
        shared by adjacent meshed lines and nodes associated with non-line
        elements will not be deleted.  Attributes assigned as a result of LATT
        are maintained.  In the program's response to the command, if a line or
        keypoint is tallied as "cleared," it means either its node or element
        reference was deleted.
        """
        command = f"LCLEAR,{nl1},{nl2},{ninc}"
        return self.run(command, **kwargs)

    def lesize(
        self,
        nl1="",
        size="",
        angsiz="",
        ndiv="",
        space="",
        kforc="",
        layer1="",
        layer2="",
        kyndiv="",
        **kwargs,
    ):
        """Specifies the divisions and spacing ratio on unmeshed lines.

        APDL Command: LESIZE

        Parameters
        ----------
        nl1
            Number of the line to be modified.  If ALL, modify all selected
            lines [LSEL].  If NL1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NL1.

        size
            If NDIV is blank, SIZE is the division (element edge) length.  The
            number of divisions is automatically calculated from the line
            length (rounded upward to next integer).  If SIZE is zero (or
            blank), use ANGSIZ or NDIV.

        angsiz
            The division arc (in degrees) spanned by the element edge (except
            for straight lines, which always result in one division).  The
            number of divisions is automatically calculated from the line
            length (rounded upward to next integer).

        ndiv
            If positive, NDIV is the number of element divisions per line.  If
            -1 (and KFORC = 1), NDIV is assumed to be zero element divisions
            per line. TARGE169 with a rigid specification ignores NDIV and will
            always mesh with one element division.

        space
            Spacing ratio.  If positive, nominal ratio of last division size to
            first division size (if > 1.0, sizes increase, if < 1.0, sizes
            decrease).  If negative, ``|SPACE|`` is nominal ratio of center
            division(s) size to end divisions size.  Ratio defaults to 1.0
            (uniform spacing). For layer-meshing, a value of 1.0 normally is
            used. If SPACE = FREE, ratio is determined by other considerations

        kforc
            KFORC 0-3 are used only with NL1 = ALL.  Specifies which selected
            lines are to be modified.

            0 - Modify only selected lines having undefined (zero) divisions.

            1 - Modify all selected lines.

            2 - Modify only selected lines having fewer divisions
                (including zero) than specified with this command.

            3 - Modify only selected lines having more divisions than
                specified with this command.

            4 - Modify only nonzero settings for SIZE, ANGSIZ, NDIV,
                SPACE, LAYER1, and LAYER2.  If KFORC = 4, blank or 0
                settings remain unchanged.

        layer1
            Layer-meshing control parameter.  Distance which defines the
            thickness of the inner mesh layer, LAYER1.  Elements in this layer
            are uniformly-sized with edge lengths equal to the specified
            element size for the line (either through SIZE or line-
            length/NDIV).  A positive value for LAYER1 is interpreted as an
            absolute length, while a negative value in interpreted as a
            multiplier on the specified element size for the line.  As a
            general rule, the resulting thickness of the inner mesh layer
            should be greater than or equal to the specified element size for
            the line.  If LAYER1 = OFF, layer-meshing control settings are
            cleared for the selected lines.  The default value is 0.0

        layer2
            Layer-meshing control parameter.  Distance which defines the
            thickness of the outer mesh layer, LAYER2.  Elements in this layer
            transition in size from those in LAYER1 to the global element size.
            A positive value of LAYER2 is interpreted as an absolute length,
            while a negative value is interpreted as a mesh transition factor.
            A value of LAYER2 = -2 would indicate that elements should
            approximately double in size as the mesh progresses normal to
            LAYER1. The default value is 0.0.

        kyndiv
            0, No, and Off means that SmartSizing cannot override specified
            divisions and spacing ratios. Mapped mesh fails if divisions do not
            match. This defines the specification as "hard".

        Notes
        -----
        Defines the number of divisions and the spacing ratio on selected
        lines.  Lines with previously specified divisions may also be changed.

        This command is also valid for rezoning.
        """
        command = f"LESIZE,{nl1},{size},{angsiz},{ndiv},{space},{kforc},{layer1},{layer2},{kyndiv}"
        return self.run(command, **kwargs)

    def lmesh(self, nl1="", nl2="", ninc="", **kwargs):
        """Generates nodes and line elements along lines.

        APDL Command: LMESH

        Parameters
        ----------
        nl1, nl2, ninc
            Mesh lines from NL1 to NL2 (defaults to NL1) in steps of NINC
            (defaults to 1).  If NL1 = ALL, NL2 and NINC are ignored and all
            selected lines [LSEL] are meshed.  If NL1 = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for NL1 (NL2
            and NINC are ignored).

        Notes
        -----
        Generates nodes and line elements along lines.  Missing nodes required
        for the generated elements are created and assigned the lowest
        available numbers.
        """
        command = f"LMESH,{nl1},{nl2},{ninc}"
        return self.run(command, **kwargs)

    def lrefine(
        self,
        nl1="",
        nl2="",
        ninc="",
        level="",
        depth="",
        post="",
        retain="",
        **kwargs,
    ):
        """Refines the mesh around specified lines.

        APDL Command: LREFINE

        Parameters
        ----------
        nl1, nl2, ninc
            Lines (NL1 to NL2 in increments of NINC) around which the mesh is
            to be refined.  NL2 defaults to NL1, and NINC defaults to 1.  If
            NL1 = ALL, NL2 and NINC are ignored and all selected lines are used
            for refinement.  If NL1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NL1 (NL2 and NINC are
            ignored).

        level
            Amount of refinement to be done.  Specify the value of LEVEL as an
            integer from 1 to 5, where a value of 1 provides minimal
            refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth
            Depth of mesh refinement in terms of the number of elements outward
            from the indicated lines (defaults to 1).

        post
            Type of postprocessing to be done after element splitting, in order
            to improve element quality:

            OFF - No postprocessing will be done.

            SMOOTH - Smoothing will be done.  Node locations may change.

            CLEAN - Smoothing and cleanup will be done.  Existing elements may be deleted, and node
                    locations may change (default).

        retain
            Flag indicating whether quadrilateral elements must be retained in
            the refinement of an all-quadrilateral mesh.  (The ANSYS program
            ignores the RETAIN argument when you are refining anything other
            than a quadrilateral mesh.)

            ON - The final mesh will be composed entirely of quadrilateral elements, regardless
                 of the element quality (default).

            OFF - The final mesh may include some triangular elements in order to maintain
                  element quality and provide transitioning.

        Notes
        -----
        LREFINE performs local mesh refinement around the specified lines. By
        default, the indicated elements are split to create new elements with
        1/2 the edge length of the original elements (LEVEL = 1).

        LREFINE refines all area elements and tetrahedral volume elements that
        are adjacent to the specified lines. Any volume elements that are
        adjacent to the specified lines, but are not tetrahedra (for example,
        hexahedra, wedges, and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains initial
        conditions at nodes [IC], coupled nodes [CP family of commands],
        constraint equations [CE family of commands], or boundary conditions or
        loads applied directly to any of its nodes or elements. This applies to
        nodes and elements anywhere in the model, not just in the region where
        you want to request mesh refinement. For additional restrictions on
        mesh refinement, see Revising Your Model in the Modeling and Meshing
        Guide.

        This command is also valid for rezoning.
        """
        command = f"LREFINE,{nl1},{nl2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)

    def mat(self, mat="", **kwargs):
        """Sets the element material attribute pointer.

        APDL Command: MAT

        Parameters
        ----------
        mat
            Assign this material number to subsequently defined elements
            (defaults to 1).

        Notes
        -----
        Identifies the material number to be assigned to subsequently defined
        elements.  This number refers to the material number (MAT) defined with
        the material properties [MP].  Material numbers may be displayed
        [/PNUM].

        Examples
        --------
        Set the material ID pointer to 2

        >>> mapdl.mat(2)
        """
        command = f"MAT,{mat}"
        return self.run(command, **kwargs)

    def mcheck(self, lab="", **kwargs):
        """Checks mesh connectivity.

        APDL Command: MCHECK

        Parameters
        ----------
        lab
            Operation:

            ESEL - Unselects the valid elements.

        Notes
        -----
        Wherever two area or volume elements share a common face, MCHECK
        verifies that the way the elements are connected to the face is
        consistent with their relative normals or integrated volumes. (This may
        detect folds or otherwise overlapping elements.)

        MCHECK verifies that the element exterior faces form simply-connected
        closed surfaces. (This may detect unintended cracks in a mesh.)

        MCHECK warns if the number of element facets in a 2-D loop or 3-D
        shell is not greater than a computed limit. This limit is the smaller
        of either three times the number of faces on one element, or one-tenth
        the total number of element faces in the model. (This may detect holes
        in the middle of a mesh.)

        The MCHECK command will perform a number of validity checks on the
        selected elements, including:

        Normal check:  Wherever two area elements share a common edge, MCHECK
        verifies that the ordering of the nodes on each element is consistent
        with their relative normals.

        Volume check:  Wherever two volume elements share a common face, MCHECK
        verifies that the sign of the integrated volume of each element is
        consistent.

        Closed surface check:  MCHECK verifies that the element exterior faces
        form simply-connected closed surfaces (this may detect unintended
        cracks in a mesh).

        Check for holes in the mesh:  MCHECK warns if the number of element
        faces surrounding an interior void in the mesh is small enough to
        suggest one or more accidentally omitted elements, rather than a
        deliberately formed hole. For this test, the number of faces around the
        void is compared to the smaller of a) three times the number of faces
        on one element, or b) one-tenth the total number of element faces in
        the model.
        """
        command = f"MCHECK,{lab}"
        return self.run(command, **kwargs)

    def modmsh(self, lab="", **kwargs):
        """Controls the relationship of the solid model and the FE model.

        APDL Command: MODMSH

        Parameters
        ----------
        lab
            Relationship key:

            STAT - Gives status of command (default).   This applies only to the CHECK option  (no
                   status is provided for the DETACH option).

            NOCHECK - Deactivates the checking of the solid model and the finite element model.
                      Allows elements and nodes generated with the mesh
                      commands to be modified directly (EMODIF, NMODIF, EDELE,
                      NDELE, etc.). Also deactivates solid model hierarchical
                      checking so that areas attached to volumes may be deleted
                      etc.

            CHECK - Reactivates future checking of the solid model.

            DETACH - Releases all associativity between the current solid model and finite element
                     model.  ANSYS deletes any element attributes that were
                     assigned to the affected solid model entities through
                     default attributes (that is, through the TYPE, REAL, MAT,
                     SECNUM, and ESYS command settings and a subsequent meshing
                     operation). However, attributes that were assigned
                     directly to the solid model entities (via the KATT, LATT,
                     AATT, and VATT commands) are not deleted.

        Notes
        -----
        Affects the relationship of the solid model (keypoints, lines, areas,
        volumes) and the finite element model (nodes, elements, and boundary
        conditions).

        Specify Lab = NOCHECK carefully. By deactivating checking, the solid
        model database can be corrupted by subsequent operations.

        After specifying Lab = DETACH, it is no longer possible to select or
        define finite element model items in terms of the detached solid model
        or to clear the mesh.
        """
        command = f"MODMSH,{lab}"
        return self.run(command, **kwargs)

    def mopt(self, lab="", value="", **kwargs):
        """Specifies meshing options.

        APDL Command: MOPT

        Parameters
        ----------
        lab
            Meshing option to be specified (determines the meaning of Value):

            AORDER - Mesh by ascending area size order.  Set Value to ON to mesh smaller areas
                     first. Using this results in finer meshes in critical
                     areas for volume meshes; this can be used for cases where
                     SMRTSIZE does not mesh as needed. Default is OFF.

            EXPND - Area mesh expansion (or contraction) option.  (This option is the same as
                    SMRTSIZE,,,EXPND.) This option is used to size internal
                    elements in an area based on the size of the elements on
                    the area's boundaries.

            Value is the expansion (or contraction) factor. For example, issuing MOPT,EXPND,2 before meshing an area will allow a mesh with elements that are approximately twice as large in the interior of an area as they are on the boundary. If Value is less than 1, a mesh with smaller elements on the interior of the area will be allowed. Value for this option should be greater than 0.5 but less than 4.  - Value defaults to 1, which does not allow expansion or contraction of internal
                              element sizes (except when using AESIZE sizing).
                              If Value = 0, the default value of 1 will be
                              used. The actual size of the internal elements
                              will also depend on the TRANS option (or upon
                              AESIZE or ESIZE sizing, if used).

            TETEXPND - Tet-mesh expansion (or contraction) option. This option is used to size
                       internal elements in a volume based on the size of the
                       elements on the volume's boundaries.

            Value is the expansion (or contraction) factor.  For example, issuing MOPT,TETEXPND,2 before meshing a volume will allow a mesh with elements that are approximately twice as large in the interior of the volume as they are on the boundary. If Value is less than 1, a mesh with smaller elements on the interior of the volume will be allowed. Value for this option should be greater than 0.1 but less than 3.   - Value defaults to 1, which does not allow expansion or contraction of internal
                              element sizes.  If Value = 0, the default value
                              of 1 will be used. If Value is greater than 2,
                              mesher robustness may be affected.

            The TETEXPND option is supported for both the VMESH and FVMESH commands.  Tet-mesh expansion is the only mesh control supported by FVMESH. - TRANS

            Mesh-transition option. Controls how rapidly elements are permitted to change in size from the boundary to the interior of an area. (This option performs the same operation as SMRTSIZE,,,,TRANS.)   - Value is the transitioning factor. Value defaults to 2.0, which permits
                              elements to approximately double in size as they
                              approach the interior of the area.  (If Value =
                              0, the default value of 2 will be used.) Value
                              must be greater than 1 and, for best results,
                              should be less than 4.  The actual size of the
                              internal elements will also depend on the EXPND
                              option (or upon AESIZE or ESIZE sizing, if used).

            For a quad mesh with any element size, this option has no effect, as the program strictly respects any face size to ensure the most uniform quad mesh possible. To obtain a graded mesh using this option, apply LESIZE to the lines of the desired face. - AMESH

            Triangle surface-meshing option.  Valid inputs for Value are:     - DEFAULT

            Allows the program to choose which triangle mesher to use.  In most cases, the program chooses the main triangle mesher, which is the Riemann space mesher.  If the chosen mesher fails for any reason, the program invokes the alternate mesher and retries the meshing operation. - MAIN

            The program uses the main triangle mesher (Riemann space mesher), and it does not invoke an alternate mesher if the main mesher fails.  The Riemann space mesher is well suited for most surfaces. - ALTERNATE

            The program uses the first alternate triangle mesher (3-D tri-mesher), and it does not invoke another mesher if this mesher fails.  This option is not recommended due to speed considerations.  However, for surfaces with degeneracies in parametric space, this mesher often provides the best results. - ALT2

            The program uses the second alternate triangle mesher (2-D parametric space mesher), and it does not invoke another mesher if this mesher fails.  This option is not recommended for use on surfaces with degeneracies (spheres, cones, etc.) or poorly parameterized surfaces because poor meshes may result. - QMESH

            Quadrilateral surface meshing option.  (Quadrilateral surface meshes will differ based on which triangle surface mesher is selected.  This is true because all free quadrilateral meshing algorithms use a triangle mesh as a starting point.)  Valid inputs for Value are:     - DEFAULT

            Let the program choose which quadrilateral mesher to use.  In most cases, the program will choose the main quadrilateral mesher, which is the Q-Morph (quad-morphing) mesher.  For very coarse meshes, the program may choose the alternate quadrilateral mesher instead.  In most cases, the Q-Morph mesher results in higher quality elements.  If either mesher fails for any reason, the program invokes the other mesher and retries the meshing operation.  (Default.) - MAIN

            The program uses the main quadrilateral mesher (Q-Morph mesher), and it does not invoke the alternate mesher if the main mesher fails. - ALTERNATE

            The program uses the alternate quadrilateral mesher, and it does not invoke the Q-Morph mesher if the alternate mesher fails.  To use the alternate quadrilateral mesher, you must also select MOPT,AMESH,ALTERNATE or MOPT,AMESH,ALT2. - VMESH

            Tetrahedral element meshing option.  Valid inputs for Value are:     - DEFAULT

            Let the program choose which tetrahedra mesher to use.   - MAIN

            Use the main tetrahedra mesher (Delaunay technique mesher).  (GHS3D meshing technology by P. L. George, INRIA, France.)  For most models, this mesher is significantly faster than the alternate mesher. - ALTERNATE

            Use the alternate tetrahedra mesher (advancing front mesher).  This mesher does not support the generation of a tetrahedral volume mesh from facets (FVMESH).  If this mesher is selected and you issue the FVMESH command, the program uses the main tetrahedra mesher to create the mesh from facets and issues a warning message to notify you. - SPLIT

            Quad splitting option for non-mapped meshing.  If Value = 1, ON, or ERR, quadrilateral elements in violation of shape error limits are split into triangles (default).  If Value = 2 or WARN, quadrilateral elements in violation of either shape error or warning limits are split into triangles.  If Value = OFF, splitting does not occur, regardless of element quality. - LSMO

            Line smoothing option. Value can be ON or OFF.  If Value = ON, smoothing of nodes on area boundaries is performed during smoothing step of meshing.  During smoothing, node locations are adjusted to achieve a better mesh.  If Value = OFF (default), no smoothing takes place at area boundaries. - CLEAR

            This option affects the element and node numbering after clearing a mesh.  If Value = ON (default), the starting node and element numbers will be the lowest available number after the nodes and elements are cleared.  If Value = OFF, the  starting node and element numbers are not reset after the clear operation. - PYRA
        """
        command = f"MOPT,{lab},{value}"
        return self.run(command, **kwargs)

    def mshape(self, key="", dimension="", **kwargs):
        """For elements that support multiple shapes, specifies the element shape

        APDL Command: MSHAPE
        to be used for meshing.

        Parameters
        ----------
        key
            Key indicating the element shape to be used:

            0 - Mesh with quadrilateral-shaped elements when Dimension = 2-D mesh with
                hexahedral-shaped elements when Dimension = 3-D.

            1 - Mesh with triangle-shaped elements when Dimension = 2-D mesh with tetrahedral-
                shaped elements when Dimension = 3-D.

        dimension
            Specifies the dimension of the model to be meshed:

            2D - 2-D model (area mesh).

            3D - 3-D model (volume mesh).

        Notes
        -----
        If no value is specified for Dimension the value of KEY determines the
        element shape that will be used for both 2-D and 3-D meshing.  In other
        words, if you specify MSHAPE,0, quadrilateral-shaped and hexahedral-
        shaped elements will be used.  If you specify MSHAPE,1, triangle-shaped
        and tetrahedral-shaped elements will be used.

        The MSHAPE, MSHKEY, and MSHMID commands replace the functionality that
        was provided by the ESHAPE command in ANSYS 5.3 and earlier releases.

        This command is also valid for rezoning.
        """
        command = f"MSHAPE,{key},{dimension}"
        return self.run(command, **kwargs)

    def mshcopy(
        self,
        keyla="",
        laptrn="",
        lacopy="",
        kcn="",
        dx="",
        dy="",
        dz="",
        tol="",
        low="",
        high="",
        **kwargs,
    ):
        """Simplifies the generation of meshes that have matching node element

        APDL Command: MSHCOPY
        patterns on two different line groups (in 2-D) or area groups (3-D).

        Parameters
        ----------
        keyla
            Copy line mesh (default) if LINE, 0 or 1. Copy area mesh if AREA,
            or 2.

        laptrn
            Meshed line/area to be copied, or a component name containing a
            list. If LAPTRN = P, graphical picking is enabled (valid only in
            the GUI).

        lacopy
            Unmeshed line/area to get copied mesh, or a component name
            containing a list. If LACOPY = P, graphical picking is enabled
            (valid only in the GUI).

        kcn
            In coordinate system KCN, LAPTRN + DX DY DZ = LACOPY.

        dx, dy, dz
            Node location increments in the active coordinate system (DR, Dθ,
            DZ for cylindrical, DR, Dθ, DΦ for spherical or toroidal).

        tol
            Tolerance. Defaults to 1.e--4.

        low
            Name of low node component to be defined (optional).

        high
            Name of high node component to be defined (optional).

        Notes
        -----
        Matching meshes are used for rotational (cyclic) symmetry, or for
        contact analysis using coupling or node-to-node gap elements. See Using
        CPCYC and MSHCOPY Commands in the Modeling and Meshing Guide for more
        information.
        """
        command = (
            f"MSHCOPY,{keyla},{laptrn},{lacopy},{kcn},{dx},{dy},{dz},{tol},{low},{high}"
        )
        return self.run(command, **kwargs)

    def mshkey(self, key="", **kwargs):
        """Specifies whether free meshing or mapped meshing should be used to mesh

        APDL Command: MSHKEY
        a model.

        Parameters
        ----------
        key
            Key indicating the type of meshing to be used:

            0 - Use free meshing (the default).

            1 - Use mapped meshing.

            2 - Use mapped meshing if possible; otherwise, use free meshing.  If you specify
                MSHKEY,2, SmartSizing will be inactive even while free meshing
                non-map-meshable areas.

        Notes
        -----
        The MSHKEY, MSHAPE, and MSHMID commands replace the functionality that
        was provided by the ESHAPE command in ANSYS 5.3 and earlier releases.

        This command is also valid for rezoning.
        """
        command = f"MSHKEY,{key}"
        return self.run(command, **kwargs)

    def mshmid(self, key="", **kwargs):
        """Specifies placement of midside nodes.

        APDL Command: MSHMID

        Parameters
        ----------
        key
            Key indicating placement of midside nodes:

            0 - Midside nodes (if any) of elements on a region boundary follow the curvature of
                the boundary line or area (the default).

            1 - Place midside nodes of all elements so that element edges are straight.  Allows
                coarse mesh along curves.

            2 - Do not create midside nodes (elements will have removed midside nodes).

        Notes
        -----
        The MSHMID, MSHAPE, and MSHKEY commands replace the functionality that
        was provided by the ESHAPE command in ANSYS 5.3 and earlier releases.

        This command is also valid for rezoning.
        """
        command = f"MSHMID,{key}"
        return self.run(command, **kwargs)

    def mshpattern(self, key="", **kwargs):
        """Specifies pattern to be used for mapped triangle meshing.

        APDL Command: MSHPATTERN

        Parameters
        ----------
        key
            Key indicating triangle pattern to be used (the figures below
            illustrate the pattern that will be used for each value of KEY):

            0 - Let ANSYS choose the pattern (the default).  ANSYS maximizes the minimum angle
                of the triangular-shaped elements that are created.

            1 - Unidirectional split at node I.

            2 - Unidirectional split at node J.

        Notes
        -----
        "Mapped triangle meshing" refers to the ANSYS program's ability to take
        a map-meshable area and mesh it with triangular elements, based on the
        value of MSHPATTERN,KEY. This type of meshing is particularly useful
        for analyses that involve the meshing of rigid contact elements.

        The MSHPATTERN command is valid only when you have specified that ANSYS
        use triangle-shaped elements [MSHAPE,1,2D] (or you are meshing with an
        element that supports only triangles), and you have also specified
        mapped meshing [MSHKEY,1] to mesh an area.

        For details about mapped meshing with triangles, see the Modeling and
        Meshing Guide.
        """
        command = f"MSHPATTERN,{key}"
        return self.run(command, **kwargs)

    def nrefine(
        self,
        nn1="",
        nn2="",
        ninc="",
        level="",
        depth="",
        post="",
        retain="",
        **kwargs,
    ):
        """Refines the mesh around specified nodes.

        APDL Command: NREFINE

        Parameters
        ----------
        nn1, nn2, ninc
            Nodes (NN1 to NN2 in increments of NINC) around which the mesh is
            to be refined.  NN2 defaults to NN1, and NINC defaults to 1.  If
            NN1 = ALL, NN2 and NINC are ignored and all selected nodes are used
            for refinement.  If NN1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).  A
            component name may also be substituted for NN1 (NN2 and NINC are
            ignored).

        level
            Amount of refinement to be done.  Specify the value of LEVEL as an
            integer from 1 to 5, where a value of 1 provides minimal
            refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth
            Depth of mesh refinement in terms of number of elements outward
            from the indicated nodes (defaults to 1).

        post
            Type of postprocessing to be done after element splitting, in order
            to improve element quality:

            OFF - No postprocessing will be done.

            SMOOTH - Smoothing will be done.  Node locations may change.

            CLEAN - Smoothing and cleanup will be done.  Existing elements may be deleted, and node
                    locations may change (default).

        retain
            Flag indicating whether quadrilateral elements must be retained in
            the refinement of an all-quadrilateral mesh.  (The ANSYS program
            ignores the RETAIN argument when you are refining anything other
            than a quadrilateral mesh.)

            ON - The final mesh will be composed entirely of quadrilateral elements, regardless
                 of the element quality (default).

            OFF - The final mesh may include some triangular elements in order to maintain
                  element quality and provide transitioning.

        Notes
        -----
        NREFINE performs local mesh refinement around the specified nodes.  By
        default, the indicated elements are split to create new elements with
        1/2 the edge length of the original elements (LEVEL = 1).

        NREFINE refines all area elements and tetrahedral volume elements that
        are adjacent to the specified nodes.  Any volume elements that are
        adjacent to the specified nodes, but are not tetrahedra (for example,
        hexahedra, wedges, and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains initial
        conditions at nodes [IC], coupled nodes [CP family of commands],
        constraint equations [CE family of commands], or boundary conditions or
        loads applied directly to any of its nodes or elements.  This applies
        to nodes and elements anywhere in the model, not just in the region
        where you want to request mesh refinement.  For additional restrictions
        on mesh refinement, see Revising Your Model in the Modeling and Meshing
        Guide.

        This command is also valid for rezoning.
        """
        command = f"NREFINE,{nn1},{nn2},{ninc},{level},{depth},{post},{retain}"
        return self.run(command, **kwargs)

    def psmesh(
        self,
        secid="",
        name="",
        p0="",
        egroup="",
        num="",
        kcn="",
        kdir="",
        value="",
        ndplane="",
        pstol="",
        pstype="",
        ecomp="",
        ncomp="",
        **kwargs,
    ):
        """Create and mesh a pretension section

        APDL Command: PSMESH

        Parameters
        ----------
        secid
            Unique section number. This number must not already be assigned to
            a section.

        name
            Unique eight character descriptive name, if desired.

        p0
            Pretension node number. The node will be defined if it doesn't
            exist and the number defaults to the highest node number plus one.

        egroup, num
            Element group on which PSMESH will operate. If Egroup = P,
            graphical picking is enabled and NUM is ignored (valid only in the
            GUI).

            L (or LINE) - PSMESH operates on all elements in the line specified by NUM. New pretension
                          nodes are associated with NUM or entities below it.
                          Any subsequent LCLEAR operation of NUM deletes the
                          pretension elements and nodes created by PSMESH.

            A (or AREA) - PSMESH operates on all elements in the area specified by NUM. New pretension
                          nodes are associated with NUM or entities below it.
                          Any subsequent ACLEAR of NUM deletes the pretension
                          elements and nodes created by PSMESH.

            V (or VOLU) - PSMESH operates on all elements in the volume specified by NUM. New pretension
                          nodes are associated with NUM or entities below it.
                          Any subsequent VCLEAR of NUM deletes the pretension
                          elements and nodes created by PSMESH.

            P - PSMESH operates on elements selected through the subsequent picking operations,
                and NUM is ignored

            ALL - The command operates on all selected elements, and NUM is ignored.

        kcn
            Coordinate system number for the separation surface and normal
            direction.

        kdir
            Direction (x, y, or z) normal to separation surface in the KCN
            coordinate system.

        value
            Point along the KDIR axis at which to locate the separation
            surface. Ignored if NDPLANE is supplied.

        ndplane
            Existing node that PSMESH will use to locate the separation
            surface. If NDPLANE is supplied, the location of the separation
            surface is defined by the KDIR coordinate of NDPLANE.

        pstol
            Optional tolerance below VALUE. Allows nodes occurring precisely at
            or slightly below the separation  to be identified properly as
            above the plane. Has the effect of shifting the plane down by
            PSTOL.  The following expression represents the default value:

        pstype
            If specified, this value is the type number for pretension
            elements. (If not specified, ANSYS defines this value.) If already
            defined, it must be of type PRETS179.

        ecomp
            If specified, the name of a component to be composed of new
            pretension elements and existing elements modified by the PSMESH
            command.

        ncomp
            Name of a component to be composed of nodes on new pretension
            elements.

        Notes
        -----
        The PSMESH command creates a pretension section normal to the
        pretension load direction by cutting the mesh along existing element
        boundaries at the point defined by VALUE or NDPLANE and inserting
        PRETS179 elements. The PSMESH command verifies that PSTYPE is PRETS179;
        if it is not, the command finds the lowest available ITYPE that is
        PRETS179, or if necessary will create a new one.

        When it is necessary to define the pretension node, ANSYS uses node
        NDPLANE. If the NDPLANE value is not specified, ANSYS defines the
        pretension node at:

        The centroid of geometric entity NUM, if Egroup = LINE, AREA or VOLU

        The centroid location of all selected elements, if Egroup = ALL or if
        graphical picking is used.

        If the elements to which the pretension load is to be applied have
        already been meshed in two groups, PSMESH cannot be used to insert the
        pretension elements. The EINTF command must be used to insert the
        PRETS179 elements between the two meshed groups.

        The PSMESH operation copies any nodal temperatures you have defined on
        the split surface of the original mesh from the original nodes to the
        newly created coincident duplicate nodes. However, displacements,
        forces, and other boundary conditions are not copied.

        By mathematical definition, the pretension surface must always be a
        flat plane. In a non-Cartesian coordinate system, the PSMESH command
        creates that plane at the indicated position, oriented with respect to
        the specified direction of the active system (in the same manner that
        the NROTAT command orients a nodal system with respect to a curved
        system). For example, assuming a X = 1 and Y = 45 in a cylindrical
        coordinate system with Z as the axis of rotation (KCN = 1), a
        pretension surface normal to X tilts 45 degrees away from the global X
        axis.

        The PSMESH command is valid for structural analyses only.
        """
        command = f"PSMESH,{secid},{name},{p0},{egroup},{num},{kcn},{kdir},{value},{ndplane},{pstol},{pstype},{ecomp},{ncomp}"
        return self.run(command, **kwargs)

    def real(self, nset="", **kwargs):
        """Sets the element real constant set attribute pointer.

        APDL Command: REAL

        Parameters
        ----------
        nset
            Assign this real constant set number to subsequently defined
            elements (defaults to 1).

        Notes
        -----
        Identifies the real constant set number to be assigned to subsequently
        defined elements.  This number refers to the real constant set number
        (NSET) defined with the real constant sets [R].  Real constant set
        numbers may be displayed [/PNUM].  If the element type requires no real
        constants, this entry is ignored.  Elements of different type should
        not refer to the same real constant set.
        """
        command = f"REAL,{nset}"
        return self.run(command, **kwargs)

    def rthick(self, par="", iloc="", jloc="", kloc="", lloc="", **kwargs):
        """Defines variable thickness at nodes for shell elements.

        APDL Command: RTHICK

        Parameters
        ----------
        par
            Array parameter (indexed by node number) that expresses the
            function to be mapped.  For example, func (17) should be the
            desired shell thickness at node 17.

        iloc
            Position in real constant set for thickness at node I of the
            element (default 1).

        jloc
            Position in real constant set for thickness at node J of the
            element (default 2).

        kloc
            Position in real constant set for thickness at node K of the
            element (default 3).

        lloc
            Position in real constant set for thickness at node L of the
            element (default 4).

        Notes
        -----
        After RTHICK, the REAL number will match the ELEM number of each
        selected element. For example, R (ILOC) = func (I NODE), R (JLOC) =
        func (J NODE), etc.

        R(ILOC), R(JLOC), R(KLOC), and R(LLOC) on a previously defined real
        constant will be overwritten.  Any other real constants on a previously
        defined real constant set will remain unchanged. This command cannot be
        used for beam elements.
        """
        command = f"RTHICK,{par},{iloc},{jloc},{kloc},{lloc}"
        return self.run(command, **kwargs)

    def shpp(self, lab="", value1="", value2="", **kwargs):
        """Controls element shape checking.

        APDL Command: SHPP

        Parameters
        ----------
        lab
            Shape checking option.  (When Lab = WARN, STATUS, SUMMARY, or
            DEFAULT, the remaining arguments are ignored.)

            ON - Activates element shape checking.  New elements, regardless of how they are
                 created, are tested against existing warning and error limits.
                 (The existing limits may be the default limits, or previously
                 modified limits.)  Elements that violate error limits produce
                 error messages and either (a) cause a meshing failure, or (b)
                 for element creation or storage other than AMESH or VMESH, are
                 not stored.  Elements that violate warning limits produce
                 warning messages.  If shape checking was previously turned off
                 [SHPP,OFF] and you turn it on, existing elements are marked as
                 untested; use the CHECK command to retest them.  With this
                 option, you may also specify a value for VALUE1 to turn
                 individual shape tests on.  If you do not specify a value for
                 VALUE1, all shape tests are turned on.

            WARN - Activates element shape checking; however, in contrast to SHPP,ON, elements
                   that violate error limits do not cause either a meshing or
                   element storage failure.  Instead, they produce warning
                   messages to notify you that error limits have been violated.
                   This option does not alter current shape parameter limits.
                   Since the default shape parameter error limits are set to
                   allow almost any usable element, the elements this option
                   allows, which would otherwise be forbidden, are likely to be
                   very poorly shaped.

            OFF - Deactivates element shape checking.  This setting does not alter current shape
                  parameter limits.  Use of this option is risky, since poorly
                  shaped elements can lead to analysis results that are less
                  accurate than would otherwise be expected for a given mesh
                  density.  With this option, you may also specify a value for
                  VALUE1 to turn individual shape tests off.  If you do not
                  specify a value for VALUE1, all element shape tests are
                  turned off.

            SILENT - Determines whether element shape checking runs in silent mode.  In silent mode,
                     ANSYS checks elements without issuing warnings, with the
                     exception of the generic warnings that it issues at
                     solution.  With this option, you must also specify a value
                     for VALUE1  (During the execution of certain commands,
                     ANSYS automatically runs element shape checking in silent
                     mode, then internally summarizes the shape test results
                     for all of the new or modified elements.  ANSYS does this
                     when it executes any of the following commands:  AGEN,
                     AMESH, AREFINE, ARSYM, ATRAN, CDREAD, EGEN, ENGEN, ENSYM,
                     EREAD, EREFINE, ESYM, ET, FVMESH, KREFINE, LREFINE,
                     NREFINE, TIMP, VEXT, VGEN, VIMP, VMESH, VOFFST, VROTAT,
                     VSWEEP, VSYMM, and VTRAN.)

            STATUS - Lists the shape parameter limits currently in effect, along with status
                     information about element shape checking (for example,
                     whether any individual shape tests are off, whether any of
                     the shape parameter limits have been modified, and so on).

            SUMMARY - Lists a summary of element shape test results for all selected elements.

            DEFAULT - Resets element shape parameter limits to their default values.  Also, if any
                      individual tests were turned off, turns them back on.
                      (The SHPP,DEFAULT command may be useful if any parameter
                      limits were previously altered by using the MODIFY
                      option.)

            OBJECT - Determines whether element shape test results data is stored in memory.  When
                     this option is turned on, an "object" is created for
                     storing test results in memory.  When this option is
                     turned off, no object is created and no data is stored;
                     thus, any operation that requires shape parameters for an
                     existing element (such as use of the CHECK command) causes
                     the shape parameters to be recomputed.  (Note the
                     distinction between storing the data in memory and storing
                     it in the database; regardless of whether this option is
                     turned on or off, no element shape test results data will
                     be stored in the database.  The element shape parameter
                     object is deleted automatically before any solution.)
                     This setting is independent of shape checking status, with
                     one exception--if shape checking is turned off [SHPP,OFF],
                     the object is not created.  Keep in mind that recomputing
                     shape parameters is more computationally expensive than
                     retrieving them from the object.  With this option, you
                     must also specify a value for the VALUE1 argument; the
                     VALUE2 argument is ignored.

            LSTET - Determines, for Jacobian ratio tests, whether sampling is done at integration
                    points (DesignSpace product method), or at corner nodes.
                    When this option is turned on, sampling is done at
                    integration points, and the default limits for h-element
                    Jacobian ratios are a warning tolerance of 10 and an error
                    tolerance of 40. When this option is turned off, sampling
                    is done at corner nodes, and the corresponding default
                    limits are a warning tolerance of 30 and an error tolerance
                    of 1000. Sampling at the integration points (option on)
                    results in a lower Jacobian ratio, but that ratio is also
                    subjected to a more restrictive error limit. Some elements
                    that have passed the integration point sampling criterion,
                    have failed the corner mode sampling criterion. Because of
                    this, use integration point sampling only for simple linear
                    analyses. For other types of analyses (e.g., nonlinear,
                    electromagnetic), use sampling at corner nodes, which is
                    the more conservative approach. With this option, you must
                    also specify a value for the VALUE1 argument; the VALUE2
                    argument is ignored.

            MODIFY - Indicates that you want to respecify a shape parameter limit.  With this
                     option, you must also specify values for the VALUE1 and
                     VALUE2 arguments.

            FLAT - Determines the warning and error limits used to test elements that may exhibit
                   nonzero/nonconstant Z coordinates. With this option, you
                   must also specify values for the VALUE1 and/or VALUE2
                   arguments.

        value1
            Valid for the ON, OFF, SILENT, OBJECT, LSTET, MODIFY, and FLAT
            options only.  When Lab = ON or OFF, use VALUE1 to individually
            control (that is, turn off or turn on) specific element shape
            tests.  Thus, VALUE1 can be ANGD (SHELL28 corner angle deviation
            tests), ASPECT (aspect ratio tests), PARAL (deviation from
            parallelism of opposite edges tests), MAXANG (maximum corner angle
            tests), JACRAT (Jacobian ratio tests), WARP (warping factor tests),
            or ALL (all tests). When Lab = SILENT, VALUE1 can be ON (to turn
            silent mode on) or OFF (to turn silent mode off).  When Lab =
            OBJECT, VALUE1 can be either 1, YES, or ON to turn on storage of
            element shape test data (the default); or it can be 0, NO, or OFF
            to turn off storage of element shape test data (delete the data and
            recompute as necessary). When Lab = LSTET, VALUE1 can be either 1,
            YES, or ON to choose Jacobian sampling at integration points; or it
            can be 0, NO, or OFF to choose Jacobian sampling at nodes (the
            default). When Lab = MODIFY, VALUE1 is the numeric location (within
            the shape parameter limit array) of the shape parameter limit to be
            modified.  Locations are identified in the element shape checking
            status listing [SHPP,STATUS].  For more information, see the
            examples in the Notes section. When Lab = FLAT, VALUE1 is the
            warning limit for XY element constant Z sets performed at CHECK or
        """
        command = f"SHPP,{lab},{value1},{value2}"
        return self.run(command, **kwargs)

    def smrtsize(
        self,
        sizlvl="",
        fac="",
        expnd="",
        trans="",
        angl="",
        angh="",
        gratio="",
        smhlc="",
        smanc="",
        mxitr="",
        sprx="",
        **kwargs,
    ):
        """Specifies meshing parameters for automatic (smart) element sizing.

        APDL Command: SMRTSIZE

        Parameters
        ----------
        sizlvl
            Overall element size level for meshing.  The level value controls
            the fineness of the mesh.  (Any input in this field causes
            remaining arguments to be ignored.)   Valid inputs are:

            n - Activate SmartSizing and set the size level to n.  Must be an integer value
                from 1 (fine mesh) to 10 (coarse mesh).  Remaining arguments
                are ignored, and argument values are set as shown in
                Table 229: SMRTSIZE - Argument Values for h-elements .

            STAT - List current SMRTSIZE settings.

            DEFA - Set all SMRTSIZE settings to default values (as shown in Table 229: SMRTSIZE -
                   Argument Values for h-elements  for size level 6).

            OFF - Deactivate SmartSizing.  Current settings of DESIZE will be used.  To
                  reactivate SmartSizing, issue SMRTSIZE,n.

        fac
            Scaling factor applied to the computed default mesh sizing.
            Defaults to 1 for h-elements (size level 6), which is medium.
            Values from 0.2 to 5.0 are allowed.

        expnd
            Mesh expansion (or contraction) factor.  (This factor is the same
            as MOPT,EXPND,Value.)  EXPND is used to size internal elements in
            an area based on the size of the elements on the area's boundaries.
            For example, issuing SMRTSIZE,,,2 before meshing an area will allow
            a mesh with elements that are approximately twice as large in the
            interior of an area as they are on the boundary.   If EXPND is less
            than 1, a mesh with smaller elements on the interior of the area
            will be allowed.  EXPND should be greater than 0.5 but less than 4.
            EXPND defaults to 1 for h-elements (size level 6), which does not
            allow expansion or contraction of internal element sizes (except
            when using AESIZE element sizing).  (If EXPND is set to zero, the
            default value of 1 will be used.)  The actual size of the internal
            elements will also depend on the TRANS option or upon AESIZE or
            ESIZE sizing, if used.

        trans
            Mesh transition factor.  (This factor is the same as
            MOPT,TRANS,Value.)  TRANS is used to control how rapidly elements
            are permitted to change in size from the boundary to the interior
            of an area.  TRANS defaults to 2.0 for h-elements (size level 6),
            which permits elements to approximately double in size from one
            element to the next as they approach the interior of the area.  (If
            TRANS is set to zero, the default value will be used.)   TRANS must
            be greater than 1 and, for best results, should be less than 4.
            The actual size of the internal elements will also depend on the
            EXPND option or upon AESIZE or ESIZE sizing, if used.

        angl
            Maximum spanned angle per lower-order element for curved lines.
            Defaults to 22.5 degrees per element (size level 6).  This angle
            limit may be exceeded if the mesher encounters a small feature
            (hole, fillet, etc.).  (This value is not the same as that set by
            DESIZE,,,,ANGL.)

        angh
            Maximum spanned angle per higher-order element for curved lines.
            Defaults to 30 degrees per element (size level 6).  This angle
            limit may be exceeded if the mesher encounters a small feature
            (hole, fillet, etc.).  (This value is NOT the same as that set by
            DESIZE,,,,,ANGH.)

        gratio
            Allowable growth ratio used for proximity checking.  Defaults to
            1.5 for h-elements (size level 6).  Values from 1.2 to 5.0 are
            allowed; however, values from 1.5 to 2.0 are recommended.

        smhlc
            Small hole coarsening key, can be ON (default for size level 6) or
            OFF.  If ON, this feature suppresses curvature refinement that
            would result in very small element edges (i.e., refinement around
            small features).

        smanc
            Small angle coarsening key, can be ON (default for all levels) or
            OFF.  If ON, this feature restricts proximity refinement in areas
            where it is ill-advised (that is, in tight corners on areas,
            especially those that approach 0 degrees).

        mxitr
            Maximum number of sizing iterations (defaults to 4 for all levels).

        sprx
            Surface proximity refinement key, can be off (SPRX = 0, which is
            the default for all levels) or on via two different values (SPRX =
            1 or SPRX = 2).  If SPRX = 1, surface proximity refinement is
            performed and any shell elements that need to be modified are
            modified.  If SPRX=2, surface proximity refinement is performed but
            no shell elements are altered.

        Notes
        -----
        If a valid level number (1 (fine) to 10 (coarse)) is input on SIZLVL,
        inputs for remaining arguments are ignored, and the argument values are
        set as shown in Table: 229:: SMRTSIZE - Argument Values for h-elements
        .

        The settings shown are for h-elements. The first column contains SIZLV
        data, ranging from 10 (coarse) to 1 (fine). The default is 6 (indicated
        by the shaded row).

        Table: 229:: : SMRTSIZE - Argument Values for h-elements
        """
        command = f"SMRTSIZE,{sizlvl},{fac},{expnd},{trans},{angl},{angh},{gratio},{smhlc},{smanc},{mxitr},{sprx}"
        return self.run(command, **kwargs)

    def tchg(self, ename1="", ename2="", etype2="", **kwargs):
        """Converts 20-node degenerate tetrahedral elements to their 10-node non-

        APDL Command: TCHG
        degenerate counterparts.

        Parameters
        ----------
        ename1
            Name (or the number) of the 20-node tetrahedron element that you
            want to convert.  This argument is required.

        ename2
            Name (or the number) of the 10-node tetrahedron element to which
            you want to convert the ENAME  elements.  This argument is
            required.

        etype2
            Element TYPE reference number for ENAME2.  If ETYPE2 is 0 or is not
            specified, the program selects the element TYPE reference number
            for ENAME2.  See the "Notes" section for details.  This argument is
            optional.

        Notes
        -----
        The TCHG command allows you to specify conversion of any selected
        20-node brick that is degenerated into a tetrahedron to a 10-node
        tetrahedron.

        The TCHG command is useful when used in with the MOPT,PYRA command.
        Twenty-node pyramid shaped elements may be used in the same volume with
        10-node tetrahedra.

        Performing a conversion is likely to create circumstances in which more
        than one element type is defined for a single volume.

        If specified, ETYPE2 will usually be the same as the local element TYPE
        number (ET,ITYPE) that was assigned to ENAME2 with the ET command.  You
        can specify a unique number for ETYPE2 if you prefer.  Although ETYPE2
        is optional, it may be useful when two or more ITYPEs have been
        assigned to the same element (for example, if two SOLID187 elements
        have been established in the element attribute tables for the current
        model, use the ETYPE2 argument to distinguish between them).  If ETYPE2
        is nonzero and it has not already been assigned to an element via ET,
        the program assigns the ETYPE2 value to ENAME2 as its element TYPE
        reference number.

        If ETYPE2 is 0 or is not specified, the program determines the element
        TYPE reference number for ENAME2 in one of these ways:

        If ETYPE2 is 0 or is not specified, and ENAME2 does not appear in the
        element attribute tables, the program uses the next available (unused)
        location in the element attribute tables to determine the element TYPE
        reference number for ENAME2.

        If ETYPE2 is 0 or is not specified, and ENAME2 appears in the element
        attribute tables, the program uses ENAME2 's existing element TYPE
        reference number for ETYPE2 .  (If there is more than one occurrence of
        ENAME2 in the element attribute tables (each with its own TYPE
        reference number), the program uses the first ENAME2 reference number
        for ETYPE2 .)

        You cannot use element conversion if boundary conditions or loads are
        applied directly to any selected elements.

        For more information about converting degenerate tetrahedral elements,
        see Meshing Your Solid Model in the Modeling and Meshing Guide
        """
        command = f"TCHG,{ename1},{ename2},{etype2}"
        return self.run(command, **kwargs)

    def timp(self, elem="", chgbnd="", implevel="", **kwargs):
        """Improves the quality of tetrahedral elements that are not associated

        APDL Command: TIMP
        with a volume.

        Parameters
        ----------
        elem
            Identifies the tetrahedral elements to be improved.  Valid values
            are ALL and P.  If ELEM = ALL (default), improve all selected
            tetrahedral elements.  If ELEM = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).

        chgbnd
            Specifies whether to allow boundary modification.  Boundary
            modification includes such things as changes in the connectivity of
            the element faces on the boundary and the addition of boundary
            nodes.  (Also see the Notes section below for important usage
            information for CHGBND.)

            0 - Do not allow boundary modification.

            1 - Allow boundary modification (default).

        implevel
            Identifies the level of improvement to be performed on the
            elements.  (Improvement occurs primarily through the use of face
            swapping and node smoothing techniques.)

            0 - Perform the least amount of swapping/smoothing.

            1 - Perform an intermediate amount of swapping/smoothing.

            2 - Perform the greatest amount of swapping/smoothing.

            3 - Perform the greatest amount of swapping/smoothing, plus additional improvement
                techniques (default).

        Notes
        -----
        The TIMP command enables you to improve a given tetrahedral mesh by
        reducing the number of poorly-shaped tetrahedral elements (in
        particular, the number of sliver tetrahedral elements)--as well as the
        overall number of elements--in the mesh.  It also improves the overall
        quality of the mesh.

        TIMP is particularly useful for an imported tetrahedral mesh for which
        no geometry information is attached.

        Regardless of the value of the CHGBND argument, boundary mid-nodes can
        be moved.

        When loads or constraints have been placed on boundary nodes or mid-
        nodes, and boundary mid-nodes are later moved, ANSYS issues a warning
        message to let you know that it will not update the loads or
        constraints.

        No boundary modification is performed if shell or beam elements are
        present in the mesh, even when CHGBND = 1.
        """
        command = f"TIMP,{elem},{chgbnd},{implevel}"
        return self.run(command, **kwargs)

    def type(self, itype="", **kwargs):
        """Sets the element type attribute pointer.

        APDL Command: TYPE

        Parameters
        ----------
        itype
            Assign this type number to the elements (defaults to 1).

        Notes
        -----
        Activates an element type number to be assigned to subsequently defined
        elements.  This number refers to the element type number (ITYPE)
        defined with the ET command.  Type numbers may be displayed [/PNUM].

        In some cases, ANSYS can proceed with a meshing operation even when no
        logical element type has been assigned via TYPE or XATT,,,TYPE.  For
        more information, see the discussion on setting element attributes in
        Meshing Your Solid Model in the Modeling and Meshing Guide.

        Examples
        --------

        Set the type pointer to 2

        >>> mapdl.type(2)
        """
        command = f"TYPE,{itype}"
        return self.run(command, **kwargs)

    def vatt(self, mat="", real="", type_="", esys="", secnum="", **kwargs):
        """Associates element attributes with the selected, unmeshed volumes.

        APDL Command: VATT

        Parameters
        ----------
        mat, real, type\\_, esys, secnum
            Material number, real constant set number, type number, coordinate
            system number, and section number to be associated with selected,
            unmeshed volumes.

        Notes
        -----
        These element attributes will be used when the volumes are meshed.  If
        a volume does not have attributes associated with it (by this command)
        at the time it is meshed, the attributes are obtained from the then
        current MAT, REAL, TYPE, ESYS, and SECNUM command settings.  Reissue
        the VATT command (before volumes are meshed) to change the attributes.
        A zero (or blank) argument removes the corresponding association.

        If any of the arguments MAT, REAL, TYPE, ESYS or SECNUM are defined as
        -1, then that value will be left unchanged in the selected set.

        In some cases, ANSYS can proceed with a volume meshing operation even
        when no logical element type has been assigned via VATT,,,TYPE or TYPE.
        For more information, see the discussion on setting element attributes
        in Meshing Your Solid Model of the Modeling and Meshing Guide.
        """
        command = f"VATT,{mat},{real},{type_},{esys},{secnum}"
        return self.run(command, **kwargs)

    def vclear(self, nv1="", nv2="", ninc="", **kwargs):
        """Deletes nodes and volume elements associated with selected volumes.

        APDL Command: VCLEAR

        Parameters
        ----------
        nv1, nv2, ninc
            Delete mesh for volumes NV1 to NV2 (defaults to NV1) in steps of
            NINC (defaults to 1).  If NV1 = ALL, NV2 and NINC are ignored and
            mesh for all selected volumes [VSEL] is deleted.  If NV1 = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).  A component name may also be
            substituted for NV1 (NV2 and NINC are ignored).

        Notes
        -----
        Deletes all nodes and volume elements associated with selected volumes
        (regardless of whether the nodes or elements are selected).  Nodes
        shared by adjacent meshed volumes and nodes associated with non-volume
        elements will not be deleted.  Attributes assigned as a result of VATT
        are maintained.  In the program's response to the command, if a volume,
        area, line, or keypoint is tallied as "cleared," it means either its
        node or element reference was deleted.
        """
        command = f"VCLEAR,{nv1},{nv2},{ninc}"
        return self.run(command, **kwargs)

    def vimp(self, vol="", chgbnd="", implevel="", **kwargs):
        """Improves the quality of the tetrahedral elements in the selected

        APDL Command: VIMP
        volume(s).

        Parameters
        ----------
        vol
            Number of the volume containing the tetrahedral elements to be
            improved.  If ``VOL = ALL`` (default), improve the tetrahedral elements
            in all selected volumes.  If ``VOL = P``, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).  A component name may also be substituted for ``VOL``.

        chgbnd
            Specifies whether to allow boundary modification.  Boundary
            modification includes such things as changes in the connectivity of
            the element faces on the boundary and the addition of boundary
            nodes.  (Also see "Notes" below for important usage information for
            ``CHGBND``.)

            0 - Do not allow boundary modification.

            1 - Allow boundary modification (default).

        implevel
            Identifies the level of improvement to be performed on the
            elements.  (Improvement occurs primarily through the use of face
            swapping and node smoothing techniques.)

            0 - Perform the least amount of swapping/smoothing.

            1 - Perform an intermediate amount of swapping/smoothing.

            2 - Perform the greatest amount of swapping/smoothing.

            3 - Perform the greatest amount of swapping/smoothing, plus
            additional improvement techniques (default).

        Notes
        -----
        ``VIMP`` is useful for further improving a volume mesh created in ANSYS
        [``VMESH``], especially quadratic tetrahedral element meshes.

        The ``VIMP`` command enables you to improve a given tetrahedral mesh by
        reducing the number of poorly-shaped tetrahedral elements (in
        particular, the number of sliver tetrahedral elements)--as well as the
        overall number of elements--in the mesh.  It also improves the overall
        quality of the mesh.

        Regardless of the value of the ``CHGBND`` argument, boundary mid-nodes can
        be moved.

        When loads or constraints have been placed on boundary nodes or mid-
        nodes, and boundary mid-nodes are later moved, ANSYS issues a warning
        message to let you know that it will not update the loads or
        constraints.

        Even when ``CHGBND = 1``, no boundary modification is performed on areas
        and lines that are not modifiable (for example, areas that are adjacent
        to other volumes or that contain shell elements, or lines that are not
        incident on modifiable areas, contain beam elements, or have line
        divisions specified for them [``LESIZE``]).
        """
        command = f"VIMP,{vol},{chgbnd},{implevel}"
        return self.run(command, **kwargs)

    def vmesh(self, nv1="", nv2="", ninc="", **kwargs):
        """Generates nodes and volume elements within volumes.

        APDL Command: VMESH

        Parameters
        ----------
        nv1, nv2, ninc
            Mesh volumes from NV1 to NV2 (defaults to NV1) in steps of NINC
            (defaults to 1).  If NV1 = ALL, NV2 and NINC are ignored and all
            selected volumes [VSEL] are meshed.  If NV1 = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may also be substituted for NV1 (NV2
            and NINC are ignored).

        Notes
        -----
        Missing nodes required for the generated elements are created and
        assigned the lowest available numbers [NUMSTR].  During a batch run and
        if elements already exist, a mesh abort will write an alternative
        database file (File.DBE) for possible recovery.

        Tetrahedral mesh expansion [MOPT,TETEXPND,Value] is supported for both
        the VMESH and FVMESH commands.

        Examples
        --------

        Set the material ID and type pointers to 2, then mesh volume 1
        using mat 2 and type 2.

        >>> mapdl.mat(2)
        >>> mapdl.type(2)
        >>> mapdl.vmesh(1)
        """
        command = f"VMESH,{nv1},{nv2},{ninc}"
        return self.run(command, **kwargs)

    def veorient(self, vnum="", option="", value1="", value2="", **kwargs):
        """Specifies brick element orientation for volume mapped (hexahedron)

        APDL Command: VEORIENT
        meshing.

        Parameters
        ----------
        vnum
            Number identifying volume for which elements are to be oriented (no
            default).

        option
            Option for defining element orientation:

            KP - Orientation is determined by two keypoints on the volume. Input the keypoint
                 numbers (KZ1 and KZ2) in fields VALUE1 and VALUE2,
                 respectively. The element z-axis points from KZ1 toward KZ2.
                 Element x and y directions point away from KZ1 along edges of
                 the volume to make a right-hand triad. (The element x- and
                 y-axes are uniquely determined by this specification.)

            LINE - Orientation is determined by one of the lines defining the volume. Input the
                   line number in field VALUE1. The element z direction follows
                   the direction of the line. Input a negative value if the
                   desired z direction is opposite to the direction of the
                   specified line. (The element x- and y-axes are uniquely
                   determined by this specification.) (VALUE2 is not used.)

            AREA - Orientation is determined by one of the areas defining the volume. The area
                   represents the desired element top surface. Input the area
                   number as VALUE1. The shortest line in the volume connected
                   to the area will be used to specify the element z direction.
                   (If more than one shortest line exists, the lowest numbered
                   of those is used.) Element x and y directions are not
                   uniquely specified by this option. (VALUE2 is not used.)

            THIN - Align the element z normal to the thinnest dimension of the volume. The
                   shortest line in the volume is used to specify the element z
                   direction. (If more than one shortest line exists, the
                   lowest numbered of those is used.) Element x and y
                   directions are not uniquely specified by this option.
                   (VALUE1 and VALUE2 are not used.)

            DELE - Delete the previously defined volume orientation for the specified volume
                   (VNUM).  (VALUE1 and VALUE2 are not used.)

        value1, value2
            Parameters required for the element z-axis direction specification.
            The meaning of VALUE1 and VALUE2 will depend on the chosen Option.
            See the description of Option above for details.

        Notes
        -----
        Use VEORIENT before the VMESH command to specify the desired
        orientation of brick elements in a mapped mesh. VEORIENT has no effect
        on tetrahedron meshes, extruded meshes (VROTAT, VDRAG, VEXT, etc.), or
        swept meshes (VSWEEP).

        Proper brick orientation is essential for certain element types such as
        SOLID185 Layered Solid, SOLID186 Layered Solid, and SOLSH190. In such
        cases, use VEORIENT or EORIENT to achieve the desired orientation. For
        other brick element types, you may need to specify element orientation
        to control orthotropic material property directions without concern for
        the element connectivity. For those cases, the ESYS command is the
        preferred method of specifying the material property directions.

        For Option = LINE, AREA, and THIN, the orientation will be internally
        converted to an equivalent Option = KP specification (KP,KZ1,KZ2). Use
        the VLIST command to view the element orientations (in terms of KZ1 and
        KZ2) associated with each volume.
        """
        command = f"VEORIENT,{vnum},{option},{value1},{value2}"
        return self.run(command, **kwargs)

    def vsweep(self, vnum="", srca="", trga="", lsmo="", **kwargs):
        """Fills an existing unmeshed volume with elements by sweeping the mesh

        APDL Command: VSWEEP
        from an adjacent area through the volume.

        Parameters
        ----------
        vnum
            Number identifying the volume that is to be meshed by VSWEEP.  If
            VNUM = P, graphical picking is enabled, you will be prompted to
            choose the volume or volumes based on the setting of
            EXTOPT,VSWE,AUTO.  This argument is required.

        srca
            Number identifying the source area.  This is the area whose mesh
            will provide the pattern for the volume elements.  (If you do not
            mesh the source area prior to volume sweeping, ANSYS meshes it
            internally when you initiate volume sweeping.)  ANSYS sweeps the
            pattern of the area elements through the volume to create the mesh
            of volume elements.  You cannot substitute a component name for
            SRCA.

        trga
            Number identifying the target area.  This is the area that is
            opposite the source area specified by SRCA.  You cannot substitute
            a component name for TRGA.

        lsmo
            Value specifying whether ANSYS should perform line smoothing during
            volume sweeping.  (The value of this argument controls line
            smoothing for the VSWEEP command only;  it has no effect on the
            setting of the MOPT command's LSMO option.)  This argument is
            optional.

            0 - Do not perform line smoothing.  This is the default.

            1 - Always perform line smoothing.  This setting is not recommended for large
                models due to speed considerations.

        Notes
        -----
        If the source mesh consists of quadrilateral elements, ANSYS fills the
        volume with hexahedral elements.  If the source mesh consists of
        triangles, ANSYS fills the volume with wedges.  If the source mesh
        consists of a combination of quadrilaterals and triangles, ANSYS fills
        the volume with a combination of hexahedral and wedge elements.

        In the past, you may have used the VROTAT, VEXT, VOFFST, and/or VDRAG
        commands to extrude a meshed area into a meshed volume.  However, those
        commands create the volume and the volume mesh simultaneously.  In
        contrast, the VSWEEP command is intended for use in an existing
        unmeshed volume.  This makes VSWEEP particularly useful when you have
        imported a solid model that was created in another program, and you
        want to mesh it in ANSYS.

        For related information, see the description of the EXTOPT command
        (although EXTOPT sets volume sweeping options, it does not affect
        element spacing). Also see the detailed discussion of volume sweeping
        in Meshing Your Solid Model of the Modeling and Meshing Guide.
        """
        command = f"VSWEEP,{vnum},{srca},{trga},{lsmo}"
        return self.run(command, **kwargs)
