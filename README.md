SPLUS-MOON
==========

Reads [S-PLUS](https://splus.cloud/) Image FITS Header and calculates moon position and illumination at the DATETIME of the observation. If `--append` option is set, the program will also append the new information to the Image FITS Header.

Usage
-----

**SPLUS-MOON** usage:

	usage: splus-moon.py [-h] [--append] FITSFILE

	Reads S-PLUS Image FITS Header and calculates moon position and illumination at the DATETIME of the observation.

	positional arguments:
  		FITSFILE      Observed Image FITS filename

	options:
  		-h, --help    show this help message and exit
  		--append, -A  Append calculated information to the Image FITS header

Example
-------

A simple example of result::

	$./splus-moon.py SPLUS-GAL-20180713-042623.fits.fz 
	OBJECT COORD (RA, DEC) : (18:15:55.852, -28:04:38.149)
	T80S DATETIME OBS: 2018-07-13T04:25:02.729000
	T80S DATETIME INI OBS: 2018-07-13 00:25:03.258000-04:00
	OBJECT COORD INI OBS (ALT, AZ) : (79.15271735462748 deg, 278.13763912778046 deg)
	MOON SEPARATION INI OBS: 161.28648794606855 deg
	MOON ILLUMINATION INI OBS: 0.00019896476842184985
	T80S DATETIME END OBS: 2018-07-13 00:25:59.270000-04:00
		OBS DURATION: 56.012 s
	OBJECT COORD END OBS (ALT, AZ) : (78.9523633264309 deg, 277.87435125012064 deg)
	MOON SEPARATION END OBS: 161.274369280656 deg
	MOON ILLUMINATION END OBS: 0.00020015159811270777
	####################################
	MEAN MOON SEPARATION: 161.2804286133623 deg
	MEAN MOON ILLUMINATION: 0.0001995581832672788
	####################################

Contact
-------
	
Contact us: [dhubax@gmail.com](mailto:dhubax@gmail.com).
