SPLUS-MOON
==========

Reads SPLUS FITSFILE and calculates moon position and illumination at the DATETIME of the observation.

Usage
-----

To run **SPLUS-MOON** just execute::

	$./splus-moon.py FITSFILE


Example
-------

A simple example of result::

	$./moon_digest.py SPLUS-GAL-20180713-042623.fits.fz 
	OBJECT COORD (RA, DEC) : (273.98271666666665 deg, -28.07726361111111 deg)
	T80S DATETIME OBS:  2018-07-13 00:25:02.729000-04:00
	T80S DATETIME OBS ZoneInfo:  America/Santiago
	T80S DATETIME INI OBS:  2018-07-13 00:25:03.258000-04:00
	OBJECT COORD INI OBS (ALT, AZ) : (79.15271735462748 deg, 278.13763912778046 deg)
	MOON SEPARATION INI OBS: 161.28649 deg
	MOON ILLUMINATION INI OBS: 0.00020
	T80S DATETIME END OBS:  2018-07-13 00:25:59.270000-04:00
		OBS DURATION:  56.012
	OBJECT COORD END OBS (ALT, AZ) : (78.9523633264309 deg, 277.87435125012064 deg)
	MOON SEPARATION END OBS: 161.27437 deg
	MOON ILLUMINATION END OBS: 0.00020
	####################################
	MEAN MOON SEPARATION: 161.28043 deg
	MEAN MOON ILLUMINATION: 0.00020
	####################################

Contact
-------
	
Contact us: [dhubax@gmail.com](mailto:dhubax@gmail.com).
