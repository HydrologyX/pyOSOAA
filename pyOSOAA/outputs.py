import numpy as np


def ExtractValue(text, reference):
    """ This function extracts the value for a given reference string for the
        text string given and returns it as a float number
        text        Text to search
        reference   Reference string
        """
    for a in text:
        if reference in a:
            res = a.replace(reference, "")

    return float(res)


class VSVZA(object):
    """ This file provides the upwelling radiance field (i.e., the Stokes
        paramaters I,Q,U where I is the radiance) versus the viewing zenith
        angle, for the given relative azimuth angle (-OSOAA.View.Phi) and
        for the given altitude or depth (-OSOAA.View.Z associated to
        -OSOAA.View.Level equals 5).
        This ascii file is composed of a header which describes in detail
        the structure of the file and columns data.
        """

    def __init__(self, resroot, filename="LUM_vsVZA.txt"):
        """ Filename defined by -OSOAA.ResFile.vsVZA, if none is defined
            then LUM_vsVZA.txt is used:
            This file provides the upwelling radiance field (i.e., the
            Stokes paramaters I,Q,U where I is the radiance) versus the
            viewing zenith angle, for the given relative azimuth angle
            (-OSOAA.View.Phi) and for the given altitude or depth
            (-OSOAA.View.Z associated to -OSOAA.View.Level equals 5).
            This ascii file is composed of a header which describes in
            detail the structure of the file and columns data.

            resroot     OSOAA results root directory
            filename    Filename to look for the results.
            fulltext    Full file text.
            vzaless     Simulated relative azimuth (degrees) for VZA < 0
                        (sign convention)
            vzamore     Simulated relative azimuth (degrees) for VZA > 0
                        (sign convention)
            depth       Value of the depth selected for the output (m)
            vza         Viewing Zenith Angle (deg)
            scaang      Scattering angle (deg)
            I           Stokes parameter at output level Z (in sr-1)
                        normalised to the extraterrestrial solar irradiance
                        (PI * L(z) / Esun)
            refl        Reflectance at output level Z (PI * L(z) / Ed(z))
            polrate     Degree of polarization (%)
            lpol        Polarized intensity at output level Z (in sr-1)
                        normalised to the extraterrestrial solar irradiance
                        (PI * Lpol(z) / Esun)
            reflpol     Polarized reflectance at output level Z
                        (PI * Lpol(z) / Ed(z))
            """

        # We open the file with the corresponding encoding and convert it
        # to a text string.
        if filename is None:
            filename = "LUM_vsVZA.txt"
        with open(resroot+"/Standard_outputs/"+filename,
                  encoding="iso-8859-15") as file:
            self.fulltext = file.readlines()
        # Read variables not tabulated
        self.vzaless = ExtractValue(self.fulltext,
                                    "for VZA < 0 (sign convention):")
        self.vzamore = ExtractValue(self.fulltext,
                                    "for VZA > 0 (sign convention):")
        self.depth = ExtractValue(self.fulltext,
                                  "Value of the depth selected for the "
                                  + "output (m) :")

        # Get header length to skip it
        skipheader = [idx for idx, text in enumerate(self.fulltext)
                      if "VZA    SCA_ANG" in text][0]
        self.vza, self.scaang, self.I, self.refl, self.polrate, self.lpol,\
        self.reflpol = np.genfromtxt(resroot+"/Standard_outputs/"+filename,
                                     skip_header=skipheader+1, unpack=True,
                                     encoding="iso-8859-15")

class VSZ(object):
    """ Filename defined by -OSOAA.ResFile.vsZ:
        This optional file provides the radiance field (I,Q,U) versus the
        altitude or depth, for the given relative azimuth angle
        (-OSOAA.View.Phi) and for the given viewing zenith angle
        (-OSOAA.View.VZA).
        """

    def __init__(self, resroot, filename=None):
        """ Filename defined by -OSOAA.ResFile.vsZ:
            This optional file provides the radiance field (I,Q,U) versus
            the altitude or depth, for the given relative azimuth angle
            (-OSOAA.View.Phi) and for the given viewing zenith angle
            (-OSOAA.View.VZA).
            resroot     OSOAA results root directory.
            filename    Filename to look for the results.
            fulltext    Full file text.
            z           Depth in the sea (meters)
            scaang      Scattering angle (deg)
            I           Stokes parameter at level Z (in sr-1) normalised to the
                        extraterrestrial solar irradiance
                        (PI * L(z) / Esun)
            refl        Reflectance at level Z
                        (PI * L(z) / Ed(z))
            polrate     Degree of polarization (%)
            lpol        Polarized intensity at level Z (in sr-1) normalised to
                        the extraterrestrial solar  irradiance
                        (PI * Lpol(z) / Esun)
            reflpol     Polarized reflectance at level Z
                        (PI * Lpol(z) / Ed(z))
            """

        with open(resroot+"/Standard_outputs/"+filename,
                  encoding="iso-8859-15") as file:
            self.fulltext = file.readlines()
        # Read variables not tabulated
        self.simazimuth = ExtractValue(self.fulltext,
                                       "Simulated relative azimuth (degrees) :")
        self.updirecion = ExtractValue(self.fulltext,
                                       "Upward direction VZA (degrees) :")

        # Get header length to skip it
        skipheader = [idx for idx, text in enumerate(self.fulltext)
                      if "       Z     SCA_ANG" in text][0]
        self.z, self.scaang, self.I, self.refl, self.polrate,\
        self.lpol, self.reflpol = np.genfromtxt(resroot+"/Standard_outputs/"+filename,
                                                skip_header=skipheader+1,
                                                unpack=True,
                                                encoding="iso-8859-15")

class OUTPUTS(object):
    """ This class contains the standard and advanced outputs generated by the
        OSOAA software"""

    def __init__(self, resroot, filenames):
        """ This methods inits the output class with all the avalaible outputs.
            resroot     Results root Directory
            filenames   Object with all filenames
            """

        self.vsvza = VSVZA(resroot, filenames.vsvza)
        if filenames.vsz is not None:
            self.vsz = VSZ(resroot, filenames.vsz)